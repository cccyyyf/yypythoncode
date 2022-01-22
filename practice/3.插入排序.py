"""
@Author  ：Margot
@Date    ：2022/1/8 22:05
@Question：InsertSort（假设前面都是有序数字，仅需和最后一个值往前对比即可完成插入排序）
"""


def insertsort(s):
    l = len(s)
    for i in range(1, l):
        min = s[i]
        while i != 0 and s[i - 1] > min:
            s[i] = s[i - 1]
            i -= 1
        s[i] = min
    return "".join(s)


if __name__ == "__main__":
    a = input("请输入一组数字：")
    s = list(a)
    print(insertsort(s))
