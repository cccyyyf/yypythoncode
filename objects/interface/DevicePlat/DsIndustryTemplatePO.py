# coding=utf-8
# Time : 2020/11/13 10:39
# Author : huxin
from objects.interface.baseObjects.BaseObj import *
from objects.interface.utils.PropertiesUtil import *
from objects.interface.utils.DBRequest import *
from RootPath import *
import allure

class DsIndustryTemplatePO(BaseObj):
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

    @allure.step("新增行业设备模板")
    def add_IndustryTemplate(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryTemplate/insert"
        result = self.do_post(url=url,headers=headers,params=body)
        return result

    @allure.step("修改行业设备模板")
    def modify_IndustryTemplate(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryTemplate/update"
        result = self.do_put(url=url,headers=headers,params=body)
        return result

    @allure.step("根据条件查询-基础模板源列表")
    def search_BaseSourceList(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryTemplate/Baselist"
        result = self.do_post(url=url, headers=headers, params=body)
        return result

    @allure.step("根据条件查询-用户模板源列表")
    def search_UserSourceList(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryTemplate/Userlist"
        result = self.do_post(url=url, headers=headers, params=body)
        return result

    @allure.step("根据条件查询行业设备模板")
    def search_List(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryTemplate/list"
        result = self.do_post(url=url, headers=headers, params=body)
        return result

    @allure.step("根据模板ID查询行业设备模板(详情)")
    def search_IndustryTemplateDetails(self, headers, templateId):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryTemplate/detail?templateId=" + templateId
        result = self.do_get(url=url, headers=headers)
        return result

    @allure.step("根据ID删除行业设备模板")
    def dele_DsIndustryTemplate(self, templateId,headers):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryTemplate/delete?templateId=" + templateId
        result = self.do_delete(url=url, headers=headers)
        return result

    @allure.step("行业设备模板excel导出")
    def export_excel(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryTemplate/exportExcel"
        result = self.do_post(url=url, headers=headers, params=body)
        return result

    @allure.step("行业设备模板下载")
    def export_Template(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryTemplate/DownloadTemplate"
        result = self.do_post(url=url, headers=headers, params=body)
        return result


    @allure.step("当前人能看到的行业设备模板")
    def get_IndustryTemplates(self,headers):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryTemplate/selectIndustrySimpleInfo"
        result = self.do_get(url=url,headers=headers)
        return result

    @allure.step("获取行业设备模板标签")
    def get_labels(self,headers,templateId):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryTemplate/getLabels?templateId="+ templateId
        result = self.do_get(url=url, headers=headers)
        return result

    #对外接口
    @allure.step("根据条件查询行业设备基础模板")
    def get_BaseList(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/industryTemplateClient/BaseList"
        response = self.do_post(url=url,headers=headers,params=body)
        return response

    @allure.step("根据条件查询行业设备用户模板")
    def get_Userlist(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/industryTemplateClient/Userlist"
        response = self.do_post(url=url,headers=headers,params=body)
        return response

    @allure.step("根据id查询行业设备模板详情")
    def get_detail(self,headers,templateId):
        url = self.request_info["url"] + "/deviceManagmentApi/industryTemplateClient/detail?templateId=" + templateId
        response = self.do_get(url=url,headers=headers)
        return response

    @allure.step("查询行业设备模板列表")
    def get_queryPage(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/industryTemplateClient/queryPage"
        response = self.do_post(url=url, headers=headers, params=body)
        return response