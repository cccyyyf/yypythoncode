# coding=utf-8
# Time : 2020/10/11 19:45
# Author : huxin

from objects.interface.DevicePlat.DsPointPO import DsPointPO
from objects.interface.DevicePlat.LoginPO import LoginPO
import allure
import random
import pytest


@allure.feature("监测量库")
class TestDsPoint(DsPointPO, LoginPO):

    def setup_class(self):
        self.headers = LoginPO().get_headers(role="wpg账号")
        self.temp = str(random.randint(1, 10000))
        self.pointCode = "auto" + self.temp
        self.pointCode2 = "auto2" + self.temp

    def teardown_class(self):
        #删除第二个添加的监测量
        sql = "select id from ds_point where point_code = '%s'"% self.pointCode2
        db_res = DsPointPO().get_DB_data(sql=sql)
        response = DsPointPO().delete_point(point_id=db_res[0]["id"],headers=self.headers)

    @allure.story("添加监测量库，只填写必填项")
    def test_add_Point_part(self):
        #判断pointCode在数据库中是否存在，如果存在就先删除
        sql = "select count(*) from ds_point where point_code = '%s'" % self.pointCode
        db_res = self.get_DB_data(sql=sql)
        if db_res[0]["count(*)"] == 1:
            del_sql = "delete from ds_point where point_code = '%s'" % self.pointCode
            del_res = self.get_DB_data(sql=del_sql)

        body = {
            "pointCode": self.pointCode,
            "pointName": "Name" + self.temp,
            "pointMemo": "自动化测试_监测量名称" + self.temp,
            "pointType": "1",
            "dataType": "word"
        }
        response = self.add_point(headers=self.headers, body=body)
        assert response["resultData"] == "新增成功"
        #校验数据库
        db_res2 = self.get_DB_data(sql=sql)
        assert db_res2[0]["count(*)"] == 1

    @allure.story("添加监测量库，参数填全")
    def test_add_Point_all(self):

        #判断pointCode在数据库中是否存在，如果存在就先删除
        sql = "select count(*) from ds_point where point_code = '%s'" % self.pointCode2
        db_res = self.get_DB_data(sql=sql)
        if db_res[0]["count(*)"] == 1:
            del_sql = "delete from ds_point where point_code = '%s'" % self.pointCode2
            del_res = self.get_DB_data(sql=del_sql)

        body = {
            "pointCode": self.pointCode2,
            "pointName": "Name2" + self.temp,
            "pointMemo": "自动化测试_监测量名称2" + self.temp,
            "pointType": "1",
            "dataType": "uint",
            "pointUnit": "Mpa",
            "minValue": 1,
            "maxValue": 3,
            "ratio": 2,
            "dataSort": 5,
            "gatewayFlag": False
        }
        response = self.add_point(headers=self.headers, body=body)
        assert response["resultData"] == "新增成功"
        #校验数据库
        db_res2 = self.get_DB_data(sql=sql)
        assert db_res2[0]["count(*)"] == 1

    @allure.story("添加监测量库，代码唯一性校验")
    def test_add_Point_only(self):

        body = {
            "pointCode": self.pointCode,
            "pointName": "auto" + self.temp,
            "pointMemo": "自动化测试_监测量名称" + self.temp,
            "pointType": "1",
            "dataType": "word"
        }
        response = self.add_point(headers=self.headers, body=body)
        assert "监测量代码已经存在" in response["errorMessage"]

    @allure.story("修改监测量库")
    def test_modify_Point(self):
        #获取监测量库id
        sql = "select id,point_code,point_name,point_memo,point_type,data_type from ds_point where point_code = '%s'"% self.pointCode
        db_res = self.get_DB_data(sql=sql)

        body = {
            "id": db_res[0]["id"],
            "pointCode": self.pointCode,
            "pointName": db_res[0]["point_name"],
            "pointMemo": db_res[0]["point_memo"],
            "pointType": "1",
            "dataType": "word",
            "dataSort": 55
        }
        response = self.modify_point(headers=self.headers,body=body)
        assert response["resultData"] == "修改成功"
        #校验数据库
        sql = "select data_sort from ds_point where point_code = '%s'"% self.pointCode
        db_res = self.get_DB_data(sql=sql)
        assert db_res[0]["data_sort"] == 55

    @allure.story("更新监测量是否为华为网关")
    def test_update_HwGateway(self):
        sql = "select id from ds_point where point_code = '%s'"% self.pointCode
        db_res = self.get_DB_data(sql=sql)
        body = {"entityId": db_res[0]["id"],
                "gatewayFlag": True
        }
        response = self.update_HwGateway(body=body,headers=self.headers)
        assert response["resultData"] == "更新成功"

    @allure.story("查询监测量列表")
    def test_search_point(self):
        body = {"currentPage": 1, "pageSize": 50, "keyword": "auto"}
        response = self.search_point(body=body,headers=self.headers)
        assert response["count"] > 0
        assert "auto" in response["resultData"][0]["pointCode"]

    @allure.story("单个删除监测量库")
    def test_delete_point_single(self):
        #获取监测量库id
        sql = "select id from ds_point where point_code = '%s'"% self.pointCode
        db_res = self.get_DB_data(sql=sql)
        response = self.delete_point(point_id=db_res[0]["id"],headers=self.headers)
        assert response["resultData"] == "删除成功"
        #校验数据
        sql = "select count(*) from ds_point where point_code = '%s'" % self.pointCode
        db_res = self.get_DB_data(sql=sql)
        assert db_res[0]["count(*)"] == 0



