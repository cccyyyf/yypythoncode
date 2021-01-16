# -*- coding: utf-8 -*-
# @Author  : Felix.Ma
# @Time    : 2021/1/7 10:28

from objects.interface.baseObjects.BaseObj import *
from objects.interface.utils.Decorators import post
from objects.interface.utils.PropertiesUtil import *
from objects.interface.utils.DBRequest import *
from objects.interface.utils.RedisUtil import Redis
from RootPath import *
import allure


class RealDataPO(BaseObj):
    public_path = RootPath.getErGongPath() + "Public.yml"
    request_info = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="接口信息")
    DB_info = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="DB信息")
    redis_info = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="redis信息")

    @allure.step("获取数据库中的信息")
    def get_db_dict(self, dict_sql) -> list:
        """
        根据sql获取数据库的值
        """
        result = db_query(self.DB_info["devicecenter"], dict_sql)
        return result

    @allure.step("获取redis的信息")
    def get_redis(self, name, key):
        """
        根据name, key获取redis的值
        """
        result = Redis.get_value(self.redis_info["redis"], name, key)
        return result

    @allure.step("实时数据列表")
    @post(request_info["url"] + "/realData/list")
    def get_list(self, headers, params):
        pass

    @allure.step("模拟量实时数据列表")
    @post(request_info["url"] + "/realData/realList")
    def get_real_list(self, headers, params):
        pass

    @allure.step("单测点实时数据")
    @post(request_info["url"] + "/realData/onePotintRealData")
    def get_onepoint_realdata(self, headers, params):
        pass
