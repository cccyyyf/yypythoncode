# coding=utf-8
# Time : 2020/12/6 10:48
# Author : huxin
from objects.interface.baseObjects.BaseObj import *
from objects.interface.utils.PropertiesUtil import *
from objects.interface.utils.DBRequest import *
from RootPath import *
import allure
from objects.interface.utils.Decorators import *

class DsIndustryDevicePO(BaseObj):
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

    @allure.step("新增行业设备信息")
    def add_DsIndustryDevice(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryDevice/add"
        response = self.do_post(url=url,headers=headers,params=body)
        return response

    @allure.step("修改行业设备信息")
    def update_DsIndustryDevice(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryDevice/update"
        response = self.do_put(url=url,headers=headers,params=body)
        return response

    @allure.step("生成设备二维码")
    def get_deviceQrCode(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryDevice/deviceQrCode"
        response = self.do_post(url=url,headers=headers,params=body)
        return response

    @allure.step("根据行业设备id查详情")
    def get_detail(self,headers,industryId):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryDevice/detail?industryId=" + industryId
        response = self.do_get(url=url,headers=headers)
        return response

    @allure.step("行业设备excel导出")
    def export_excel(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryDevice/exportExcel"
        response = self.do_post(url=url,headers=headers,params=body)
        return response

    @allure.step("根据条件查询行业设备信息列表")
    def get_list(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryDevice/list"
        response = self.do_post(url=url,headers=headers,params=body)
        return response

    @allure.step("行业设备id查实时数据")
    def get_realTimeData(self,headers,industryId):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryDevice/realTimeData?industryId=" + industryId
        response = self.do_get(url=url,headers=headers)
        return response

    @allure.step("实时数据过滤")
    @post(request_info["url"] + "/deviceManagmentApi/DsIndustryDevice/realTimeDataSearch")
    def search_realTimeData(self,headers,params):
        pass


    @allure.step("根据条件查询行业设备模板")
    @post(request_info["url"] + "/deviceManagmentApi/DsIndustryDevice/templateList")
    def get_templateList(self,headers,params):
        pass

    @allure.step("批量删除行业设备信息")
    @post(request_info["url"] + "/deviceManagmentApi/DsIndustryDevice/removes")
    def remove_devices(self,headers,params):
        pass

    @allure.step("根据ID删除行业设备信息")
    def dele_device(self,headers,dsIndustryDeviceId):
        url = self.request_info["url"] + "/deviceManagmentApi/DsIndustryDevice/delete?dsIndustryDeviceId=" + dsIndustryDeviceId
        response = self.do_delete(url=url,headers=headers)
        return response

    #对外接口
    @allure.step("根据行业设备编号查详情")
    def get_ByIndustryDeviceId(self,headers,industryDeviceId):
        url = self.request_info["url"] + "/deviceManagmentApi/industryDevice/getByIndustryDeviceId?industryDeviceId=" + industryDeviceId
        response = self.do_get(url=url,headers=headers)
        return response

    @allure.step("根据行业设备编号查询关联的设备测点")
    def get_DevicePointByIndustryDeviceId(self,headers,industryDeviceId):
        url = self.request_info["url"] + "/deviceManagmentApi/industryDevice/getDevicePointByIndustryDeviceId?industryDeviceId=" + industryDeviceId
        response = self.do_get(url=url,headers=headers)
        return response

    @allure.step("根据行业设备查询关联的设备测点")
    def get_DevicePointByIndustryId(self, headers, industryId):
        url = self.request_info[
                  "url"] + "/deviceManagmentApi/industryDevice/DevicePointByIndustryId?industryId=" + industryId
        response = self.do_get(url=url, headers=headers)
        return response

    @allure.step("根据行业设备id查详情")
    def get_IndustryDetail(self, headers, industryId):
        url = self.request_info[
                  "url"] + "/deviceManagmentApi/industryDevice/getIndustryDetail?industryId=" + industryId
        response = self.do_get(url=url, headers=headers)
        return response

    @allure.step("根据行业设备主键id用实时数据")
    @post(request_info["url"] + "/deviceManagmentApi/industryDevice/queryRealTimeDataSearch")
    def query_RealTimeDataSearch(self,headers,params):
        pass

    @allure.step("根据行业设备编号查询实时数据查询")
    @post(request_info["url"] + "/deviceManagmentApi/industryDevice/queryRealTimeDataSearchByCode")
    def query_RealTimeDataSearchByCode(self,headers,params):
        pass

    @allure.step("根据条件查询行业设备信息")
    @post(request_info["url"] + "/deviceManagmentApi/industryDevice/selectIndustryList")
    def select_IndustryList(self,headers,params):
        pass
