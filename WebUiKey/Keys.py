#2021/07/19
'''

Selenium的关键字驱动类：
    自定义封装一个为自己所拥有的自动化测试行为库，包含所有你需要的常用测试操作行为。

'''
from time import sleep
from selenium import webdriver

#初始化浏览器对象：满足各类浏览器的初始化---
def open_browser(txt):
    try:
        driver = getattr(webdriver, txt)()     #getattr()函数用于返回一个对象属性值
    except Exception as e:
        print(e)
        driver = webdriver.chrome()
    return driver


class Key:
    #临时创建driver对象
    #driver = webdriver.Chrome()

    #构造函数---
    def __init__(self,txt):
        self.driver = open_browser(txt)

    #访问url
    def open(self, url):
        self.driver.get(url)

    #元素定位:需要满足8种元素定位的方法
    def locator(self, name, value):
        return self.driver.find_element(name, value)

    #输入
    def input(self, name, value, txt):
        self.locator(name, value).send_keys(txt)

    #点击
    def click(self,name, value):
        self.locator(name, value).click()

    #等待
    def sleep(self, txt):
        sleep(txt)

    #关闭浏览器，释放资源
    def quit(self):
        self.driver.quit()

    #窗口最大化
    def maxwindow(self):
        self.driver.maximize_window()