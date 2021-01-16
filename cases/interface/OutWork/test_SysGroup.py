# -*- coding: utf-8 -*-
# @Author  : Felix.Ma
# @Time    : 2020/11/11 11:31

import allure
from objects.interface.OutWork.SysGroupPO import SysGroupPO
from objects.interface.baseObjects.LoginPO import LoginPO
from cases.interface.OutWork.public import par_dir, yml_name, login_api_url


@allure.feature("获取字典")
class TestSysGroup(SysGroupPO):

    def setup_class(self):
        self.headers = LoginPO().get_headers("wpg账号", par_dir, yml_name, login_api_url)

    def teardown_class(self):
        pass

    @allure.story("新增群组")
    def test_add_group(self):
        params = {
            "code": "",
            "createBy": "001",
            "createTime": "",
            "delFlag": "0",
            "disableFlag": "0",
            "groupName": "测试组",
            "groupType": "0",
            "id": "",
            "parentId": "",
            "pwGroupId": 0,
            "pwGroupParentId": 0,
            "remark": "",
            "stepSort": 0,
            "tenantId": "",
            "updateBy": "",
            "updateTime": "",
            "version": 0
        }
        response = self.add_group(headers=self.headers, params=params)
        assert response["status"] == "complete"

    @allure.story("查询群组")
    def test_query_group(self):
        params = {
            "disableFlag": "",
            "name": "",
            "page": {
                "asc": [],
                "ascs": [],
                "current": 0,
                "desc": [],
                "descs": [],
                "hitCount": True,
                "optimizeCountSql": True,
                "orders": [
                    {
                        "asc": True,
                        "column": ""
                    }
                ],
                "pages": 0,
                "records": [
                    {
                        "children": [
                            {
                                "children": [
                                    {}
                                ],
                                "code": "",
                                "createBy": "",
                                "createTime": "",
                                "delFlag": "",
                                "disableFlag": "",
                                "groupName": "",
                                "groupType": "",
                                "id": "",
                                "parentId": "",
                                "pwGroupId": 0,
                                "pwGroupParentId": 0,
                                "remark": "",
                                "stepSort": 0,
                                "tenantId": "",
                                "updateBy": "",
                                "updateTime": "",
                                "version": 0
                            }
                        ],
                        "code": "",
                        "createBy": "",
                        "createTime": "",
                        "delFlag": "",
                        "disableFlag": "",
                        "groupName": "",
                        "groupType": "",
                        "id": "",
                        "parentId": "",
                        "pwGroupId": 0,
                        "pwGroupParentId": 0,
                        "remark": "",
                        "stepSort": 0,
                        "tenantId": "",
                        "updateBy": "",
                        "updateTime": "",
                        "version": 0
                    }
                ],
                "searchCount": True,
                "size": 0,
                "total": 0
            }
        }
        response = self.query_group(headers=self.headers, params=params)
        assert response["status"] == "complete"

    @allure.story("新增用户")
    def test_add_user(self):
        params = {
            "sysGroupId": "",
            "userIds": []
        }
        response = self.add_user(headers=self.headers, params=params)
        assert response["status"] == "complete"
