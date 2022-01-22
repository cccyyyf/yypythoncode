"""
@Author  ：Margot
@Date    ：2022/1/7 21:47 
@Question：SelectionSort（每次选出一个最大值放到末尾或最小值放在行首）
"""


def selectionsortmax(s):
    l = len(s)
    while l > 1:
        max = s[0]
        pos = 0
        for i in range(0, l):
            if s[i] > max:
                max = s[i]
                pos = i
        s[l - 1], s[pos] = s[pos], s[l - 1]
        l = l - 1
    return "".join(s)


def selectionsortmin(s):
    l = len(s)
    for i in range(l - 1):
        minpos = i
        for j in range(i + 1, l):
            if s[j] < s[minpos]:
                minpos = j
        if minpos != i:
            s[i], s[minpos] = s[minpos], s[i]
    return "".join(s)


if __name__ == "__main__":
    a = input("请输入一组数字：")
    s = list(a)
    print(selectionsortmin(s))
