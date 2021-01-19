# coding=utf-8
# Time : 2020/12/7 16:47
# Author : huxin
from objects.interface.DevicePlat.DsIndustryAlarmPO import DsIndustryAlarmPO
from objects.interface.DevicePlat.LoginPO import LoginPO
from objects.interface.utils.PropertiesUtil import *
from RootPath import *
from objects.interface.utils.DateTimeUtil import *
import allure
import pytest

@allure.feature("行业设备报警对外接口")
class TestDsIndustryAlarm(DsIndustryAlarmPO):

    id = ""
    def setup_class(self):
        self.headers = LoginPO().get_headers(role="wpg账号")

    def teardown_class(self):
        #清空数据
        pass

    @allure.story("查询行业报警列表,查询全部")
    def test_query_DsIndustryAlarm(self):
        body = {
            "applicationSystem": "",
            "createTimeEnd": "",
            "createTimeStart": "",
            "currentPage": 1,
            "delFlag": 0,
            "id": "",
            "keyWord": "",
            "level": "",
            "orderBy": "",
            "pageSize": 10,
            "stationId": "",
            "tenantId": "",
            "type": ""
        }
        result = self.query_DsIndustryAlarm(headers=self.headers,body=body)
        assert result["count"] > 0
        assert len(result["resultData"]) >0

    @allure.story("查询行业报警列表，通过关键字查询")
    def test_query_DsIndustryAlarm_r(self):
        body = {
            "applicationSystem": "",
            "createTimeEnd": "",
            "createTimeStart": "",
            "currentPage": 1,
            "delFlag": 0,
            "id": "",
            "keyWord": "wwwwwwwwwwwww",
            "level": "",
            "orderBy": "",
            "pageSize": 10,
            "stationId": "",
            "tenantId": "",
            "type": ""
        }
        result = self.query_DsIndustryAlarm(headers=self.headers,body=body)
        assert len(result["resultData"]) == 0

    @allure.story("查询行业设备告警详情")
    def test_get_detail_out(self):
        sql = "SELECT id FROM `ds_industry_alarm` limit 1 "
        sql_result = self.get_DB_data(sql=sql)
        id = sql_result[0]["id"]
        result = self.get_detail_out(headers=self.headers,entityId=id)
        assert result["resultData"]["id"] == id

    @allure.story("查询行业设备告警详情，id不存在")
    def test_get_detail_out_r(self):
        id = "wwwwwwwwwwwwwwwwwwwwwwww"
        result = self.get_detail_out(headers=self.headers,entityId=id)
        assert result["resultData"] is None
