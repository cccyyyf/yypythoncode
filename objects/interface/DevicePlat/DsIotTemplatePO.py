# coding=utf-8
# Time : 2020/11/3 13:39
# Author : huxin
from objects.interface.baseObjects.BaseObj import *
from objects.interface.utils.PropertiesUtil import *
from objects.interface.utils.DBRequest import *
from RootPath import *
import allure

class DsIotTemplatePO(BaseObj):
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

    @allure.step("新增iot设备模板")
    def add_iotTemplate(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIotTemplate"
        result = self.do_post(url=url,headers=headers,params=body)
        return result

    @allure.step("修改iot设备模板")
    def modify_iotTemplate(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIotTemplate"
        result = self.do_put(url=url,headers=headers,params=body)
        return result

    @allure.step("根据条件查询-基础模板源列表")
    def search_BaseSourceList(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIotTemplate/BaseSourceList"
        result = self.do_post(url=url, headers=headers, params=body)
        return result

    @allure.step("根据条件查询-用户模板源列表")
    def search_UserSourceList(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIotTemplate/UserSourceList"
        result = self.do_post(url=url, headers=headers, params=body)
        return result

    @allure.step("根据条件查询IOT设备模板")
    def search_List(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIotTemplate/list"
        result = self.do_post(url=url, headers=headers, params=body)
        return result

    @allure.step("根据条件查询IOT设备模板(详情)")
    def search_IotTemplateDetails(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIotTemplate/queryDsIotTemplateDetails"
        result = self.do_post(url=url, headers=headers, params=body)
        return result

    @allure.step("根据ID删除IOT设备模板")
    def dele_DsIotTemplate(self,id,headers):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIotTemplate/" + id
        result = self.do_delete(url=url, headers=headers)
        return result

    @allure.step("Iot设备模板excel导出")
    def export_excel(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/exportExcel"
        result = self.do_post(url=url, headers=headers, params=body)
        return result

    @allure.step("ioT模板下载")
    def export_Template(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/exportTemplate"
        result = self.do_post(url=url, headers=headers, params=body)
        return result

    @allure.step("ioT模板导入")
    def import_Excel(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/importExcel"
        result = self.do_post(url=url, headers=headers, params=body)
        return result

    @allure.step("克隆iot模板")
    def copy_iotTemplate(self,headers,id):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIotTemplate/" + id
        result = self.do_get(url=url,headers=headers)
        return result
