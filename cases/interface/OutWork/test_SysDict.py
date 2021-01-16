# -*- coding: utf-8 -*-
# @Author  : Felix.Ma
# @Time    : 2020/11/4 14:16

import allure
from objects.interface.OutWork.SysDictPO import SysDictPO
from objects.interface.baseObjects.LoginPO import LoginPO
from cases.interface.OutWork.public import par_dir, yml_name, login_api_url


@allure.feature("获取字典")
class TestSysDict(SysDictPO):

    def setup_class(self):
        self.headers = LoginPO().get_headers("wpg账号", par_dir, yml_name, login_api_url)

    def teardown_class(self):
        pass

    @allure.story("获取所有字典")
    def test_get_all_dict(self):
        response = self.get_all_dict(headers=self.headers)
        assert response["status"] == "complete"
        assert response["resultData"]
        result_data = response["resultData"]
        dict_types = ["ticket_status", "ticket_template_type", "step_status", "ticket_sys_code", "deal_user_type",
                      "step_type", "ticket_operation", "step_msg_type", "ticket_priority",
                      "ticket_template_type_all_child", "group_type", "ticket_template_tree"]
        for dict_type in dict_types:
            assert result_data[dict_type]

    @allure.story("根据code获取字典")
    def test_get_dict_by_code(self):
        response = self.get_dict_by_code(headers=self.headers, sysDictCode='99')
        assert response["status"] == "complete"
        assert response["resultData"]
