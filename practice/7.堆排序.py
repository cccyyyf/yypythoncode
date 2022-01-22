"""
@Author  ：Margot
@Date    ：2022/1/17 21:16 
@Question：HeapSort
@Note：
堆要满足两个点：完全二叉树、父节点大于子节点
思路：1.按照初始数组构造初始堆；
     2.每次交换第一个和最后一个元素，输出最后一个元素（最大值），此时破坏了堆的结构，将剩余数值重新构建为堆，重复前面操作直到数组排序完成
"""
import math


def heapify(tree, i):
    m = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < treel and tree[left] > tree[m]:
        m = left
    if right < treel and tree[right] > tree[m]:
        m = right
    if m != i:
        swap(tree, m, i)
        heapify(tree, m)


def swap(tree, i, j):
    tree[i], tree[j] = tree[j], tree[i]


def heapsort(tree):
    global treel
    treel = len(tree)
    # 初始建堆（从最后一个非叶子节点开始)
    for i in range(math.floor(treel / 2) - 1, -1, -1):
        heapify(tree, i)
    # 堆排序
    for i in range(treel - 1, 0, -1):
        # 交换当前节点和堆顶节点
        swap(tree, 0, i)
        treel -= 1
        heapify(tree, 0)
    return ''.join(tree)


if __name__ == "__main__":
    a = input("请输入一组数字：")
    s = list(a)
    print(heapsort(s))
