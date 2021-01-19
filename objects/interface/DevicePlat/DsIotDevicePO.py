# coding=utf-8
# Time : 2020/11/5 10:32
# Author : huxin

from objects.interface.baseObjects.BaseObj import *
from objects.interface.utils.PropertiesUtil import *
from objects.interface.utils.DBRequest import *
from RootPath import *
import allure
from objects.interface.utils.Decorators import *


class DsIotDevicePO(BaseObj):
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

    @allure.step("新增IOT设备信息")
    def add_iotDevice(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIotDevice"
        result = self.do_post(url=url, headers=headers, params=body)
        return result

    @allure.step("修改IOT设备信息")
    def modify_iotDevice(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIotDevice"
        result = self.do_put(url=url, headers=headers, params=body)
        return result

    @allure.step("唯一性校验")
    def check_only(self, body, headers):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIotDevice/check"
        result = self.do_post(url=url, headers=headers, params=body)
        return result

    @allure.step("查看设备详情")
    def get_detail(self, id, headers):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIotDevice/detail?entityId=" + id
        body={}
        result = self.do_post(url=url, headers=headers, params=body)
        return result

    @allure.step("获取点击编辑后的详细")
    def edit_detail(self, body, headers,id):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIotDevice/edit?entityId=" +id
        result = self.do_post(url=url, headers=headers, params=body)
        return result

    @allure.step("Excel导出iot设备")
    def export_excel(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIotDevice/export"
        result = self.do_post(url=url, headers=headers, params=body)
        return result

    @allure.step("获取Iot设备连接方式字典列表")
    def get_connectionType(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIotDevice/listConnectionType"
        result = self.do_post(url=url, headers=headers, params=body)
        return result

    @allure.step("分页查询IOT设备信息")
    def get_listPage(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIotDevice/listPage"
        result = self.do_post(url=url, headers=headers, params=body)
        return result

    @allure.step("选择设备模板")
    def get_templateDetails(self, headers, body, id):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIotDevice/template?templateId=" + id
        result = self.do_post(url=url, headers=headers, params=body)
        return result

    @allure.step("删除iot设备信息")
    def dele_iotDevices(self, headers, ids):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIotDevice/removes?ids=" + ids
        result = self.do_delete(url=url, headers=headers)
        return result

    #对外接口
    @allure.step("获取设备详情")
    def get_detailAllByDeviceId(self,headers,deviceId):
        url = self.request_info["url"] + "/deviceManagmentApi/iotDeviceClient/detailAllByDeviceId?deviceId=" + deviceId
        result = self.do_get(url=url,headers= headers)
        return result

    @allure.step("查询设备列表")
    @post(request_info["url"] + "/deviceManagmentApi/iotDeviceClient/devicePageList")
    def get_devicePageList(self,headers,params):
        pass

    @allure.step("获取设备监测量")
    def get_devicePointList(self,headers,deviceId):
        url = self.request_info["url"] + "/deviceManagmentApi/iotDeviceClient/devicePointList?deviceId=" + deviceId
        result = self.do_get(url=url,headers= headers)
        return result

    @allure.step("获取设备实时数据")
    def get_deviceRealTimeData(self,headers,deviceId):
        url = self.request_info["url"] + "/deviceManagmentApi/iotDeviceClient/deviceRealTimeData?deviceId=" + deviceId
        result = self.do_get(url=url,headers= headers)
        return result