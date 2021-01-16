# coding=utf-8
# Time : 2020/9/16 10:18
# Author : huxin
import allure
from objects.webpage.baidu.test.BaiduPO import BaiduPO
import time


@allure.feature("百度网站WEB测试")
class TestBaiduSearch(BaiduPO):

    def teardown_class(self):
        self.closeAllBrowsers(self)

    @allure.story("测试首页搜素功能")
    def test_HomeSearch(self):
        # 打开百度
        self.open_baidu()
        # 输入内容“百度测试”
        self.input_content("百度测试")
        # 点击“百度一下”
        self.click_button()
        # 断言搜索结果
        self.verifyElementExists(locator="视频图标")
