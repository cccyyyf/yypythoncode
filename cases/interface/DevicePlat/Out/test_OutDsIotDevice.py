# coding=utf-8
# Time : 2020/12/11 14:19
# Author : huxin
from objects.interface.DevicePlat.DsIotDevicePO import DsIotDevicePO
from objects.interface.DevicePlat.DsIotTemplatePO import DsIotTemplatePO
from objects.interface.DevicePlat.LoginPO import LoginPO
from objects.interface.utils.DateTimeUtil import *
import allure
import pytest


@allure.feature("Iot设备信息对外接口")
class TestOutDsIotDevice(DsIotDevicePO):


    def setup_class(self):
        self.headers = LoginPO().get_headers(role="wpg账号")

        #获取iot设备
        sql = "select id,device_id,device_name from ds_iot_device ORDER BY id desc limit 1"
        sql_result = DsIotDevicePO().get_DB_data(sql=sql)
        self.deviceId = sql_result[0]["device_id"]
        self.deviceName =sql_result[0]["device_name"]

    def teardown_class(self):
        pass


    @allure.story("获取设备详情")
    def test_get_detailAllByDeviceId(self):
        result = self.get_detailAllByDeviceId(headers=self.headers,deviceId=self.deviceId)
        assert result["success"] == True
        assert result["resultData"]["detail"]["deviceName"] == self.deviceName

    @allure.story("查询设备列表,特定设备")
    def test_get_devicePageList(self):
        params = {
            "areaId": "",
            "collectorType": "",
            "currentPage": 1,
            "isSelectAttribute": True,
            "keyWord": self.deviceName,
            "labelId": [],
            "orderBy": "",
            "pageSize": 10,
            "stationId": "",
            "templateType": ""
        }
        result = self.get_devicePageList(headers=self.headers,params=params)
        assert result["success"] == True
        assert result["count"] > 0
        assert self.deviceName in result["resultData"][0]["deviceName"]

    @allure.story("查询设备列表,全量")
    def test_get_devicePageList_r(self):
        params = {
            "areaId": "",
            "collectorType": "",
            "currentPage": 1,
            "isSelectAttribute": True,
            "keyWord": "",
            "labelId": [],
            "orderBy": "",
            "pageSize": 10,
            "stationId": "",
            "templateType": ""
        }
        result = self.get_devicePageList(headers=self.headers,params=params)
        assert result["success"] == True
        assert result["count"] > 0
        assert len(result["resultData"]) > 0

    @allure.story("获取设备监测量")
    def test_get_devicePointList(self):
        result = self.get_devicePointList(headers=self.headers,deviceId=self.deviceId)
        assert result["success"] == True
        assert result["count"] > 0
        assert len(result["resultData"]) > 0

    @allure.story("获取设备实时数据")
    def test_get_deviceRealTimeData(self):
        result = self.get_deviceRealTimeData(headers=self.headers,deviceId=self.deviceId)
        assert result["success"] == True

