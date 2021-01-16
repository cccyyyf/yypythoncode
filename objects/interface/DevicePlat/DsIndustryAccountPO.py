# coding=utf-8
# Time : 2020/12/8 17:47
# Author : huxin
from objects.interface.baseObjects.BaseObj import *
from objects.interface.utils.Decorators import post
from objects.interface.utils.PropertiesUtil import *
from objects.interface.utils.DBRequest import *
from RootPath import *
import allure

class DsIndustryAccountPO(BaseObj):
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

    @allure.step("根据id查询台账详情")
    def get_DsIndustryAccount(self,headers,entityId):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryAccount?entityId=" + entityId
        response = self.do_get(url=url,headers=headers)
        return response

    @allure.step("新增台账信息")
    @post(request_info["url"] + "/deviceManagmentApi/DsIndustryAccount")
    def add_DsIndustryAccount(self,headers,params):
        pass

    @allure.step("修改台账信息")
    def modify_DsIndustryAccount(self,headers,params):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryAccount"
        response = self.do_put(url=url,params=params,headers=headers)
        return response

    @allure.step("删除台账信息")
    def dele_DsIndustryAccount(self,headers,bussinessId):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryAccount?bussinessId=" + bussinessId
        response = self.do_delete(url=url,headers=headers)
        return response

    @allure.step("导出excel")
    @post(request_info["url"] + "/deviceManagmentApi/DsIndustryAccount/exportExcel")
    def export_excel(self,headers,params):
        pass

    @allure.step("查询台账信息列表")
    @post(request_info["url"] + "/deviceManagmentApi/DsIndustryAccount/list")
    def get_list(self,headers,params):
        pass

    #对外接口
    @allure.step("根据id查询台账详情")
    def get_detail(self,headers,entityId):
        url = self.request_info["url"] + "/deviceManagmentApi/industryAccount/getDetail?entityId=" + entityId
        response = self.do_get(url=url,headers=headers)
        return response

    @allure.step("根据行业设备编码查询台账详情")
    @post(request_info["url"] + "/deviceManagmentApi/industryAccount/getDetailByIndustryDeviceId")
    def get_DetailByIndustryDeviceId(self,headers,params):
        pass

    @allure.step("根据条件查询台账信息表")
    @post(request_info["url"] + "/deviceManagmentApi/industryAccount/queryDsIndustryAccount")
    def query_DsIndustryAccount(self,headers,params):
        pass