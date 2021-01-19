# -*- coding: utf-8 -*-
# @Author  : Felix.Ma
# @Time    : 2020/11/3 17:32

from objects.interface.baseObjects.BaseObj import *
from objects.interface.utils.PropertiesUtil import *
from objects.interface.utils.DBRequest import *
from RootPath import *
import allure


class SysDictPO(BaseObj):
    outwork_path = RootPath.getOutWorkPath() + "Api.yml"
    request_info = PropertiesUtil.loadLocatorValueFromYml(path=outwork_path, key="接口信息")
    db_info = PropertiesUtil.loadLocatorValueFromYml(path=outwork_path, key="db信息")

    @allure.step("获取全部字典")
    def get_all_dict(self, headers):
        url = self.request_info["url"] + "/outworkapi/common/allDict"
        response = self.do_get(url=url, headers=headers)
        return response

    @allure.step("获取数据库中的信息")
    def get_db_dict(self, dict_sql) -> list:
        """
        根据sql获取数据库的值
        """
        result = db_query(self.db_info["outwork"], dict_sql)
        return result

    @allure.step("根据code获取字典")
    def get_dict_by_code(self, headers, sys_dict_code):
        url = self.request_info["url"] + f"/outworkapi/common/getSysDictItemByCode/{sys_dict_code}"
        response = self.do_get(url=url, headers=headers)
        return response
