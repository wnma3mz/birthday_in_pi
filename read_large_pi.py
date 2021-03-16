import time
from functools import partial
import copy

"""
http://www.numberworld.org/y-cruncher/
"""
fname = "pi_str.txt"


def chunked_file_reader(file, block_size=1024 * 8):
    """生成器函数分块读取文件内容使用 iter 函数"""
    # 首先使用 partial(fp.read, block_size) 构造一个新的无需参数的函数
    # 循环将不断返回 fp.read(block_size) 调用结果直到其为 '' 时终止
    for chunk in iter(partial(file.read, block_size), ""):
        yield chunk


def m1(target_str, block_size=1024 * 8):
    i = 0
    old_chunk = ""
    with open(fname) as f:
        for chunk in chunked_file_reader(f, block_size=block_size):
            if target_str in old_chunk + chunk:
                index = (old_chunk + chunk).find(target_str)
                return i * block_size + index + 1 - 2
            i += 1
            # old_chunk = copy.deepcopy(chunk[-len(target_str):])
    return -1


if __name__ == "__main__":
    target_str = "1415926"
    s1 = time.time()
    output = m1(target_str, 2048 * 20)
    print(output)
    print("m1 time: ", time.time() - s1)
