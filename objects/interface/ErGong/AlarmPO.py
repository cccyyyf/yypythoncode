# -*- coding: utf-8 -*-
# @Author  : Felix.Ma
# @Time    : 2021/1/5 17:12

from objects.interface.baseObjects.BaseObj import *
from objects.interface.utils.PropertiesUtil import *
from objects.interface.utils.DBRequest import *
from RootPath import *
import allure


class AlarmPO(BaseObj):
    public_path = RootPath.getErGongPath() + "Public.yml"
    request_info = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="接口信息")
    DB_info = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="DB信息")

    @allure.step("查询当前报警数")
    def get_index_alarm_count(self, headers):
        url = self.request_info["url"] + "/alarm/indexAlarmCount"
        response = self.do_get(url=url, headers=headers)
        return response

    @allure.step("获取数据库中的信息")
    def get_db_dict(self, dict_sql) -> list:
        """
        根据sql获取数据库的值
        """
        result = db_query(self.DB_info["devicecenter"], dict_sql)
        return result