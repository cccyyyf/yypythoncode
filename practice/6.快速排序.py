"""
@Author  ：Margot
@Date    ：2022/1/13 20:42 
@Question：QuickSort（选择一个基准，将基准左右两边的数值进行排序。递归）
@Note：
归并和快排用的都是分治思想，递推公式和递归代码也非常相似，那它们的区别在哪里呢？
归并排序，是先递归调用，再进行合并，合并的时候进行数据的交换。所以它是自下而上的排序方式。何为自下而上？就是先解决子问题，再解决父问题。
快速排序，是先分区，在递归调用，分区的时候进行数据的交换。所以它是自上而下的排序方式。何为自上而下？就是先解决父问题，再解决子问题。
"""


def quicksort(s, low, high):
    if low < high:
        i = low
        j = high
        while i < j and s[j] >= s[i]:
            j -= 1
        swap(s, i, j)
        while i < j and s[i] <= s[j]:
            i += 1
        swap(s, i, j)
        quicksort(s, low, j - 1)
        quicksort(s, j + 1, high)
    return "".join(s)


def swap(s, i, j):
    s[i], s[j] = s[j], s[i]


if __name__ == "__main__":
    a = input("请输入一组数字：")
    s = list(a)
    l = len(s)
    print(quicksort(s, 0, l - 1))
