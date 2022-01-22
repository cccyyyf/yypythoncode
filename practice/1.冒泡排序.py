"""
@Author  ：Margot
@Date    ：2022/1/6 22:27 
@Question：BubbleSort（两个两个比较，最后会找到一个最大值放置末尾）
"""


def bubblesort(s):
    l = len(s)
    sflag = 1
    if l == 1:
        print("数组长度为1不必比较")
    for j in range(l - 1, 0, -1):  # range倒序的用法
        for i in range(0, j):
            if s[i] > s[i + 1]:
                s[i], s[i + 1] = s[i + 1], s[i]
                sflag = 0
        if sflag == 1:
            break
    return "".join(s)


if __name__ == "__main__":
    a = input("请输入一组数字:")
    s = list(a)
    print(bubblesort(s))
