"""
@Author  ：Margot
@Date    ：2022/1/10 21:20 
@Question：ShellSort（递减增量排序，插入排序高效版本）
"""

import math


def shellsort(s):
    l = len(s)
    gap = math.floor(l / 2)
    while gap > 0:
        for i in range(gap, l):
            temp = s[i]
            j = i - gap
            while j >= 0 and s[j] > temp:
                s[gap + j] = s[j]
                j -= gap
            s[j + gap] = temp
        gap = math.floor(gap / 2)
    return "".join(s)


if __name__ == "__main__":
    a = input("请输入一组数字：")
    s = list(a)
    print(shellsort(s))
