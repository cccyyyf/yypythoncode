# coding=utf-8
# Time : 2020/10/11 19:44
# Author : huxin

from objects.interface.baseObjects.BaseObj import *
from objects.interface.utils.PropertiesUtil import *
from objects.interface.utils.DBRequest import *
from RootPath import *
import allure
from .LoginPO import LoginPO


class DsPointPO(BaseObj):
    public_path = RootPath.getDevicePlatPath() + "Public.yml"
    request_info = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="接口信息")
    DB_info = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="DB信息")

    @allure.step("添加监测量库")
    def add_point(self, headers, body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsPoint"
        response = self.do_post(url=url, params=body, headers=headers)
        return response

    @allure.step("获取数据库中的信息")
    def get_DB_data(self, sql) -> list:
        """
        根据sql获取数据库的值
        """
        result = db_query(self.DB_info["devicecenter"], sql)
        return result

    @allure.step("修改监测量库")
    def modify_point(self,headers,body):
        url = self.request_info["url"] + "/deviceManagmentApi/DsPoint"
        response = self.do_put(url=url,headers=headers,params=body)
        return response

    @allure.step("删除监测量库")
    def delete_point(self,point_id,headers):
        url = self.request_info["url"] + "/deviceManagmentApi/DsPoint?entityId=" + point_id
        response = self.do_delete(url=url,headers=headers)
        return response

    @allure.step("查询监测量库")
    def search_point(self,body,headers):
        url = self.request_info["url"] + "/deviceManagmentApi/DsPoint/list"
        response = self.do_post(url=url,params=body,headers=headers)
        return response

    @allure.step("更新监测量是否为华为网关接口")
    def update_HwGateway(self,body,headers):
        entityId = body["entityId"]
        gatewayFlag = body["gatewayFlag"]
        url = self.request_info["url"] + "/deviceManagmentApi/DsPoint/updateHwGateway?entityId=%s&gatewayFlag=%s" % (entityId, gatewayFlag)
        response = self.do_put(url=url,params=body,headers=headers)
        return response