# -*- coding: utf-8 -*-
# @Author  : Felix.Ma
# @Time    : 2020/11/20 17:03

from objects.interface.baseObjects.BaseObj import *
from objects.interface.utils.PropertiesUtil import *
from objects.interface.utils.DBRequest import *
from RootPath import *
import allure


class FormPO(BaseObj):
    outwork_path = RootPath.getOutWorkPath() + "Api.yml"
    request_info = PropertiesUtil.loadLocatorValueFromYml(path=outwork_path, key="接口信息")
    db_info = PropertiesUtil.loadLocatorValueFromYml(path=outwork_path, key="db信息")

    @allure.step("新增表单")
    def add_form(self, params, headers):
        url = self.request_info["url"] + "/outworkapi/form/addOrUpdateBasicForm"
        response = self.do_post(url=url, params=params, headers=headers)
        return response

    @allure.step("获取数据库中的信息")
    def get_db_dict(self, dict_sql) -> list:
        """
        根据sql获取数据库的值
        """
        result = db_query(self.db_info["outwork"], dict_sql)
        return result
