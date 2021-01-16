# coding=utf-8
# Time : 2020/12/4 15:47
# Author : huxin
from objects.interface.DevicePlat.DsIotDevicePO import DsIotDevicePO
from objects.interface.DevicePlat.LoginPO import LoginPO
from objects.interface.DevicePlat.DsInterUserPO import DsInterUserPO
from objects.interface.utils.PropertiesUtil import *
from RootPath import *
import allure
import pytest
import time

@allure.feature("接口用户管理")
class TestDsInterUser(DsInterUserPO):

    id = ""
    def setup_class(self):
        self.headers = LoginPO().get_headers(role="wpg账号")
        public_path = RootPath.getDevicePlatPath() + "Public.yml"
        self.userInfo = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="接口用户管理")
        #获取iot设备信息
        sql = "select id,device_id,device_name from ds_iot_device  WHERE create_name = 'Admin' ORDER BY create_time desc limit 1"
        sql_result = DsIotDevicePO().get_DB_data(sql=sql)
        self.deviceId = sql_result[0]["device_id"]
        self.deviceName =sql_result[0]["device_name"]
        #清除遗留
        sql = "delete from ds_inter_user WHERE login_name like '%Auto%'"
        result = DsInterUserPO().get_DB_data(sql=sql)

    def teardown_class(self):
        pass

    @allure.story("新增接口用户")
    def test_add_InterUser(self):
        body = {
            "id": "",
            "loginName": self.userInfo["username"],
            "password": self.userInfo["passwd"],
            "userType": "manufacturer",
            "phone": "",
            "email": self.userInfo["email"],
            "notification": 0,
            "remark": "",
            "deviceId": [self.deviceId]
        }
        result = self.add_InterUser(headers=self.headers,body=body)
        assert result["resultData"] == "添加成功"
        #数据库校验
        sql = "select count(*),id from ds_inter_user where login_name = '%s'" %(self.userInfo["username"])
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["count(*)"] > 0
        #获取用户id
        TestDsInterUser.id = sql_result[0]["id"]

    @allure.story("修改接口用户")
    def test_update_InterUser(self):
        body = {
            "id": self.id,
            "loginName": self.userInfo["username"],
            "password": "",
            "userType": "manufacturer",
            "phone": "",
            "email": self.userInfo["NEWemail"],
            "notification": 0,
            "remark": "",
            "deviceId": [self.deviceId]
        }
        result = self.update_InterUser(headers=self.headers,body=body)
        assert result["resultData"] == "修改成功"
        # 数据库校验
        sql = "select email from ds_inter_user where id = '%s'"%(self.id)
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["email"] == self.userInfo["NEWemail"]

    @allure.story("查看接口用户详情")
    def test_get_details(self):
        result = self.get_details(headers=self.headers,entityId=self.id)
        assert result["resultData"]["email"] == self.userInfo["NEWemail"]
        assert len(result["resultData"]["deviceId"]) > 0

    @allure.story("查询接口用户列表")
    def test_get_list(self):
        body={"currentPage":1,"delFlag":0,"keyword":"","order":"desc","orderBy":"createTime","pageSize":20,"tenantId":"","userType":[]}
        result = self.get_list(headers=self.headers,body=body)
        assert result["count"] > 0
        assert len(result["resultData"]) > 0

    @allure.story("接口用户重置密码")
    def test_reset_passwd(self):
        result = self.reset_passwd(headers=self.headers,userId=self.id)
        assert result["success"] == True

    @allure.story("删除接口用户")
    def test_dele_InterUser(self):

        result = self.dele_InterUser(headers=self.headers,userId=self.id)
        assert result["resultData"] == "删除成功"
        #校验数据库
        sql = "select count(*) from ds_inter_user where id = '%s'" %(self.id)
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["count(*)"] == 0


