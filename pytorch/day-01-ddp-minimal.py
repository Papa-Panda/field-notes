"""Day 01 最小 DDP 闭环（与 notebook Cell 8 同源）。
标准起法: torchrun --nproc_per_node=2 day-01-ddp-minimal.py
"""
import os
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP


def main():
    # torchrun 会注入 RANK / WORLD_SIZE / MASTER_ADDR / MASTER_PORT
    dist.init_process_group("gloo")

    torch.manual_seed(0)  # DDP 铁律：各 rank 初始参数必须一致
    model = DDP(torch.nn.Linear(10, 1))
    opt = torch.optim.SGD(model.parameters(), lr=0.1)

    x = torch.randn(32, 10)
    y = torch.randn(32, 1)
    opt.zero_grad()
    loss = ((model(x) - y) ** 2).mean()
    loss.backward()  # DDP 在这里 hook 了 gradient bucketing + all-reduce
    opt.step()

    # 验证：all_gather 各 rank 更新后的参数，应 bit 级一致
    params = torch.cat([p.data.view(-1) for p in model.parameters()])
    gathered = [torch.zeros_like(params) for _ in range(dist.get_world_size())]
    dist.all_gather(gathered, params)
    if dist.get_rank() == 0:
        for r in range(1, dist.get_world_size()):
            d = (gathered[0] - gathered[r]).abs().max().item()
            print(f"rank0 vs rank{r}: 参数最大差 = {d:.2e}  (应为 0)")
        print(f"loss = {loss.item():.4f}")
    dist.destroy_process_group()


if __name__ == "__main__":
    main()
