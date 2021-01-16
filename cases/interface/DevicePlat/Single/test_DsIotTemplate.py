# coding=utf-8
# Time : 2020/11/3 15:00
# Author : huxin
from objects.interface.DevicePlat.DsIotTemplatePO import DsIotTemplatePO
from objects.interface.DevicePlat.LoginPO import LoginPO
from objects.interface.DevicePlat.DsPointPO import DsPointPO
from objects.interface.utils.PropertiesUtil import *
from RootPath import *
from objects.interface.utils.DateTimeUtil import *
import allure
import pytest
import random

@allure.feature("Iot设备模板")
class TestDsIotTemplate(DsIotTemplatePO):

    nowTime = get_time_stamp()
    templateNum = "autoTest" + str(nowTime)
    def setup_class(self):
        self.headers = LoginPO().get_headers(role="wpg账号")
        #新增监测量
        self.pointCode = "auto" + str(random.randint(1, 10000))
        self.pointName = "auto" + str(random.randint(1, 10000))
        self.pointMemo = "自动化测试_监测量名称" + str(random.randint(1, 10000))
        body_point = {
            "pointCode": self.pointCode,
            "pointName": self.pointName,
            "pointMemo": self.pointMemo,
            "pointType": "4",
            "dataType": "uint",
            "gatewayFlag": True,
        }
        response_point = DsPointPO().add_point(headers=self.headers, body=body_point)
        assert response_point["resultData"] == "新增成功"
        sql = "select id from ds_point where point_code = '%s'" % self.pointCode
        db_res = DsPointPO().get_DB_data(sql=sql)
        self.point_id = db_res[0]["id"]

    def teardown_class(self):
        #清空数据
        sql = "delete from ds_iot_template where template_name like '%接口自动化测试%' "
        result = DsIotTemplatePO().get_DB_data(sql=sql)
        #删除监测量数据
        response = DsPointPO().delete_point(point_id=self.point_id, headers=self.headers)

    @allure.story("添加iot模板-网关类")
    def test_add_iotTemplate_gateway(self):

        body={
            "attribute": [{
                "__config__": {
                    "label": "单行文本",
                    "labelWidth": None,
                    "showLabel": True,
                    "changeTag": True,
                    "tag": "el-input",
                    "tagIcon": "input",
                    "required": True,
                    "layout": "colFormItem",
                    "span": 24,
                    "document": "https://element.eleme.cn/#/zh-CN/component/input",
                    "regList": [],
                    "formId": 108,
                    "renderKey": "1081604454704308"
                },
                "__slot__": {
                    "prepend": "",
                    "append": "",
                    "suffix": ""
                },
                "placeholder": "请输入单行文本",
                "style": {
                    "width": "100%"
                },
                "clearable": True,
                "maxlength": None,
                "show-word-limit": False,
                "readonly": False,
                "disabled": False,
                "__vModel__": "field108"
            }],
            "templateNum": self.templateNum,
            "templateName": "接口自动化测试名称" + str(self.nowTime),
            "templateType": "gateway",
            "collectorType": "DTU",
            "topic": "test/test/test",
            "remark": "测试备注",
            "templatePointList": [
                {
                    "id": self.point_id,
                    "pointId": self.point_id,
                    "pointCode": self.pointCode,
                    "pointName": self.pointName,
                    "pointMemo": self.pointMemo,
                    "pointType": 4,
                    "dataType": "uint",
                    "ratio": 1.000000
                }
            ],
            "labelIdList": ["938549a71d863e22a3fca23d4f766b03"]
        }
        result = self.add_iotTemplate(headers=self.headers,body=body)
        assert result["resultData"] == "新增成功"

        #数据库校验
        sql = "select count(*) from ds_iot_template where template_num = '%s'" %(self.templateNum)
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["count(*)"] == 1

    @allure.story("添加iot模板-传感类")
    def test_add_iotTemplate_sensor(self):
        templateNum2 = "autoTest" + str(self.nowTime + 1)
        body={
            "attribute": [{
                "__config__": {
                    "label": "单行文本",
                    "labelWidth": None,
                    "showLabel": True,
                    "changeTag": True,
                    "tag": "el-input",
                    "tagIcon": "input",
                    "required": True,
                    "layout": "colFormItem",
                    "span": 24,
                    "document": "https://element.eleme.cn/#/zh-CN/component/input",
                    "regList": [],
                    "formId": 108,
                    "renderKey": "1081604454704308"
                },
                "__slot__": {
                    "prepend": "",
                    "append": "",
                    "suffix": ""
                },
                "placeholder": "请输入单行文本",
                "style": {
                    "width": "100%"
                },
                "clearable": True,
                "maxlength": None,
                "show-word-limit": False,
                "readonly": False,
                "disabled": False,
                "__vModel__": "field108"
            }],
            "templateNum": templateNum2,
            "templateName": "接口自动化测试名称" + str(self.nowTime +1),
            "templateType": "sensor",
            "remark": "测试备注",
            "templatePointList": [
                {
                    "id": self.point_id,
                    "pointId": self.point_id,
                    "pointCode": self.pointCode,
                    "pointName": self.pointName,
                    "pointMemo": self.pointMemo,
                    "pointType": 4,
                    "dataType": "uint",
                    "ratio": 1.000000
                }
            ],
            "labelIdList": ["938549a71d863e22a3fca23d4f766b03"]
        }
        result = self.add_iotTemplate(headers=self.headers,body=body)
        assert result["resultData"] == "新增成功"

        #数据库校验
        sql = "select count(*) from ds_iot_template where template_num = '%s'" %(templateNum2)
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["count(*)"] == 1

    @allure.story("修改iot模板")
    def test_modify_iotTemplate(self):
        #获取id
        id_sql = "select id from ds_iot_template where template_num = '%s'" % (self.templateNum)
        id_result = self.get_DB_data(sql=id_sql)
        id = id_result[0]["id"]
        body = {
            "id": id,
            "tenantId": "001",
            "attribute": [{
                "__config__": {
                    "label": "单行文本",
                    "labelWidth": None,
                    "showLabel": True,
                    "changeTag": True,
                    "tag": "el-input",
                    "tagIcon": "input",
                    "required": True,
                    "layout": "colFormItem",
                    "span": 24,
                    "document": "https://element.eleme.cn/#/zh-CN/component/input",
                    "regList": [],
                    "formId": 108,
                    "renderKey": "1081604454704308"
                },
                "__slot__": {
                    "prepend": "",
                    "append": "",
                    "suffix": ""
                },
                "placeholder": "请输入单行文本",
                "style": {
                    "width": "100%"
                },
                "clearable": True,
                "maxlength": None,
                "show-word-limit": False,
                "readonly": False,
                "disabled": False,
                "__vModel__": "field108"
            }],
            "templateNum": self.templateNum,
            "templateName": "接口自动化测试名称" + str(self.nowTime),
            "templateType": "gateway",
            "collectorType": "FBOX",
            "topic": "test/test/test",
            "remark": "测试备注",
            "templatePointList": [
                {
                    "id": self.point_id,
                    "pointId": self.point_id,
                    "pointCode": self.pointCode,
                    "pointName": self.pointName,
                    "pointMemo": self.pointMemo,
                    "pointType": 4,
                    "dataType": "uint",
                    "ratio": 1.000000
                }
            ],
            "labelIdList": ["938549a71d863e22a3fca23d4f766b03"]
        }
        result = self.modify_iotTemplate(headers=self.headers, body=body)
        assert result["resultData"] == "修改成功"

        # 数据库校验
        sql = "select collector_type from ds_iot_template where template_num = '%s'" % (self.templateNum)
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["collector_type"] == "FBOX"

    @allure.story("模板源-查询基础模板")
    def test_search_BaseSourceList(self):
        body={"currentPage":1,"pageSize":20,"templateType":"","templateNameOrNum":""}
        result = self.search_BaseSourceList(headers=self.headers,body=body)
        assert result["count"] > 0
        assert len(result["resultData"]) > 0

    @allure.story("模板源-查询用户模板源列表")
    def test_search_UserSourceList(self):
        body={"currentPage":1,"pageSize":20,"templateType":"","templateNameOrNum":""}
        result = self.search_UserSourceList(headers=self.headers,body=body)
        assert result["count"] > 0
        assert len(result["resultData"]) > 0

    @allure.story("查询IOT设备模板")
    def test_search_List(self):
        body={"currentPage":1,"pageSize":20,"templateName":"接口自动化","orderBy":""}
        result = self.search_List(headers=self.headers,body=body)
        assert result["count"] > 0
        assert len(result["resultData"]) > 0
        assert "接口自动化" in result["resultData"][0]["templateName"]
    '''
    该接口已废弃
    @allure.story("查看模板详情")
    def test_search_IotTemplateDetails(self):
        body = {"currentPage":1,"pageSize":20,"orderBy":"","templateName":"接口自动化测试"}
        result = self.search_IotTemplateDetails(headers=self.headers,body=body)
        assert result["count"] > 0
        assert len(result["resultData"]) > 0
        assert "接口自动化" in result["resultData"][0]["templateName"]
    '''
    @allure.story("excel导出")
    def test_export_excel(self):
        body = {"currentPage":1,"pageSize":20}
        result = self.export_excel(headers=self.headers,body=body)

    @allure.story("模板下载")
    def test_export_template(self):
        #获取要导出模板的id
        id_sql = "select id from ds_iot_template where template_num = '%s'" % (self.templateNum)
        id_result = self.get_DB_data(sql=id_sql)
        id = id_result[0]["id"]

        body = [id]
        result = self.export_Template(headers=self.headers,body=body)

    @allure.story("获取待克隆模板信息")
    def test_copy_iotTemplate(self):
        #获取id
        id_sql = "select id from ds_iot_template where template_num = '%s'" % (self.templateNum)
        id_result = self.get_DB_data(sql=id_sql)
        id = id_result[0]["id"]

        result = self.copy_iotTemplate(headers=self.headers,id=id)
        assert result["resultData"]["points"] is not None

    @allure.story("删除iot模板")
    def test_dele_DsIotTemplate(self):
        #获取要删除的id
        id_sql = "select id from ds_iot_template where template_num = '%s'" % (self.templateNum)
        id_result = self.get_DB_data(sql=id_sql)
        id = id_result[0]["id"]

        result = self.dele_DsIotTemplate(headers=self.headers,id=id)
        assert result["resultData"] == "删除成功"

        #校验数据库
        sql = "select id from ds_iot_template where id = '%s'" % (id)
        sql_result = self.get_DB_data(sql=sql)
        assert len(sql_result) == 0

