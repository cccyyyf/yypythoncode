from objects.webpage.utils.PropertiesUtil import ConfigUtil,PropertiesUtil
from objects.webpage.baseObjects.BaseObjectPO import PageObjectPO
import os
from RootPath import RootPath
import allure

# 获取ini配置信息
conf = ConfigUtil(RootPath.getWebIniPath())

class BaiduPO(PageObjectPO):

    def getPropertiesPath(self):
        """
        获取yaml文件路径
        """
        return os.path.join(os.path.dirname(__file__),  "BaiduPO.yml").replace("objects", "resources")


    @allure.step("打开网址")
    def open_baidu(self):
        self.goTo("http://www.baidu.com")

    @allure.step("输入搜索内容")
    def input_content(self,text):

        self.sendKeys(locator="输入框",keyWords=text)

    @allure.step("点击百度一下")
    def click_button(self):
        search_button = PropertiesUtil.loadLocatorValueFromYml(path=self.getPropertiesPath(),key="百度一下")
        self.click(search_button)