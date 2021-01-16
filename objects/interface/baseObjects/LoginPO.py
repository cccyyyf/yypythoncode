# coding=utf-8
# Time : 2020/10/11 19:43
# Author : huxin

from objects.interface.baseObjects.BaseObj import *
from objects.interface.utils.PropertiesUtil import *
from RootPath import *
import allure


class LoginPO(BaseObj):

    @allure.step("获取接口信息")
    def get_request_info(self, par_dir, yml_name):
        """

        Args:
            par_dir: 类似"resources/interface/OutWork/"
            yml_name: "Api.yml"

        Returns: tuple

        """
        public_path = RootPath.getPath(par_dir) + yml_name
        request_info = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="接口信息")
        return public_path, request_info

    @allure.step("获取token")
    def get_token(self, role, par_dir, yml_name, login_api_url):
        """

        Args:
            role: wpg账号，租主账号，租户账号
            par_dir: 类似"resources/interface/OutWork/"
            yml_name: "Api.yml"
            login_api_url: "/outworkapi/sso/login"

        Returns: token

        """
        public_path, request_info = self.get_request_info(par_dir, yml_name)
        role_info = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key=role)
        url = request_info["url"] + login_api_url
        body = {
            "loginName": role_info["loginName"],
            "loginToken": "",
            "password": role_info["password"],
            "tenantName": ""
        }
        try:
            response = self.do_post(url=url, params=body)
            token = response["resultData"]["token"]
            return token
        except Exception as e:
            print("获取token失败")
            print(e)

    @allure.step("组装接口请求header")
    def get_headers(self, role, par_dir, yml_name, login_api_url):
        """

        Args:
            role: wpg账号，租主账号，租户账号
            par_dir: 类似"resources/interface/OutWork/"
            yml_name: "Api.yml"
            login_api_url: "/outworkapi/sso/login"

        Returns: 带token的headers

        """
        _, request_info = self.get_request_info(par_dir, yml_name)
        headers = request_info["headers"]
        token = self.get_token(role, par_dir, yml_name, login_api_url)
        headers["Authorization"] = token
        return headers
