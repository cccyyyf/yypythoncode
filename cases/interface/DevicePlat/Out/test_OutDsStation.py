# coding=utf-8
# Time : 2020/10/21 18:35
# Author : huxin

from objects.interface.DevicePlat.DsStationPO import DsStationPO
from objects.interface.DevicePlat.LoginPO import LoginPO
from objects.interface.utils.PropertiesUtil import *
from RootPath import *
import allure
import pytest


@allure.feature("站点对外接口")
class TestOutDsStation(DsStationPO):

    station_id = ""
    @classmethod
    def setup_class(self):
        self.headers = LoginPO().get_headers(role="wpg账号")
        public_path = RootPath.getDevicePlatPath() + "Public.yml"
        self.staion = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="站点管理")

        #初始化数据，获得area_id
        body = {
            "id": "",
            "areaName": self.staion["areaName"],
            "parentId": "0"
        }
        response = DsStationPO().add_area(headers=self.headers, body=body)
        #获取区域id
        area_id_sql = "SELECT id FROM ds_area where area_name = '%s'"%(self.staion["areaName"])
        id_result = DsStationPO().get_DB_data(sql=area_id_sql)
        self.area_id = id_result[0]["id"]

        #初始化数据，获得station_id
        body ={
            "id": "",
            "stationName": self.staion["stationName"],
            "stationCode": "station01",
            "areaId": self.area_id, #一级区域A
            "shorthand": "pinyinjianxie01",
            "stationType": "PressurePoint",
            "lati": "1",
            "longi": "2",
            "addr": "接口自动化测试地址",
            "labelId": "",
            "remark": ""
        }
        result = DsStationPO().add_station(headers=self.headers,body=body)

        # 获取站点id
        sql_id = "SELECT id FROM ds_station where station_name = '%s'" % (self.staion["stationName"])
        id_result = DsStationPO().get_DB_data(sql=sql_id)
        TestOutDsStation.station_id = id_result[0]["id"]

    def teardown_class(self):
        #删除站点
        result = DsStationPO().dele_station(headers=self.headers,ids=self.station_id)
        #assert result["resultData"] == "删除了站点1条"
        #删除区域
        result2 = DsStationPO().dele_area(headers=self.headers,entityId=self.area_id)

    @allure.story("查询站点信息列表-默认入参")
    def test_queryPage(self):
        body = {
            "areaId": "",
            "currentPage": 1,
            "delFlag": 0,
            "keyword": "",
            "labelId": [],
            "order": "",
            "orderBy": "",
            "pageSize": 10,
            "stationType": "",
            "tenantId": ""
        }
        result = self.query_page(headers=self.headers,body=body)
        assert len(result["resultData"]) >0
        assert result["count"] >0

    @allure.story("查询站点信息列表-按站点类型查询")
    def test_queryPage_r1(self):
        body = {
            "areaId": "",
            "currentPage": 1,
            "delFlag": 0,
            "keyword": "",
            "labelId": [],
            "order": "",
            "orderBy": "",
            "pageSize": 10,
            "stationType": "PressurePoint",
            "tenantId": ""
        }
        result = self.query_page(headers=self.headers,body=body)
        assert result["resultData"][0]["stationTypeName"] == "压力点"

    @allure.story("查询站点信息列表-按站点名称（自动化测试）查询")
    def test_queryPage_r2(self):
        body = {
            "keyword": "自动化测试"
        }
        result = self.query_page(headers=self.headers,body=body)
        assert "自动化测试" in result["resultData"][0]["stationName"]

    @allure.story("查询区域站点混合树-关键字为空")
    def test_query_stationAreaTree(self):
        body = {
            "adminFlag": True,
            "keyword": ""
        }
        result = self.query_page(headers=self.headers,body=body)
        assert len(result["resultData"]) >0

    @allure.story("查询区域站点混合树-关键字为【自动化测试】")
    def test_query_stationAreaTree_r1(self):
        body = {
            "adminFlag": True,
            "keyword": "自动化测试"
        }
        result = self.query_page(headers=self.headers,body=body)
        assert "自动化测试" in result["resultData"][0]["stationName"]

    @allure.story("查询区域站点混合树-adminFlag=false")
    def test_query_stationAreaTree_r2(self):
        body = {
            "adminFlag": False,
            "keyword": "自动化测试"
        }
        result = self.query_page(headers=self.headers,body=body)
        assert "自动化测试" in result["resultData"][0]["stationName"]


    @allure.story("查询站点详情-站点存在")
    def test_query_detail(self):
        #self.headers["Content-Type"] = "application/x-www-form-urlencoded"
        result = self.get_detail(headers=self.headers,id=self.station_id)
        assert result["resultData"]["id"] == self.station_id

    @allure.story("查询站点详情-站点不存在")
    def test_query_detail_r(self):
        #self.headers["Content-Type"] = "application/x-www-form-urlencoded"
        result = self.get_detail(headers=self.headers,id="11111")
        assert result["errorMessage"] == "站点不存在"