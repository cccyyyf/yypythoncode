# coding=utf-8
# Time : 2020/12/8 15:34
# Author : huxin
from RootPath import RootPath
from objects.interface.DevicePlat.DsIndustryDevicePO import DsIndustryDevicePO
from objects.interface.DevicePlat.LoginPO import LoginPO
import allure
import pytest
from objects.interface.utils.PropertiesUtil import *


@allure.feature("行业设备信息对外接口")
class TestOutDsIndustryDevice(DsIndustryDevicePO):

    id_standaloned = ""

    def setup_class(self):
        self.headers = LoginPO().get_headers(role="wpg账号")
        public_path = RootPath.getDevicePlatPath() + "Public.yml"
        self.deviceInfo = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="行业设备信息")

        #  获取设备信息
        sql = "select device_name ,device_id,id from ds_industry_device order by create_time desc limit 1"
        sql_result = DsIndustryDevicePO().get_DB_data(sql=sql)
        self.device_name = sql_result[0]["device_name"]
        self.device_id = sql_result[0]["device_id"]
        TestOutDsIndustryDevice.id_standaloned = sql_result[0]["id"]

    def teardown_class(self):
        #删除行业设备
        result = DsIndustryDevicePO().dele_device(headers=self.headers,dsIndustryDeviceId=self.id_standaloned)

    @allure.story("根据行业设备编号查详情,有数据")
    def test_get_ByIndustryDeviceId(self):
        result = self.get_ByIndustryDeviceId(headers=self.headers,industryDeviceId=self.device_id)
        assert result["resultData"]["industryDeviceVO"]["deviceId"] == self.device_id
        assert result["success"] == True

    @allure.story("根据行业设备编号查详情,无数据")
    def test_get_ByIndustryDeviceId_r(self):
        result = self.get_ByIndustryDeviceId(headers=self.headers,industryDeviceId="aaaaaaaaaaa")
        assert len(result["resultData"]) == 0
        assert result["success"] == True

    @allure.story("根据行业设备编号查询关联的设备测点,有数据")
    def test_get_DevicePointByIndustryDeviceId(self):
        result = self.get_DevicePointByIndustryDeviceId(headers=self.headers,industryDeviceId=self.device_id)
        assert len(result["resultData"]) > 0
        assert result["success"] == True

    @allure.story("根据行业设备编号查询关联的设备测点，无数据")
    def test_get_DevicePointByIndustryDeviceId_r(self):
        result = self.get_DevicePointByIndustryDeviceId(headers=self.headers,industryDeviceId="aaaaaaaaaaaaa")
        assert len(result["resultData"]) == 0
        assert result["success"] == True

    @allure.story("根据行业设备查询关联的设备测点")
    def test_get_DevicePointByIndustryId(self):
        result = self.get_DevicePointByIndustryDeviceId(headers=self.headers,industryDeviceId=self.device_id)
        assert len(result["resultData"]) > 0
        assert result["success"] == True

    @allure.story("根据行业设备id查详情")
    def test_get_IndustryDetail(self):
        result = self.get_IndustryDetail(headers=self.headers,industryId=self.id_standaloned)
        assert result["resultData"]["industryDeviceVO"]["id"] == self.id_standaloned
        assert result["success"] == True

    @allure.story("根据行业设备id查详情,设备不存在")
    def test_get_IndustryDetail_r(self):
        result = self.get_IndustryDetail(headers=self.headers, industryId="wwwwwwwwwwwwwwwww")
        assert result["errorMessage"] == "查详情时，找不到行业设备"
        assert result["success"] == False

    @allure.story("用测点名过滤实时数据,设备id为空")
    def test_query_RealTimeDataSearch(self):
        body= {
            "industryId": "",
            "keyWord": ""
        }
        result = self.query_RealTimeDataSearch(headers=self.headers,params=body)
        assert result["errorMessage"] == "行业设备id不能为空"

    @allure.story("用测点名过滤实时数据,查询所有")
    def test_query_RealTimeDataSearch_r1(self):
        body= {
            "industryId": self.id_standaloned,
            "keyWord": ""
        }
        result = self.query_RealTimeDataSearch(headers=self.headers,params=body)
        assert result["success"] == True

    @allure.story("用测点名过滤实时数据,设备编号为空")
    def test_query_RealTimeDataSearchByCode(self):
        body= {
            "industryDeviceId": "",
            "keyWord": ""
        }
        result = self.query_RealTimeDataSearchByCode(headers=self.headers,params=body)
        assert result["errorMessage"] == "行业设备编号不能为空"

    @allure.story("用测点名过滤实时数据,查询所有")
    def test_query_RealTimeDataSearchByCode_r1(self):
        body= {
            "industryDeviceId": self.device_id,
            "keyWord": ""
        }
        result = self.query_RealTimeDataSearchByCode(headers=self.headers,params=body)
        assert result["success"] == True

    @allure.story("根据条件查询行业设备信息列表")
    def test_select_IndustryList(self):
        body = {
            "areaId": "",
            "areaIds": "",
            "currentPage": 1,
            "delFlag": 0,
            "id": "",
            "ids": [],
            "isSelectAttribute": True,
            "keyWord": "",
            "labelId": "",
            "orderBy": "",
            "pageSize": 10,
            "stationId": "",
            "stationIds": "",
            "deviceType": ""
        }
        result = self.select_IndustryList(headers=self.headers,params=body)
        assert result["count"] > 0
        assert len(result["resultData"]) > 0