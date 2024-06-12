# coding:utf-8
import lxbasic.core as bsc_core

a = range(25)

# print bsc_core.RawListMtd.split_to(
#     a, 16
# )


def split_list(lst, min_size, max_chunks):
    if len(lst) <= min_size:
        return [lst]

    num_chunks = min((len(lst) + min_size - 1) // min_size, max_chunks)

    # 平均分配剩余的元素
    avg_size = len(lst) // num_chunks
    remainder = len(lst) % num_chunks

    chunks = []
    start = 0

    for i in range(num_chunks):
        end = start + avg_size + (1 if i < remainder else 0)
        chunks.append(lst[start:end])
        start = end

    return chunks

# 示例列表
lst = list(range(1, 1000))

# 每个切片数量不小于64，总切片数量不超过32，超过32个切片时平均分配
chunks = split_list(lst, 64, 32)
print len(chunks)
for chunk in chunks:
    print(chunk)


