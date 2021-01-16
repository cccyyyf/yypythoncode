# -*- coding: utf-8 -*-
# @Author  : Felix.Ma
# @Time    : 2020/11/9 9:40

import allure
from objects.interface.OutWork.MenuPO import MenuPO
from objects.interface.baseObjects.LoginPO import LoginPO
from cases.interface.OutWork.public import par_dir, yml_name, login_api_url


@allure.feature("获取目录")
class TestMenu(MenuPO):

    def setup_class(self):
        self.headers = LoginPO().get_headers("wpg账号", par_dir, yml_name, login_api_url)

    def teardown_class(self):
        pass

    @allure.story("获取目录")
    def test_get_menus(self):
        params = {"codes": ""}
        response = self.get_menus(headers=self.headers, params=params)
        assert response["status"] == "complete"
        assert response["resultData"]
