# coding=utf-8
# Time : 2020/10/21 18:35
# Author : huxin

from objects.interface.DevicePlat.DsStationPO import DsStationPO
from objects.interface.DevicePlat.LoginPO import LoginPO
from objects.interface.utils.PropertiesUtil import *
from RootPath import *
import allure
import pytest


@allure.feature("区域对外接口")
class TestOutDsArea(DsStationPO):

    area_id = ""
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
        TestOutDsArea.area_id = id_result[0]["id"]

    def teardown_class(self):
        #删除区域
        result = DsStationPO().dele_area(headers=self.headers,entityId=self.area_id)

    @allure.story("查询区域-关键字为空")
    def test_query_AreaTree(self):
        body = {
            "keyword": ""
        }
        result = self.get_tree(headers=self.headers,body=body)
        assert len(result["resultData"]) >0

    @allure.story("查询区域站-关键字为【testAAA】")
    def test_query_AreaTree_r1(self):
        body = {
            "keyword": self.staion["areaName"]
        }
        result = self.get_tree(headers=self.headers,body=body)
        assert "Test" in result["resultData"][0]["name"]

    @allure.story("查询区域-关键字为【随便填写的关键字】")
    def test_query_AreaTree_r2(self):
        body = {
            "keyword": "随便填写的关键字"
        }
        result = self.get_tree(headers=self.headers,body=body)
        assert len(result["resultData"]) == 0

