# coding=utf-8
# Time : 2020/10/21 18:38
# Author : huxin

from objects.interface.baseObjects.BaseObj import *
from objects.interface.utils.PropertiesUtil import *
from objects.interface.utils.DBRequest import *
from RootPath import *
import allure


class DsStationPO(BaseObj):
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

    @allure.step("添加区域")
    def add_area(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsArea/create"
        response = self.do_post(url=url, headers=headers, params=body)
        return response

    @allure.step("修改区域")
    def modify_area(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsArea/update"
        response = self.do_put(url=url, headers=headers, params=body)
        return response

    @allure.step("查询区域")
    def search_area(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsArea/getTree"
        response = self.do_post(url=url, headers=headers, params=body)
        return response

    @allure.step("删除区域")
    def dele_area(self, headers, entityId):
        url = self.request_info["url"] + "/deviceManagmentApi/DsArea/DsArea?entityId=" + entityId
        response = self.do_delete(url=url, headers=headers)
        return response

    @allure.step("新增站点")
    def add_station(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsStation/insert"
        response = self.do_post(url=url, headers=headers, params=body)
        return response

    @allure.step("修改站点")
    def modify_station(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsStation/edit"
        response = self.do_put(url=url, headers=headers, params=body)
        return response

    @allure.step("根据条件查询站点信息表")
    def search_station(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsStation/page"
        response = self.do_post(url=url, headers=headers, params=body)
        return response

    @allure.step("分配用户时，查询区域站点树")
    def search_area_station(self, headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsStation/stationAreaTree"
        response = self.do_post(url=url,headers=headers,params=body)
        return response

    @allure.step("获取角色")
    def get_role_list(self, headers):
        url = self.request_info["url"] + "/deviceManagmentApi/DsStation/roleList"
        response = self.do_get(url=url, headers=headers)
        return response

    @allure.step("用户批量关联站点")
    def relate_user_stations(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsStation/relateUserSts"
        response = self.do_post(url=url, headers=headers, params=body)
        return response

    @allure.step("excel导出")
    def export_excel(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsStation/exportExcel"
        response = self.do_post(url=url, headers=headers, params=body)
        return response

    @allure.step("批量删除")
    def dele_station(self,headers,ids):
        url = self.request_info["url"] + "/deviceManagmentApi/DsStation/batchDel?ids=" + ids
        response = self.do_delete(url=url,headers=headers)
        return response


    #对外接口方法
    @allure.step("查看站点详情")
    def get_detail(self,headers,id):
        url = self.request_info["url"] +"/deviceManagmentApi/stationClient/detail?stationId=" + id
        response = self.do_get(url=url,headers=headers)
        return response

    @allure.step("查询站点信息表")
    def query_page(self,headers,body):
        url = self.request_info["url"] +"/deviceManagmentApi/stationClient/queryPage"
        response = self.do_post(url=url,headers=headers,params=body)
        return response

    @allure.step("查询区域-站点混合树")
    def query_stationAreaTree(self,headers,body):
        url = self.request_info["url"] +"/deviceManagmentApi/stationClient/stationAreaTree"
        response = self.do_post(url=url,headers=headers,params=body)
        return response

    @allure.step("查询区域")
    def get_tree(self,headers,body):
        url = self.request_info["url"] +"/deviceManagmentApi/areaClient/getTree"
        response = self.do_post(url=url,headers=headers,params=body)
        return response