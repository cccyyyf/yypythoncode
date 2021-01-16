# coding=utf-8
# Time : 2020/11/13 15:00
# Author : huxin
from objects.interface.DevicePlat.DsIndustryTemplatePO import DsIndustryTemplatePO
from objects.interface.DevicePlat.LoginPO import LoginPO
from objects.interface.utils.PropertiesUtil import *
from RootPath import *
from objects.interface.utils.DateTimeUtil import *
import allure
import pytest

@allure.feature("行业设备模板")
class TestDsIndustryTemplate(DsIndustryTemplatePO):

    nowTime = get_time_stamp()
    templateName = "autoTest" + str(nowTime)
    def setup_class(self):
        self.headers = LoginPO().get_headers(role="wpg账号")

    def teardown_class(self):
        #清空数据
        pass

    @allure.story("添加行业设备模板")
    def test_add_IndustryTemplate(self):
        body={"templateName":self.templateName,"templateType":"Water_Plant","labelId":"","attribute":"[]"}
        result = self.add_IndustryTemplate(headers=self.headers,body=body)
        assert result["resultData"] == "添加成功"

        #数据库校验
        sql = "select count(*) from ds_industry_template where template_name = '%s'" %(self.templateName)
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["count(*)"] == 1

    @allure.story("修改行业设备模板")
    def test_modify_IndustryTemplate(self):
        #获取id
        id_sql = "select id from ds_industry_template where template_name = '%s'" % (self.templateName)
        id_result = self.get_DB_data(sql=id_sql)
        id = id_result[0]["id"]
        body={"id":id,"templateName":self.templateName,"templateType":"Water_Plant","labelId":"","attribute":"[]","remark":"测试备注"}
        result = self.modify_IndustryTemplate(headers=self.headers, body=body)
        assert result["resultData"] == "修改成功"

        # 数据库校验
        sql = "select remark from ds_industry_template where template_name = '%s'" % (self.templateName)
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["remark"] == "测试备注"

    @allure.story("模板源-查询基础模板")
    def test_search_BaseList(self):
        body={"currentPage":1,"pageSize":20,"templateType":"","templateNameOrNum":""}
        result = self.search_BaseSourceList(headers=self.headers,body=body)
        assert result["count"] > 0
        assert len(result["resultData"]) > 0

    @allure.story("模板源-查询用户模板源列表")
    def test_search_UserList(self):
        body={"currentPage":1,"pageSize":20,"templateType":"","templateNameOrNum":""}
        result = self.search_UserSourceList(headers=self.headers,body=body)
        assert result["count"] > 0
        assert len(result["resultData"]) > 0

    @allure.story("查询行业设备模板")
    def test_search_List(self):
        body={"currentPage":1,"pageSize":20,"keyword":"autoTest","orderBy":""}
        result = self.search_List(headers=self.headers,body=body)
        assert result["count"] > 0
        assert len(result["resultData"]) > 0
        assert "autoTest" in result["resultData"][0]["templateName"]

    @allure.story("查看模板详情")
    def test_search_IndustryTemplateDetails(self):
        id_sql = "select id from ds_industry_template where template_name = '%s'" % (self.templateName)
        id_result = self.get_DB_data(sql=id_sql)
        id = id_result[0]["id"]
        result = self.search_IndustryTemplateDetails(headers=self.headers,templateId=id)
        assert len(result["resultData"]) > 0
        assert "autoTest" in result["resultData"]["templateName"]

    @allure.story("excel导出")
    def test_export_excel(self):
        body = {"currentPage":1,"pageSize":20,"order":"","orderBy":""}
        result = self.export_excel(headers=self.headers,body=body)

    @allure.story("模板下载")
    def test_export_template(self):
        #获取要导出模板的id
        id_sql = "select id from ds_industry_template where template_name = '%s'" % (self.templateName)
        id_result = self.get_DB_data(sql=id_sql)
        id = id_result[0]["id"]
        body = [id]
        result = self.export_Template(headers=self.headers,body=body)

    @allure.story("获取当前用户能看到的行业设备模板")
    def test_get_templates(self):
        #切换用户headers

        result = self.get_IndustryTemplates(headers=self.headers)
        assert len(result["resultData"]) >0

    @allure.story("获取行业设备模板标签")
    def test_get_labels(self):
        id_sql = "select id from ds_industry_template where template_name = '%s'" % (self.templateName)
        id_result = self.get_DB_data(sql=id_sql)
        id = id_result[0]["id"]

        result = self.get_labels(headers=self.headers,templateId=id)
        assert len(result["resultData"]) == 0
        assert result["success"] == True

    @allure.story("删除行业设备模板")
    def test_dele_DsIndustryTemplate(self):
        #获取要删除的id
        id_sql = "select id from ds_industry_template where template_name = '%s'" % (self.templateName)
        id_result = self.get_DB_data(sql=id_sql)
        id = id_result[0]["id"]

        result = self.dele_DsIndustryTemplate(headers=self.headers,templateId=id)
        assert result["resultData"] == "删除成功"

        #校验数据库
        sql = "select id from ds_industry_template where id = '%s'" % (id)
        sql_result = self.get_DB_data(sql=sql)
        assert len(sql_result) == 0

