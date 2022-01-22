"""
@Author  ：Margot
@Date    ：2022/1/7 09:16 
@Question：两个继承类问题
"""

# B类继承自A类，实例化B类后，调用get方法，父类中的方法会优先被执行，再执行子类中的同名方法，父类的方法会被覆盖。
class A:
    def get(self):
        self.say()

    def say(self):
        print("AAAAA")


class B(A):
    def say(self):
        print("BBBBB")


b = B()
b.get()

# isinstance() 考虑继承关系；type() 不考虑继承关系。
class A(object):
    pass


class B(A):
    pass


print(isinstance(A(), A))
print(isinstance(B(), A))
print(type(A()) == A)
print(type(B()) == A)
