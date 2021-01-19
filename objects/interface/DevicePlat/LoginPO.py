# coding=utf-8
# Time : 2020/10/11 19:43
# Author : huxin

from objects.interface.baseObjects.BaseObj import *
from objects.interface.utils.PropertiesUtil import *
from RootPath import *
import allure
import requests,json
from requests_toolbelt.multipart.encoder import MultipartEncoder


class LoginPO(BaseObj):
    public_path = RootPath.getDevicePlatPath() + "Public.yml"
    request_info = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="接口信息")

    @allure.step("获取token")
    def get_token(self, role):
        """
        wpg账号，租主账号，租户账号
        """
        role_info = PropertiesUtil.loadLocatorValueFromYml(path=self.public_path, key=role)

        url = "http://10.10.15.213:7000" + "/auth/oauth/token"
        body = MultipartEncoder({
            "username": role_info["loginName"],
            "password": role_info["password"],
            "grant_type": "password"
        })
        headers = {"Content-Type": body.content_type, "Authorization": "Basic bWFjaGluZXBsYXRmb3JtOndwZ0AyMDIw"}
        try:
            #response = self.do_post(url=url, params=body,headers=headers)
            response = requests.post(url, data=body,headers=headers)
            response = json.loads(response.content)
            token = response["token_type"].capitalize() + " " + response["access_token"]
            return token
        except Exception as e:
            print("获取token失败")
            print(e)

    @allure.step("组装接口请求header")
    def get_headers(self, role):
        """
        wpg账号，租主账号，租户账号
        """
        headers = self.request_info["headers"]
        token = self.get_token(role=role)
        headers["Authorization"] = token
        return headers


aa = LoginPO().get_token("wpg账号")
print(aa)