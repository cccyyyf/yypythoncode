# coding=utf-8
# Time : 2020/12/6 10:49
# Author : huxin
from objects.interface.baseObjects.BaseObj import *
from objects.interface.utils.PropertiesUtil import *
from objects.interface.utils.DBRequest import *
from RootPath import *
import allure

class DsIndustryAlarmPO(BaseObj):

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

    @allure.step("新增行业设备报警")
    def add_DsIndustryAlarm(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryAlarm/insertAlarm"
        response = self.do_post(url=url,params=body,headers=headers)
        return response

    @allure.step("修改行业设备报警")
    def modify_DsIndustryAlarm(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryAlarm"
        response = self.do_put(url=url,params=body,headers=headers)
        return response

    @allure.step("根据ID删除")
    def dele_DsIndustryAlarm(self,headers,entityId):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryAlarm/deleteAlarm?entityId=" + entityId
        response = self.do_delete(url=url,headers=headers)
        return response

    @allure.step("根据id查询行业设备告警详情")
    def get_details(self,headers,entityId):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryAlarm/getDetails?entityId=" + entityId
        response = self.do_get(url=url,headers=headers)
        return response

    @allure.step("根据条件查询行业设备报警列表")
    def query_list(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryAlarm/list"
        response = self.do_post(url=url,headers=headers,params=body)
        return response

    @allure.step("批量删除")
    def removes(self,headers,ids):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryAlarm/list?ids=" + ids
        response = self.do_delete(url=url,headers=headers)
        return response

    #对外接口
    @allure.step("根据id查询行业设备告警详情-外")
    def get_detail_out(self,headers,entityId):
        url = self.request_info["url"] + "/deviceManagmentApi/industryAlarm/getDetail?entityId=" + entityId
        response = self.do_get(url=url,headers=headers)
        return response

    @allure.step("根据条件查询行业设备报警信息")
    def query_DsIndustryAlarm(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/industryAlarm/queryDsIndustryAlarm"
        response = self.do_post(url=url,params=body,headers=headers)
        return response
