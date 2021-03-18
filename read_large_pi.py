import copy
import time
from functools import partial

"""
使用http://www.numberworld.org/y-cruncher/生成的txt文件，填写对应的文件路径至fname中。
pi_str.txt为小数据参考测试
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
                return i * block_size + index + 1 - 2 - len(old_chunk)
            i += 1
            old_chunk = copy.deepcopy(chunk[-len(target_str) :])
    return -1


def m2(target_str):
    # 一般查询方法的性能，若查询不到则返回-2（-1+1-2）
    with open(fname) as f:
        data = f.read()
    return data.find(target_str) + 1 - 2


if __name__ == "__main__":
    target_str = input("请输入需要查询的数字\n")
    s1 = time.time()
    output = m1(target_str, 20 * 2048)
    if output == -1:
        print("未查询到")
    else:
        print("开始位数：", output)
    print("花费时间: ", time.time() - s1)
    input("输入任意键退出查询")