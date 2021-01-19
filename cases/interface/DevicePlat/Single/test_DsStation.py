# coding=utf-8
# Time : 2020/10/21 18:35
# Author : huxin

from objects.interface.DevicePlat.DsStationPO import DsStationPO
from objects.interface.DevicePlat.LoginPO import LoginPO
from objects.interface.utils.PropertiesUtil import *
from RootPath import *
import allure
import pytest
import random


@allure.feature("站点管理")
class TestDsStation(DsStationPO):

    area_id = ""
    station_id = ""
    def setup_class(self):
        self.headers = LoginPO().get_headers(role="wpg账号")
        public_path = RootPath.getDevicePlatPath() + "Public.yml"
        #self.staion = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="站点管理")
        self.temp = str(random.randint(1,10000))
        self.areaName = "AutoAreaName" + self.temp
        self.areaName_new = "AutoAreaNameNew" + self.temp
        self.stationName = "站点名称接口自动化测试" + self.temp
        self.stationName_new = "站点名称接口自动化测试New" + self.temp
        self.stationCode = "AutoCode" + str(random.randint(1,99))
        self.shorthand = "AutoPin" + str(random.randint(1,99))

    def teardown_class(self):
        pass

    @allure.story("添加根区域")
    def test_add_area(self):

        body = {
            "id": "",
            "areaName": self.areaName,
            "parentId": "0"
        }
        response = self.add_area(headers=self.headers, body=body)
        assert response["success"]==True
        #校验数据库
        sql = "SELECT count(*) FROM ds_area where area_name = '%s'"%(self.areaName)
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["count(*)"] == 1

    @allure.story("修改根区域")
    def test_modify_area(self):
        #获取区域id
        area_id_sql = "SELECT id FROM ds_area where area_name = '%s'"%(self.areaName)
        id_result = self.get_DB_data(sql=area_id_sql)
        TestDsStation.area_id = id_result[0]["id"]

        body= {
            "id": self.area_id,
            "areaName": self.areaName_new,
            "parentId": "0"
        }
        response = self.modify_area(headers=self.headers, body=body)
        assert response["resultData"] == "修改成功"

        #校验数据库
        sql = "SELECT area_name FROM ds_area where id = '%s'"%(self.area_id)
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["area_name"] == self.areaName_new

    @allure.story("查询区域")
    def test_search_area(self):
        body = {"keyword": self.areaName_new}
        result = self.search_area(headers=self.headers,body=body)
        assert result["resultData"][0]["name"] == self.areaName_new

    @allure.story("新建站点")
    def test_add_station(self):
        body = {
            "id": "",
            "stationName": self.stationName,
            "stationCode": self.stationCode,
            "areaId": self.area_id,
            "shorthand": self.shorthand,
            "stationType": "PressurePoint",
            "lati": "1",
            "longi": "2",
            "addr": "接口自动化测试地址",
            "labelId": "",
            "remark": ""
        }
        result = self.add_station(headers=self.headers,body=body)
        assert result["success"] == True

        #校验数据库
        sql = "SELECT count(*),id FROM ds_station where station_name = '%s'"%(self.stationName)
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["count(*)"] > 0
        #获取站点id
        TestDsStation.station_id = sql_result[0]["id"]

    @allure.story("修改站点信息")
    def test_modify_station(self):
        body = {
            "id": self.station_id,
            "stationName": self.stationName_new,
            "stationCode": self.stationCode,
            "areaId": self.area_id,
            "shorthand": self.shorthand,
            "stationType": "PressurePoint",
            "lati": "1",
            "longi": "2",
            "addr": "接口自动化测试地址New",
            "labelId": "",
            "remark": ""
        }
        result = self.modify_station(headers=self.headers,body=body)
        assert result["success"] == True

        #校验数据库
        sql = "SELECT station_name FROM ds_station where station_name = '%s'"%(self.stationName_new)
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["station_name"] == self.stationName_new

    @allure.story("通过关键字查询站点")
    def test_search_station(self):
        body={
            "areaId": "",
            "keyword": self.stationName_new,
            "labelId": ""
        }
        result = self.search_station(headers=self.headers,body=body)
        assert result["resultData"][0]["stationName"] == self.stationName_new


    @allure.story("查询区域站点树")
    def test_search_area_station(self):
        body={"keyword":"New","adminFlag":False}
        result = self.search_area_station(headers=self.headers,body=body)
        assert len(result["resultData"]) > 0


    @allure.story("获取角色")
    def test_get_role(self):
        headers_x = self.headers.copy()  #注意此处用法
        headers_x["Content-Type"] = "application/x-www-form-urlencoded"
        result = self.get_role_list(headers=headers_x)
        assert len(result["resultData"]) > 0

    @allure.story("用户分配站点")
    def test_user_stations(self):
        body = {
            "stationId": [self.station_id],
            "userId": "de51caa1c6b9b10f32cf79608d095d7b" #wpg用户user0003
        }
        result = self.relate_user_stations(headers=self.headers,body=body)
        assert result["success"] == True
        assert result["count"] == 0

        #校验数据库

    @allure.story("导出站点")
    def test_dexport_excel(self):
        body = [self.station_id]
        result = self.export_excel(headers=self.headers,body=body)

    @allure.story("删除站点")
    def test_dele_stations(self):
        result = self.dele_station(headers=self.headers,ids=self.station_id)
        assert result["resultData"] == "删除了站点1条"

        #校验数据库
        sql = "SELECT count(*) FROM ds_station where id = '%s'"%(self.station_id)
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["count(*)"] == 0

    @allure.story("删除区域")
    def test_dele_area(self):
        result = self.dele_area(headers=self.headers,entityId=self.area_id)
        assert result["resultData"] == "删除成功"

        #校验数据库
        sql = "SELECT count(*) FROM ds_area where id = '%s'"%(self.area_id)
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["count(*)"] == 0