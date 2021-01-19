# coding=utf-8
# Time : 2020/12/8 19:02
# Author : huxin
from objects.interface.DevicePlat.DsIndustryAccountPO import DsIndustryAccountPO
from objects.interface.DevicePlat.DsIndustryDevicePO import DsIndustryDevicePO
from objects.interface.DevicePlat.LoginPO import LoginPO
from objects.interface.utils.PropertiesUtil import *
from RootPath import *
from objects.interface.utils.DateTimeUtil import *
import allure
import pytest

@allure.feature("设备台账信息")
class TestDsIndustryAccount(DsIndustryAccountPO):

    bussinessId = str(get_time_stamp())
    id_account = ""
    def setup_class(self):
        self.headers = LoginPO().get_headers(role="wpg账号")
        #  获取设备信息
        sql = "select device_name ,device_id from ds_industry_device limit 1"
        sql_result = DsIndustryDevicePO().get_DB_data(sql=sql)
        self.device_name = sql_result[0]["device_name"]
        self.device_id = sql_result[0]["device_id"]

    def teardown_class(self):
        #删除行业设备
        #result = DsIndustryDevicePO().dele_device(headers=self.headers, dsIndustryDeviceId=self.id_standaloned)
        pass

    @allure.story("新增台账信息")
    def test_add_DsIndustryAccount(self):
        body = {
            "bussinessId": self.bussinessId,
            "type": "accMaintainRecord",
            "deviceId": self.device_id,
            "deviceName": self.device_name,
            "accountName": "autotest设备保养",
            "accountType": "accSecDeviceMaintain",
            "happenTime": "2020-12-06 12:00:00",
            "finishTime": "2020-12-07 12:00:00",
            "remark": "",
            "address": "",
            "workorderFlag": "0"
        }
        result = self.add_DsIndustryAccount(headers=self.headers,params=body)
        assert result["success"] == True
        assert result["resultData"]["bussinessId"] == self.bussinessId
        #校验数据库
        sql = "select count(*),id from ds_industry_account where bussiness_id = '%s'" %(self.bussinessId)
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["count(*)"] == 1
        TestDsIndustryAccount.id_account = sql_result[0]["id"]

    @allure.story("修改台账信息")
    def test_modify_DsIndustryAccount(self):
        body = {
            "bussinessId": self.bussinessId,
            "type": "accMaintainRecord",
            "deviceId": self.device_id,
            "deviceName": self.device_name,
            "accountName": "autotest设备保养",
            "accountType": "accSecDeviceMaintain",
            "happenTime": "2020-12-06 12:00:00",
            "finishTime": "2020-12-07 12:00:00",
            "remark": "TESTremark",
            "address": "",
            "workorderFlag": "0"
        }
        result = self.modify_DsIndustryAccount(headers=self.headers,params=body)
        assert result["success"] == True
        assert result["resultData"] == "修改成功"
        #校验数据库
        sql = "select remark from ds_industry_account where bussiness_id = '%s'" %(self.bussinessId)
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["remark"] == "TESTremark"

    @allure.story("查询台账详情")
    def test_get_DsIndustryAccount(self):
        result = self.get_DsIndustryAccount(headers=self.headers,entityId=self.id_account)
        assert result["success"] == True
        assert result["resultData"]["accountName"] == "autotest设备保养"

    @allure.story("查询台账列表")
    def test_get_list(self):
        body = {
            "keyWord": self.device_name,
            "labelId": "",
            "stationIds": "",
            "happenStartTime": "",
            "happenEndTime": "",
            "currentPage": 1,
            "pageSize": 20
        }
        result = self.get_list(headers=self.headers,params=body)
        assert result["count"] > 0
        assert result["resultData"][0]["accountName"] == "autotest设备保养"

    @allure.story("excel导出")
    def test_export_excel(self):
        body = {"keyWord":"","labelId":"","stationIds":"","happenStartTime":"","happenEndTime":"","currentPage":1,"pageSize":20}
        result = self.export_excel(headers=self.headers,params=body)

    @allure.story("删除台账信息")
    def test_dele_DsIndustryAccount(self):
        result = self.dele_DsIndustryAccount(headers=self.headers,bussinessId=self.bussinessId)
        assert result["resultData"] == "删除成功"
        #校验数据库
        sql = "select count(*) from ds_industry_account where bussiness_id = '%s'" %(self.bussinessId)
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["count(*)"] == 0


