# coding=utf-8
# Time : 2020/12/06 10:01
# Author : huxin
from objects.interface.DevicePlat.DsIndustryTemplatePO import DsIndustryTemplatePO
from objects.interface.DevicePlat.LoginPO import LoginPO
from objects.interface.utils.PropertiesUtil import *
from RootPath import *
from objects.interface.utils.DateTimeUtil import *
import allure
import pytest

@allure.feature("行业设备模板对外接口")
class TestOutDsIndustryTemplate(DsIndustryTemplatePO):

    nowTime = get_time_stamp()
    templateName = "autoTest" + str(nowTime)
    templateId = ""
    def setup_class(self):
        self.headers = LoginPO().get_headers(role="wpg账号")
        #添加模板
        body={"templateName":self.templateName,"templateType":"Water_Plant","labelId":"","attribute":"[]"}
        result = DsIndustryTemplatePO().add_IndustryTemplate(headers=self.headers,body=body)

    def teardown_class(self):
        #清空数据
        id_sql = "select id from ds_industry_template where template_name = '%s'" % (self.templateName)
        id_result = DsIndustryTemplatePO().get_DB_data(sql=id_sql)
        id = id_result[0]["id"]
        result = DsIndustryTemplatePO().dele_DsIndustryTemplate(headers=self.headers,templateId=id)

    @allure.story("根据条件查询行业设备基础模板,查询所有======废弃")
    def get_BaseList(self):
        body = {
            "currentPage": 1,
            "delFlag": 0,
            "keyword": "",
            "labelId": [],
            "order": "",
            "orderBy": "",
            "pageSize": 10,
            "templateType": "",
            "tenantId": "",
            "templateNameOrNum": ""
        }
        result = self.get_BaseList(headers=self.headers,body=body)
        assert result["count"] > 0
        assert len(result["resultData"]) > 0

    @allure.story("根据条件查询行业设备基础模板,根据关键字查询======废弃")
    def get_BaseList_r(self):
        body = {
            "currentPage": 1,
            "delFlag": 0,
            "keyword": "",
            "labelId": [],
            "order": "",
            "orderBy": "",
            "pageSize": 10,
            "templateType": "",
            "tenantId": "",
            "templateNameOrNum": self.templateName
        }
        result = self.get_BaseList(headers=self.headers,body=body)
        assert result["count"] > 0
        assert result["resultData"][0]["templateName"] == self.templateName

    @allure.story("根据条件查询行业设备用户模板,查询所有=====废弃")
    def get_Userlist(self):
        body = {
            "currentPage": 1,
            "delFlag": 0,
            "keyword": "",
            "labelId": [],
            "order": "",
            "orderBy": "",
            "pageSize": 10,
            "templateType": "",
            "tenantId": "",
            "templateNameOrNum": ""
        }
        result = self.get_Userlist(headers=self.headers,body=body)
        assert result["count"] > 0
        assert len(result["resultData"]) > 0

    @allure.story("根据条件查询行业设备用户模板,根据关键字查询====废弃")
    def get_Userlist_r(self):
        body = {
            "currentPage": 1,
            "delFlag": 0,
            "keyword": "",
            "labelId": [],
            "order": "",
            "orderBy": "",
            "pageSize": 10,
            "templateType": "",
            "tenantId": "",
            "templateNameOrNum": self.templateName
        }
        result = self.get_Userlist(headers=self.headers,body=body)
        assert result["count"] > 0
        assert result["resultData"][0]["templateName"] == self.templateName
        #获取模板id
        TestOutDsIndustryTemplate.templateId = result["resultData"][0]["id"]

    @allure.story("根据条件查询行业设备模板,查询全部")
    def test_get_queryPage(self):
        body = {
            "currentPage": 1,
            "delFlag": 0,
            "keyword": "",
            "labelId": [],
            "order": "",
            "orderBy": "",
            "pageSize": 10,
            "templateType": "",
            "tenantId": "",
            "templateNameOrNum": ""
        }
        result = self.get_queryPage(headers=self.headers,body=body)
        assert result["count"] > 0
        assert len(result["resultData"]) > 0

    @allure.story("根据条件查询行业设备模板,根据关键字查询")
    def test_get_queryPage_r(self):
        body = {
            "currentPage": 1,
            "delFlag": 0,
            "keyword": self.templateName,
            "labelId": [],
            "order": "",
            "orderBy": "",
            "pageSize": 10,
            "templateType": "",
            "tenantId": "",
            "templateNameOrNum": ""
        }
        result = self.get_queryPage(headers=self.headers,body=body)
        assert result["count"] > 0
        assert result["resultData"][0]["templateName"] == self.templateName
        #获取模板id
        TestOutDsIndustryTemplate.templateId = result["resultData"][0]["id"]

    @allure.story("根据id查询行业设备模板详情")
    def test_get_detail(self):
        result = self.get_detail(headers=self.headers,templateId=self.templateId)
        assert result["resultData"]["templateName"] == self.templateName