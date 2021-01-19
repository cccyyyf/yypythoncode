from objects.interface.baseObjects.BaseObj import *
from objects.interface.utils.PropertiesUtil import *
from RootPath import *
import allure


class SynUserInfoPO(BaseObj):
    public_path = RootPath.getErGongPath() + "Public.yml"
    request_info = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="接口信息")

    @allure.step("登录")
    def login(self,headers,body):
        # http://119.3.37.131:8080/waterApi/sso/login
        url = self.request_info["url"] + "/sso/login"
        result = self.do_post(url=url,headers=headers,params=body)
        return result

    def getHeader(self):
        header =self.request_info["headers"]
        return header

    def login(self,role):
        role_info = PropertiesUtil.loadLocatorValueFromYml(path=self.public_path, key=role)
        url = self.request_info["url"] + "/sso/login"
        body = {
            "loginName": role_info["loginName"],
            "password": role_info["password"]
        }
        try:
            response = self.do_post(url=url, params=body)
            token = response["resultData"]["token"]
            return token
        except Exception as e:
            print("登录失败，获取token失败")
            print(e)

    def getTokenHeader(self):
        headers =self.request_info["headers"]
        token = self.getToken(self,"root账号")
        headers["Authorization"] = token
        return headers