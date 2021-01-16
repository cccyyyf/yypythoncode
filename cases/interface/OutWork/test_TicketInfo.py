# -*- coding: utf-8 -*-
# @Author  : Felix.Ma
# @Time    : 2020/11/24 9:50

import allure
from objects.interface.OutWork.TicketInfoPO import TicketInfoPO
from objects.interface.baseObjects.LoginPO import LoginPO
from cases.interface.OutWork.public import par_dir, yml_name, login_api_url

ticket = {"title": "ticket title", "priority": 0, "questionDescribe": "description", "sysSource": "kf",
          "address": "兰若寺", "field_kHPoXFqtM": "100米", "latitude": 39.910925, "longitude": 116.413384}
template = {"name": "deadcells-创建到达审核-无分支", "bigType": "pipe", "smallType": "dma"}
# 工单状态: 1.办理中
ticket_status = ["1"]
# 节点状态: 0.待接单 1.待办理 2.已办结
node_status = ["0", "1", "2"]
node_name = ["创建", "到达", "审核", "接单"]
node_type = ["create", "arrive", "approval", "accept", "handle"]
users = ["死亡细胞", "哈迪斯", "大菠萝"]
templateId = "4dd6d5cb50fa68728701f151bdce04eb"
search_params = {"createTimeStart": "", "createTimeEnd": "", "ticketNo": None,
                 "title": ticket["title"],
                 "agingStatus": "", "ticketStatus": "", "stepStatus": "", "priority": "",
                 "sysCodeList": [],
                 "userIdList": [], "page": {"current": 1, "size": 20}}


@allure.feature("工单处理")
class TestTicketInfo(TicketInfoPO):
    ticket_id = ""
    step_ids = []

    def setup_class(self):
        self.headers1 = LoginPO().get_headers("wpg账号", par_dir, yml_name, login_api_url)
        self.headers2 = LoginPO().get_headers("租主账号", par_dir, yml_name, login_api_url)
        self.headers3 = LoginPO().get_headers("租户账号", par_dir, yml_name, login_api_url)

    def teardown_class(self):
        pass

    @allure.story("创建工单")
    def test_create_ticket(self):
        params = {
            "formJson": ticket,
            "templateId": templateId,
            "createTicketFormDTO": ticket}
        response = self.create_ticket(headers=self.headers1, params=params)
        assert response["status"] == "complete"

    @allure.story("获取所有工单列表信息")
    def test_get_ticket_list_info(self, headers=1, stepName=node_name[1], stepStatus=node_status[0], stepOperator=users[1]):
        if headers == 1:
            header = self.headers1
        if headers == 2:
            header = self.headers2
        if headers == 3:
            header = self.headers3
        response = self.get_ticket_list_info(headers=header, params=search_params)
        assert response["status"] == "complete"
        assert response["resultData"]["records"]
        record = response["resultData"]["records"][0]
        assert record["templateName"] == template["name"]
        assert record["formValue"]["title"] == ticket["title"]
        assert record["bigType"] == template["bigType"]
        assert record["smallType"] == template["smallType"]
        assert record["priority"] == ticket["priority"]
        assert record["ticketStatus"] == ticket_status[0]
        assert record["stepName"] == stepName
        assert record["stepStatus"] == stepStatus
        assert record["stepOperator"] == stepOperator
        assert record["address"] == ticket["address"]
        assert record["createByName"] == users[0]
        assert record["sysCode"] == ticket["sysSource"]

    @allure.story("获取我的创建列表信息")
    def test_get_ticket_create_list_info(self):
        response = self.get_ticket_create_list_info(headers=self.headers1, params=search_params)
        assert response["status"] == "complete"
        assert response["resultData"]["records"]
        record = response["resultData"]["records"][0]
        assert record["templateName"] == template["name"]
        assert record["formValue"]["title"] == ticket["title"]
        assert record["bigType"] == template["bigType"]
        assert record["smallType"] == template["smallType"]
        assert record["priority"] == ticket["priority"]
        assert record["ticketStatus"] == ticket_status[0]
        assert record["stepName"] == node_name[1]
        assert record["stepStatus"] == node_status[0]
        assert record["stepOperator"] == users[1]
        assert record["address"] == ticket["address"]

    @allure.story("获取待处理列表信息")
    def test_get_ticket_wait_list_info(self, headers=2, stepName=node_name[1], stepStatus=node_status[0],
                                       stepOperator=users[1]):
        if headers == 1:
            header = self.headers1
        if headers == 2:
            header = self.headers2
        if headers == 3:
            header = self.headers3
        response = self.get_ticket_wait_list_info(headers=header, params=search_params)
        assert response["status"] == "complete"
        assert response["resultData"]["records"]
        record = response["resultData"]["records"][0]
        TestTicketInfo.ticket_id = record["id"]
        assert record["templateName"] == template["name"]
        assert record["formValue"]["title"] == ticket["title"]
        assert record["bigType"] == template["bigType"]
        assert record["smallType"] == template["smallType"]
        assert record["priority"] == ticket["priority"]
        assert record["ticketStatus"] == ticket_status[0]
        assert record["stepName"] == stepName
        assert record["stepStatus"] == stepStatus
        assert record["stepOperator"] == stepOperator
        assert record["address"] == ticket["address"]
        assert record["createByName"] == users[0]
        assert record["sysCode"] == ticket["sysSource"]

    @allure.story("获取工单详情")
    def test_get_ticket_info(self):
        response = self.get_ticket_info(headers=self.headers2, params=TestTicketInfo.ticket_id)
        assert response["status"] == "complete"
        assert response["resultData"]
        ticket_info = response["resultData"]["ticketInfo"]
        result_template = response["resultData"]["template"]
        ticketStatus = response["resultData"]["ticketStatus"]
        assert ticket_info["title"] == ticket["title"]
        assert result_template["bigType"] == template["bigType"]
        assert result_template["smallType"] == template["smallType"]
        assert result_template["name"] == template["name"]
        assert ticketStatus["ticketStatus"] == ticket_status[0]
        assert ticket_info["createByName"] == users[0]
        assert ticket_info["formValue"]["questionDescribe"] == ticket["questionDescribe"]
        assert ticket_info["address"] == ticket["address"]
        assert ticket_info["priority"] == ticket["priority"]
        assert ticket_info["sysCode"] == ticket["sysSource"]
        assert ticket_info["formValue"]["field_kHPoXFqtM"] == ticket["field_kHPoXFqtM"]
        assert ticket_info["formValue"]["latitude"] == ticket["latitude"]
        assert ticket_info["formValue"]["longitude"] == ticket["longitude"]

    @allure.story("获取节点信息")
    def test_get_step_detail(self, headers=2, operation=0):
        if headers == 1:
            header = self.headers1
        if headers == 2:
            header = self.headers2
        if headers == 3:
            header = self.headers3

        if operation == 0:
            stepStatus = ["2", "0", None]
        if operation == 1:
            stepStatus = ["2", "1", None]
        if operation == 2:
            stepStatus = ["2", "2", "0"]
        if operation == 3:
            stepStatus = ["2", "2", "1"]
        if operation == 4:
            stepStatus = ["2", "2", "2"]
        response = self.get_step_detail(headers=header, params=TestTicketInfo.ticket_id)
        assert response["status"] == "complete"
        assert response["resultData"]
        resultData = response["resultData"]
        for i in range(len(resultData)):
            assert resultData[i]["stepName"].strip() == node_name[i]
            assert resultData[i]["stepType"] == node_type[i]
            if resultData[i]["stepStatus"] and resultData[i]["waitAcceptName"]:
                if resultData[i]["id"] not in self.step_ids:
                    self.step_ids.append(resultData[i]["id"])
                assert resultData[i]["stepStatus"] == stepStatus[i]
                assert resultData[i]["waitAcceptName"] == users[i]

    @allure.story("获取节点流转日志")
    def test_get_operate_record(self, headers=2, stepName=node_name[0], operatorName=users[0], eventCode=node_type[0],
                                eventDescription="工单创建"):
        if headers == 1:
            header = self.headers1
        if headers == 2:
            header = self.headers2
        if headers == 3:
            header = self.headers3
        response = self.get_operate_record(headers=header, params=TestTicketInfo.ticket_id)
        assert response["status"] == "complete"
        assert response["resultData"]
        resultData = response["resultData"]
        assert resultData[0]["stepName"] == stepName
        assert resultData[0]["operatorName"] == operatorName
        assert resultData[0]["eventCode"] == eventCode
        assert resultData[0]["eventDescription"] == eventDescription

    @allure.story("接单")
    def test_accept_ticket(self, headers=2, stepDetailId=""):
        if not stepDetailId:
            stepDetailId = self.step_ids[1]
        if headers == 1:
            header = self.headers1
        if headers == 2:
            header = self.headers2
        if headers == 3:
            header = self.headers3
        params = {"stepDetailId": stepDetailId, "ticketId": TestTicketInfo.ticket_id}
        response = self.accept_ticket(headers=header, params=params)
        assert response["status"] == "complete"
        assert response["resultData"] == "提交成功"

    @allure.story("第二个人校验待处理列表")
    def test_get_ticket_wait_list_info_again(self):
        self.test_get_ticket_wait_list_info(stepStatus=node_status[1])

    @allure.story("第二个人校验节点信息")
    def test_get_step_detail_again(self):
        self.test_get_step_detail(operation=1)

    @allure.story("第二个人校验节点流转日志")
    def test_get_operate_record_again(self):
        self.test_get_operate_record(stepName=node_name[1], operatorName=users[1], eventCode=node_type[3],
                                     eventDescription=users[1] + node_name[1] + node_name[3])

    @allure.story("办理工单")
    def test_operate_ticket(self, headers=2, formValue={}, stepDetailId=""):
        if not stepDetailId:
            stepDetailId = self.step_ids[1]
        if headers == 1:
            header = self.headers1
        if headers == 2:
            header = self.headers2
        if headers == 3:
            header = self.headers3
        params = {"stepDetailId": stepDetailId}
        params.update(formValue)
        response = self.operate_ticket(headers=header, params=params)
        assert response["status"] == "complete"
        assert response["resultData"] == "提交成功"

    @allure.story("第二个人校验所有工单列表")
    def test_get_ticket_list_info_again(self):
        self.test_get_ticket_list_info(headers=2, stepName=node_name[2], stepOperator=users[2])

    @allure.story("第三个人校验待处理列表")
    def test_get_ticket_wait_list_info_3rd(self):
        self.test_get_ticket_wait_list_info(headers=3, stepName=node_name[2], stepOperator=users[2])

    @allure.story("第三个人校验节点信息")
    def test_get_step_detail_3rd(self):
        self.test_get_step_detail(headers=3, operation=2)

    @allure.story("第三个人校验节点流转日志")
    def test_get_operate_record_3rd(self):
        self.test_get_operate_record(stepName=node_name[1], operatorName=users[1], eventCode=node_type[4],
                                     eventDescription=users[1] + "完成" + node_name[1])

    @allure.story("第三个人接单")
    def test_accept_ticket_again(self):
        print(self.step_ids)
        self.test_accept_ticket(headers=3, stepDetailId=self.step_ids[2])

    @allure.story("第三个人校验待处理列表")
    def test_get_ticket_wait_list_info_4th(self):
        self.test_get_ticket_wait_list_info(headers=3, stepStatus=node_status[1], stepName=node_name[2],
                                            stepOperator=users[2])

    @allure.story("第三个人校验节点信息")
    def test_get_step_detail_4th(self):
        self.test_get_step_detail(headers=3, operation=3)

    @allure.story("第三个人校验节点流转日志")
    def test_get_operate_record_4rd(self):
        self.test_get_operate_record(headers=3, stepName=node_name[2], operatorName=users[2], eventCode=node_type[3],
                                     eventDescription=users[2] + node_name[2] + node_name[3])

    @allure.story("第三个人审核")
    def test_operate_ticket_again(self):
        formValue = {"formValue": {"field105": 1, "field106": "通过", "field_kpjJV2qbR": "通过原因"}}
        self.test_operate_ticket(headers=3, formValue=formValue, stepDetailId=self.step_ids[2])

    @allure.story("获取已完成工单列表信息")
    def test_get_ticket_done_list_info(self):
        response = self.get_ticket_list_info(headers=self.headers3, params=search_params)
        assert response["status"] == "complete"
        assert response["resultData"]["records"]
        record = response["resultData"]["records"][0]
        assert record["templateName"] == template["name"]
        assert record["formValue"]["title"] == ticket["title"]
        assert record["bigType"] == template["bigType"]
        assert record["smallType"] == template["smallType"]
        assert record["priority"] == ticket["priority"]
        assert not record["stepName"]
        assert not record["stepStatus"]
        assert not record["stepOperator"]
        assert record["address"] == ticket["address"]
        assert record["createByName"] == users[0]
        assert record["sysCode"] == ticket["sysSource"]

    @allure.story("第三个人校验节点信息")
    def test_get_step_detail_5th(self):
        self.test_get_step_detail(headers=3, operation=4)

    @allure.story("第三个人校验节点流转日志")
    def test_get_operate_record_5th(self):
        self.test_get_operate_record(headers=3, stepName=node_name[2], operatorName=users[2], eventCode=node_type[4],
                                     eventDescription=users[2] + "完成" + node_name[2])
