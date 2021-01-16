# -*- coding: utf-8 -*-
# @Author  : Felix.Ma
# @Time    : 2020/11/9 9:36

from objects.interface.baseObjects.BaseObj import *
from objects.interface.utils.PropertiesUtil import *
from objects.interface.utils.DBRequest import *
from RootPath import *
import allure


class MenuPO(BaseObj):
    outwork_path = RootPath.getOutWorkPath() + "Api.yml"
    request_info = PropertiesUtil.loadLocatorValueFromYml(path=outwork_path, key="接口信息")
    db_info = PropertiesUtil.loadLocatorValueFromYml(path=outwork_path, key="db信息")

    @allure.step("获取菜单")
    def get_menus(self, headers, params):
        url = self.request_info["url"] + "/outworkapi/sysmenuClient/sysmenu/list"
        response = self.do_post(url=url, params=params, headers=headers)
        return response

    @allure.step("获取数据库中的信息")
    def get_db_menu(self, dict_sql) -> list:
        """
        根据sql获取数据库的值
        """
        result = db_query(self.db_info["outwork"], dict_sql)
        return result
