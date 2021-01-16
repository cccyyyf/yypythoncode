# coding=utf-8
# Author: wanghui
# Time : 2020/9/27

import allure
from objects.interface.baseObjects.BaseObj import BaseObj
from objects.interface.utils.DBRequest import *
from RootPath import RootPath
from configparser import ConfigParser
import json



class TenantPO(BaseObj):

    # 获取token
    def getToken(self, **kwargs):
        """
        获取token值
        """
        body = {"loginName": kwargs["loginName"], "password": kwargs["password"]}
        try:
            response = self.do_post(url=kwargs["url"], params=body)
            token = response["resultData"]["token"]
            return token
        except Exception as e:
            print("获取token失败")
            print(e)

    # 调用Check token接口
    def check_token(self, **kwargs):
        token = self.getToken(**kwargs)
        header = {'Content-Type': 'application/json', 'Authorization': token}
        url = "http://10.10.15.213:8877/userCenterApi/sso/checkToken"
        try:
            response = self.do_get(url, header)
        except Exception as e:
            print("调用checkToken失败")
            print(e)



# get方法请求测试示例
if __name__ == '__main__':
    test_fun = TenantPO()
    login_param = {"url": "http://10.10.15.213:8877/userCenterApi/auth/login", "loginName": "admin",
                      "password": "123456"}
    print(test_fun.check_token(**login_param))