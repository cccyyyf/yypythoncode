# -*- coding: utf-8 -*-
# @Author  : Felix.Ma
# @Time    : 2021/1/6 9:04

from objects.interface.baseObjects.BaseObj import *
from objects.interface.utils.Decorators import post
from objects.interface.utils.PropertiesUtil import *
from objects.interface.utils.DBRequest import *
from RootPath import *
import allure


class PumpHousePO(BaseObj):
    public_path = RootPath.getErGongPath() + "Public.yml"
    request_info = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="接口信息")
    DB_info = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="DB信息")

    @allure.step("首页泵房运行信息返回动态配置信息数据")
    @post(request_info["url"] + "/pumpHouse/pumpRunInfo")
    def pump_run_info(self, headers, params):
        pass

    @allure.step("获取数据库中的信息")
    def get_db_dict(self, dict_sql) -> list:
        """
        根据sql获取数据库的值
        """
        result = db_query(self.DB_info["devicecenter"], dict_sql)
        return result
