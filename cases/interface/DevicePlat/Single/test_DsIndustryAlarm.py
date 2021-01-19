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

@allure.feature("行业设备报警")
class TestDsIndustryAlarm(DsIndustryAlarmPO):

    id = ""
    alarmTitle = "autoTest" + str(get_time_stamp())
    def setup_class(self):
        self.headers = LoginPO().get_headers(role="wpg账号")
        #获取行业设备信息
        sql = "select device_name,device_id from ds_industry_device limit 1 "
        sql_result = DsIndustryAlarmPO().get_DB_data(sql=sql)
        self.deviceId = sql_result[0]["device_id"]
        self.deviceName = sql_result[0]["device_name"]

    def teardown_class(self):
        #清空数据
        pass

    @allure.story("新增行业设备报警")
    def test_add_DsIndustryAlarm(self):
        body = {
            "id": "",
            "deviceId": self.deviceId,
            "deviceName": self.deviceName,
            "systemSource": "Dd_managment",
            "alarmTime": "2020-12-13 16:59:18",
            "alarmTitle": self.alarmTitle,
            "alarmLevel": "alarm_message",
            "alarmType": "	point_value",
            "alarmContent": "报警content",
            "workorderNo": "0",
            "workorderType": "",
            "workorderMsg": ""
}
        result = self.add_DsIndustryAlarm(headers=self.headers,body=body)
        assert result["success"] == True
        assert result["resultData"] == "添加成功"
        #校验数据库
        sql = "SELECT count(*),id FROM `ds_industry_alarm` where alarm_title = '%s'" %(self.alarmTitle)
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["count(*)"] == 1
        TestDsIndustryAlarm.id = sql_result[0]["id"]

    @allure.story("查询行业报警列表,查询全部")
    def test_query_list(self):
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
        result = self.query_list(headers=self.headers,body=body)
        assert result["count"] > 0
        assert len(result["resultData"]) >0

    @allure.story("查询行业报警列表，通过关键字查询")
    def test_query_list_r(self):
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
        result = self.query_list(headers=self.headers,body=body)
        assert len(result["resultData"]) == 0

    @allure.story("查询行业设备告警详情")
    def test_get_details(self):

        result = self.get_details(headers=self.headers,entityId=self.id)
        assert result["resultData"]["id"] == self.id

    @allure.story("根据ID删除报警信息")
    def test_removes(self):
        result = self.dele_DsIndustryAlarm(headers=self.headers,entityId=self.id)
        assert result["resultData"] == "删除成功"
        #校验数据库
        sql = "SELECT count(*),id FROM `ds_industry_alarm` where alarm_title = '%s'" %(self.alarmTitle)
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["count(*)"] == 0

