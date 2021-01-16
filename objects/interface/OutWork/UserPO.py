# -*- coding: utf-8 -*-
# @Author  : Felix.Ma
# @Time    : 2020/11/9 8:42

from objects.interface.baseObjects.BaseObj import *
from objects.interface.utils.PropertiesUtil import *
from objects.interface.utils.DBRequest import *
from RootPath import *
import allure


class UserPO(BaseObj):
    outwork_path = RootPath.getOutWorkPath() + "Api.yml"
    request_info = PropertiesUtil.loadLocatorValueFromYml(path=outwork_path, key="接口信息")
    db_info = PropertiesUtil.loadLocatorValueFromYml(path=outwork_path, key="db信息")

    @allure.step("获取租户下全部用户")
    def get_all_users(self, headers):
        url = self.request_info["url"] + "/outworkapi/user/allUser"
        response = self.do_get(url=url, headers=headers)
        return response

    @allure.step("获取数据库中的信息")
    def get_db_user(self, dict_sql) -> list:
        """
        根据sql获取数据库的值
        """
        result = db_query(self.db_info["outwork"], dict_sql)
        return result

    @allure.step("根据id查询用户")
    def get_user_by_id(self, headers, userid):
        url = self.request_info["url"] + f"/outworkapi/user/selectUserById/{userid}"
        response = self.do_get(url=url, headers=headers)
        return response

    @allure.step("同步用户")
    def sync_users(self, headers):
        url = self.request_info["url"] + "/outworkapi/user/syncUsers"
        response = self.do_post(url=url, params={}, headers=headers)
        return response
