#2021/07/18
#网易云自动登录
'''
八大元素定位法则
1.id,基于元素属性中id的值来进行定位，类似身份证号，不出意外不会有重复
2.name，类似人名，会有重复
3.link text，主要用于超链接定位
4.partial link text，link text的模糊查询版，类似数据库中的like %，匹配到多个时，选取第一个,如果使用elements则得到一个list，通过循环遍历出来
  基于此获取多元素操作：
  dr = driver.find_elements_by_partial_link_text('百度')
  for d in dr:
    print(d.text)
5.classname，基于元素样式定位，非常容易遇到重复（复杂的样式容易报错，简单的样式容易重复）
6.tagname，基于标签名来进行定位，重复度最高只有在定位后需要二次筛选的时候使用
7.cssselector，应用相对校对的一种行为，最初IE浏览器不支持xpath，完全基于class属性的定位
8.xpath，目前应用最多的一种行为，基于页面结构来进行的定位
  绝对路径：从html根路径下一层一层往下数，找到对应的层级，从而找到元素，除非十万火急，不要这么写
  相对路径：基于匹配制度来查找元素，依照xpath语法结构来走
  例如：  1. //*[@id="kw"]
  // 表示从根路径下开始查找
  * 表示任意元素
  [] 表示筛选条件（查找函数）
  @ 表示基于属性来筛选，如 @id="kw"表示基于id属性值为kw的条件来进行筛选
  如果要基于text来定位元素，在[]中添加text()="文本内容"进行查找，如//a[text()="登录"]
  如果文本内容不是text，是value，则使用@value，如//input[@value="登录"]
  当元素无法定位时，可定位子级的父级来获取元素
        2. //input[contains(@id,"kw")]
           //input[contains(text(),"百度一下")]
   contains表示进一步查找，匹配项模糊查找

  可用console：$x()或查找方式来校验定位是否正确
'''
import time
from selenium import webdriver
driver=webdriver.Chrome("D:\webDriver\chromedriver_win32\chromedriver.exe")
driver.get("https://music.163.com/")
# driver.get("https://github.com/")
# time.sleep(10)
# driver.find_element_by_xpath("/html/body/div[1]/header/div/div[2]/div[2]/div[2]").click()
