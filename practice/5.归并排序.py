"""
@Author  ：Margot
@Date    ：2022/1/11 21:02 
@Question：MergeSort（数组递归地一分为二，最小数组排序，直到最后地两个大数组排序完成，即一个完整数组排序完成）
"""

import math


def merge(left, right):
    result = []
    ll = len(left)
    lr = len(right)
    i, j, k = 0, 0, 0
    while i < ll and j < lr:
        if left[i] < right[j]:
            result[k] = left[i]
            i += 1
            k += 1
        else:
            result[k] = right[j]
            j += 1
            k += 1
    while i < ll:
        result[k] = left[i]
        i += 1
        k += 1
    while j < lr:
        result[k] = right[j]
        j += 1
        k += 1
    return "".join(result)


# another merge function
def anothermerge(left, right):
    result = []
    while left and right:
        if left[0] <= right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    while left:
        result.append(left.pop(0))
    while right:
        result.append(right.pop(0))

    return result


def mergesort(s):
    if len(s) < 2:
        return s
    else:
        middle = math.floor(len(s) / 2)
        left, right = s[0:middle], s[middle:]
    return anothermerge(mergesort(left), mergesort(right))


if __name__ == "__main__":
    a = input("请输入一组数字：")
    s = list(a)
    print(mergesort(s))
