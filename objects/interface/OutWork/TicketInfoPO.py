# -*- coding: utf-8 -*-
# @Author  : Felix.Ma
# @Time    : 2020/11/24 9:47

from objects.interface.baseObjects.BaseObj import *
from objects.interface.utils.PropertiesUtil import *
from objects.interface.utils.DBRequest import *
from RootPath import *
import allure


class TicketInfoPO(BaseObj):
    outwork_path = RootPath.getOutWorkPath() + "Api.yml"
    request_info = PropertiesUtil.loadLocatorValueFromYml(path=outwork_path, key="接口信息")
    db_info = PropertiesUtil.loadLocatorValueFromYml(path=outwork_path, key="db信息")

    @allure.step("创建工单")
    def create_ticket(self, params, headers):
        url = self.request_info["url"] + "/outworkapi/ticketInfo/createTicket"
        response = self.do_post(url=url, params=params, headers=headers)
        return response

    @allure.step("获取数据库中的信息")
    def get_db_dict(self, dict_sql) -> list:
        """
        根据sql获取数据库的值
        """
        result = db_query(self.db_info["outwork"], dict_sql)
        return result

    @allure.step("获取所有工单列表信息")
    def get_ticket_list_info(self, params, headers):
        url = self.request_info["url"] + "/outworkapi/ticketInfo/selectTicketInfoPage"
        response = self.do_post(url=url, params=params, headers=headers)
        return response

    @allure.step("获取我的创建列表信息")
    def get_ticket_create_list_info(self, params, headers):
        url = self.request_info["url"] + "/outworkapi/ticketInfo/selectTicketInfoCreatePage"
        response = self.do_post(url=url, params=params, headers=headers)
        return response

    @allure.step("获取待处理列表信息")
    def get_ticket_wait_list_info(self, params, headers):
        url = self.request_info["url"] + "/outworkapi/ticketInfo/selectTicketInfoWaitPage"
        response = self.do_post(url=url, params=params, headers=headers)
        return response

    @allure.step("获取工单详情")
    def get_ticket_info(self, params, headers):
        url = self.request_info["url"] + "/outworkapi/ticketDetail/ticketAndStatusInfo/" + params
        response = self.do_get(url=url, headers=headers)
        return response

    @allure.step("获取节点信息")
    def get_step_detail(self, params, headers):
        url = self.request_info["url"] + "/outworkapi/ticketDetail/stepDetail/" + params
        response = self.do_get(url=url, headers=headers)
        return response

    @allure.step("获取节点流转日志")
    def get_operate_record(self, params, headers):
        url = self.request_info["url"] + "/outworkapi/ticketDetail/operateRecord/" + params
        response = self.do_get(url=url, headers=headers)
        return response

    @allure.step("接单")
    def accept_ticket(self, params, headers):
        url = self.request_info["url"] + "/outworkapi/ticketOperation/accept"
        response = self.do_post(url=url, headers=headers, params=params)
        return response

    @allure.step("办理")
    def operate_ticket(self, params, headers):
        url = self.request_info["url"] + "/outworkapi/ticketOperation/submit"
        response = self.do_post(url=url, headers=headers, params=params)
        return response

    @allure.step("获取已完成列表信息")
    def get_ticket_done_list_info(self, params, headers):
        url = self.request_info["url"] + "/outworkapi/ticketInfo/selectTicketInfoDonePage"
        response = self.do_post(url=url, headers=headers, params=params)
        return response


