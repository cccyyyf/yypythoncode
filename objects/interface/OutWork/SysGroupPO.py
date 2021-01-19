# -*- coding: utf-8 -*-
# @Author  : Felix.Ma
# @Time    : 2020/11/11 11:26

from objects.interface.baseObjects.BaseObj import *
from objects.interface.utils.PropertiesUtil import *
from objects.interface.utils.DBRequest import *
from RootPath import *
import allure


class SysGroupPO(BaseObj):
    outwork_path = RootPath.getOutWorkPath() + "Api.yml"
    request_info = PropertiesUtil.loadLocatorValueFromYml(path=outwork_path, key="接口信息")
    db_info = PropertiesUtil.loadLocatorValueFromYml(path=outwork_path, key="db信息")

    @allure.step("新增群组")
    def add_group(self, params, headers):
        url = self.request_info["url"] + "/outworkapi/sysGroup/add"
        response = self.do_post(url=url, params=params, headers=headers)
        return response

    @allure.step("获取数据库中的信息")
    def get_db_dict(self, dict_sql) -> list:
        """
        根据sql获取数据库的值
        """
        result = db_query(self.db_info["outwork"], dict_sql)
        return result

    @allure.step("分页查询")
    def query_group(self, params, headers):
        url = self.request_info["url"] + "/outworkapi/sysGroup/selectSysGroupPage"
        response = self.do_post(url=url, params=params, headers=headers)
        return response

    @allure.step("新增用户")
    def add_user(self, params, headers):
        url = self.request_info["url"] + "/outworkapi/sysGroup/addUser"
        response = self.do_put(url=url, params=params, headers=headers)
        return response
