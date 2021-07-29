#2021/07/18
#selenium安装成功测试

from selenium import webdriver

#填写chromedriver安装地址

driver=webdriver.Chrome("D:\webDriver\chromedriver_win32\chromedriver.exe")
#填写需测试的网页地址

driver.get("https://www.jianshu.com/u/a2d1bc176e90")

#打开窗口最大化

driver.maximize_window()
