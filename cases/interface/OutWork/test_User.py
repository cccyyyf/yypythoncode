# -*- coding: utf-8 -*-
# @Author  : Felix.Ma
# @Time    : 2020/11/9 8:54

import allure
from objects.interface.OutWork.UserPO import UserPO
from objects.interface.baseObjects.LoginPO import LoginPO
from cases.interface.OutWork.public import par_dir, yml_name, login_api_url


@allure.feature("获取用户")
class TestUser(UserPO):

    def setup_class(self):
        self.headers = LoginPO().get_headers("wpg账号", par_dir, yml_name, login_api_url)

    def teardown_class(self):
        pass

    @allure.story("获取所有用户")
    def test_get_all_users(self):
        response = self.get_all_users(headers=self.headers)
        assert response["status"] == "complete"
        assert response["resultData"]

    @allure.story("根据userid获取用户")
    def test_get_user_by_id(self):
        response = self.get_user_by_id(headers=self.headers, userid='1')
        assert response["status"] == "complete"
        assert response["resultData"]

    @allure.story("同步用户")
    def test_sync_users(self):
        response = self.sync_users(headers=self.headers)
        assert response["status"] == "complete"

