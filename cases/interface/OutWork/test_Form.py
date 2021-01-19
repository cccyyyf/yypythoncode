# -*- coding: utf-8 -*-
# @Author  : Felix.Ma
# @Time    : 2020/11/20 17:09

import allure
from objects.interface.OutWork.FormPO import FormPO
from objects.interface.baseObjects.LoginPO import LoginPO
from cases.interface.OutWork.public import par_dir, yml_name, login_api_url


@allure.feature("操作表单")
class TestSysGroup(FormPO):

    userid = 'e58888a43ad3d6e085f86187a72efd07'

    def setup_class(self):
        self.headers = LoginPO().get_headers("wpg账号", par_dir, yml_name, login_api_url)

    def teardown_class(self):
        pass

    @allure.story("新增表单")
    def test_add_form(self):
        params = {"formName": "11", "formType": "create", "remark": "11"}
        response = self.add_form(headers=self.headers, params=params)
        assert response["status"] == "complete"
        assert response["resultData"]
        result = response["resultData"]
        result["createBy"] = self.userid

