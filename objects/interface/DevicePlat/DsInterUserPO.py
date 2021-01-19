# coding=utf-8
# Time : 2020/12/4 13:33
# Author : huxin

from objects.interface.baseObjects.BaseObj import *
from objects.interface.utils.PropertiesUtil import *
from objects.interface.utils.DBRequest import *
from RootPath import *
import allure

class DsInterUserPO(BaseObj):
    public_path = RootPath.getDevicePlatPath() + "Public.yml"
    request_info = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="接口信息")
    DB_info = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="DB信息")

    @allure.step("获取数据库中的信息")
    def get_DB_data(self, sql) -> list:
        """
        根据sql获取数据库的值
        """
        result = db_query(self.DB_info["devicecenter"], sql)
        return result

    @allure.step("新增接口用户")
    def add_InterUser(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/insertDsInterUser"
        response = self.do_post(url=url,headers=headers,params=body)
        return response

    @allure.step("修改接口用户")
    def update_InterUser(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/updateDsInterUser"
        response = self.do_put(url=url,headers=headers,params=body)
        return response

    @allure.step("查看接口用户详情")
    def get_details(self,headers,entityId):
        url = self.request_info["url"] + "/deviceManagmentApi/details?entityId=" + entityId
        response = self.do_get(url=url,headers=headers)
        return response

    @allure.step("查询接口用户列表")
    def get_list(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/list"
        response = self.do_post(url=url,headers=headers,params=body)
        return response

    @allure.step("接口用户重置密码")
    def reset_passwd(self,headers,userId):
        url = self.request_info["url"] + "/deviceManagmentApi/resetPassword?userId=" + userId
        response = self.do_post(url=url,headers=headers,params={})
        return response

    @allure.step("删除接口用户")
    def dele_InterUser(self,headers,userId):
        url = self.request_info["url"] + "/deviceManagmentApi/removeById?userId=" + userId
        response = self.do_delete(url=url,headers=headers)
        return response


    #接口用户对外接口
    @allure.step("接口用户登录")
    def user_login(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/interUserClient/login"
        response = self.do_post(url=url,headers=headers,params=body)
        return response

    @allure.step("查询设备列表")
    def get_deviceList(self,headers,body):
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        url = self.request_info["url"] + "/deviceManagmentApi/interUserClient/deviceList"
        response = self.do_post(url=url,headers=headers,params=body)
        return response

    @allure.step("查询测点实时数据")
    def get_realTimeData(self,headers,body):
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        url = self.request_info["url"] + "/deviceManagmentApi/interUserClient/realTimeData"
        response = self.do_post(url=url,headers=headers,params=body)
        return response