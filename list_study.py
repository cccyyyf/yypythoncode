# @Time: 2021/11/29 23:27
# @Auth: Margot

'''
生成一个平方列表，如[1,4,9...]
使用for循环怎么写？
使用列表推导式怎么写？
'''

def byfor():
    l = []
    for i in range(1,4):
        l.append(i**2)   # l.append(i*i)
    print(l)

def bylist():
    l1 = [i**2 for i in range(1,4)]
    print(l1)
    #列表推导式中还可以加if语句
    l2 = [i**2 for i in range(1,4) if i!=1]
    print(l2)
    #列表推导式同时可以嵌套循环
    l3 = [i*j for i in range(1,4) for j in range(1,4)]
    print(l3)
if __name__ == '__main__':
    bylist()

