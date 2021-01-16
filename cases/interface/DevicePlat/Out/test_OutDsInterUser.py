# coding=utf-8
# Time : 2020/12/5 12:47
# Author : huxin
from objects.interface.DevicePlat.DsIotDevicePO import DsIotDevicePO
from objects.interface.DevicePlat.LoginPO import LoginPO
from objects.interface.DevicePlat.DsInterUserPO import DsInterUserPO
from objects.interface.utils.PropertiesUtil import *
from RootPath import *
import allure
import pytest

@allure.feature("接口用户管理对外接口")
class TestOutDsInterUser(DsInterUserPO):
    id=""
    token=""
    headers ={"Content-Type":"application/json"}
    header_set=""
    def setup_class(self):
        public_path = RootPath.getDevicePlatPath() + "Public.yml"
        TestOutDsInterUser.header_set = LoginPO().get_headers(role="wpg账号")
        self.userInfo = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="接口用户管理")

        #获取iot设备信息
        sql = "select id,device_id,device_name from ds_iot_device  WHERE create_name = 'Admin' and more_flag =0 ORDER BY create_time desc limit 1"
        sql_result = DsIotDevicePO().get_DB_data(sql=sql)
        self.deviceId = sql_result[0]["device_id"]
        self.deviceName =sql_result[0]["device_name"]
        #清除遗留
        sql = "delete from ds_inter_user WHERE login_name like '%Auto%'"
        result = DsInterUserPO().get_DB_data(sql=sql)
        #新增接口用户
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
        result = DsInterUserPO().add_InterUser(headers=self.header_set,body=body)
        #获取用户id
        sql = "select count(*),id from ds_inter_user where login_name = '%s'" %(self.userInfo["username"])
        sql_result = DsInterUserPO().get_DB_data(sql=sql)
        TestOutDsInterUser.id = sql_result[0]["id"]

    def teardown_class(self):
        #删除接口用户
        result = DsInterUserPO().dele_InterUser(headers=self.header_set, userId=self.id)
        #pass

    @allure.story("登录,正常登录")
    def test_user_login(self):
        body = {
            "loginName": self.userInfo["username"],
            "password": self.userInfo["passwd"],
            "tenantId": "001"
        }
        result = self.user_login(headers=self.headers,body=body)
        assert result["resultData"]["token"] is not None
        TestOutDsInterUser.token = result["resultData"]["token"]
        TestOutDsInterUser.headers["Authorization"] = result["resultData"]["token"]

    @allure.story("登录,用户名不存在")
    def test_user_login_r1(self):
        body = {
            "loginName": "aaaaa",
            "password": self.userInfo["passwd"],
            "tenantId": "001"
        }
        result = self.user_login(headers=self.headers,body=body)
        assert result["resultData"] is None
        assert result["errorMessage"] == "用户不存在"

    @allure.story("登录,密码错误")
    def test_user_login_r2(self):
        body = {
            "loginName": self.userInfo["username"],
            "password": "*%$?",
            "tenantId": "001"
        }
        result = self.user_login(headers=self.headers,body=body)
        assert result["resultData"] is None
        assert result["errorMessage"] == "密码不正确,请重试"

    @allure.story("登录,入参tenantId不存在")
    def test_user_login_r3(self):
        body = {
            "loginName": self.userInfo["username"],
            "password": self.userInfo["passwd"],
        }
        result = self.user_login(headers=self.headers,body=body)
        assert result["resultData"] is None
        assert result["errorMessage"] == "租户id不能为空"

    @allure.story("查询设备列表，token非法")
    def test_get_deviceList_r(self):
        headers_r = self.headers.copy()
        headers_r["Authorization"] = "aaaaaaaaaaaaaaaaaaa"
        result = self.get_deviceList(headers=headers_r,body={})
        assert result["errorMessage"] == "非法的token"

    @allure.story("查询设备列表，正常查询")
    def test_get_deviceList(self):
        result = self.get_deviceList(headers=self.headers,body={})
        assert len(result["resultData"]) > 0
        assert result["resultData"][0]["deviceId"] == self.deviceId

    @allure.story("查询测点实时数据，设备id不存在")
    def test_get_realTimeData_r1(self):
        body = {"deviceId":"123456789"}
        result = self.get_realTimeData(headers=self.headers,body=body)
        assert result["errorMessage"] == "用户无当前设备的操作权限,请联系管理员"

    @allure.story("查询测点实时数据,正常")
    def test_get_realTimeData(self):
        body = {"deviceId":self.deviceId}
        result = self.get_realTimeData(headers=self.headers,body=body)
        #assert len(result["resultData"]) >0
        assert result["success"] == True