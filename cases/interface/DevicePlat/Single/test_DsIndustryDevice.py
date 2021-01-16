# coding=utf-8
# Time : 2020/12/8 9:34
# Author : huxin
from RootPath import RootPath
from objects.interface.DevicePlat.LoginPO import LoginPO
from objects.interface.DevicePlat.DsStationPO import DsStationPO
from objects.interface.DevicePlat.DsPointPO import DsPointPO
from objects.interface.DevicePlat.DsIndustryDevicePO import DsIndustryDevicePO
from objects.interface.DevicePlat.DsIotTemplatePO import DsIotTemplatePO
from objects.interface.DevicePlat.DsIotDevicePO import DsIotDevicePO
from objects.interface.DevicePlat.DsIndustryTemplatePO import DsIndustryTemplatePO
import allure
import pytest

from objects.interface.utils.DateTimeUtil import get_time_stamp
from objects.interface.utils.PropertiesUtil import *
import random


@allure.feature("行业设备信息")
class TestDsIndustryDevice(DsIndustryDevicePO):

    id_standaloned = ""
    id_complete = ""
    def setup_class(self):
        self.headers = LoginPO().get_headers(role="wpg账号")
        public_path = RootPath.getDevicePlatPath() + "Public.yml"
        self.staion = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="站点管理")
        self.deviceInfo = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="行业设备信息")
        self.temp = str(random.randint(1, 10000))
        self.pointCode = "auto" + self.temp
        self.pointName = "auto" + self.temp
        self.pointMemo = "自动化测试_监测量名称" + self.temp
        self.nowTime = get_time_stamp()
        self.deviceName = "自动化测试设备" + str(self.nowTime)
        # 添加监测量
        body_point = {
            "pointCode": self.pointCode,
            "pointName": self.pointName,
            "pointMemo": self.pointMemo,
            "pointType": "4",
            "dataType": "unit",
            "gatewayFlag": True
        }
        response_point = DsPointPO().add_point(headers=self.headers, body=body_point)
        sql = "select id from ds_point where point_code = '%s'" % self.pointCode
        db_res = DsPointPO().get_DB_data(sql=sql)
        self.point_id = db_res[0]["id"]

        # 添加区域
        body_area = {
            "id": "",
            "areaName": self.staion["areaName"],
            "parentId": "0"
        }
        response_area = DsStationPO().add_area(headers=self.headers, body=body_area)
        area_id_sql = "SELECT id FROM ds_area where area_name = '%s'" % (self.staion["areaName"])
        id_result =  DsStationPO().get_DB_data(sql=area_id_sql)
        self.area_id = id_result[0]["id"]
        # 添加站点
        body_staion = {
            "id": "",
            "stationName": self.staion["stationName"],
            "stationCode": "station01",
            "areaId": self.area_id,
            "shorthand": "pinyinjianxie01",
            "stationType": "PressurePoint",
            "lati": "1",
            "longi": "2",
            "addr": "接口自动化测试地址",
            "labelId": "",
            "remark": ""
        }
        result_staion = DsStationPO().add_station(headers=self.headers, body=body_staion)
        sql_id = "SELECT id FROM ds_station where station_name = '%s'" % (self.staion["stationName"])
        id_result = DsStationPO().get_DB_data(sql=sql_id)
        self.station_id = id_result[0]["id"]

        # 添加行业设备模板
        self.templateName = "autoTest" + str(self.nowTime + 1)
        body = {"templateName": self.templateName, "templateType": "Water_Plant", "labelId": "", "attribute": "[]"}
        result = DsIndustryTemplatePO().add_IndustryTemplate(headers=self.headers, body=body)
        id_sql = "select id from ds_industry_template where template_name = '%s'" % (self.templateName)
        id_result = DsIndustryTemplatePO().get_DB_data(sql=id_sql)
        self.template_id = id_result[0]["id"]

        # 添加iot模板(gateway)
        self.templateNum = "autoTest" + str(self.nowTime + 1)
        body_template = {
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
            "collectorType": "HWGATEWAY",
            "topic": "test/test/test",
            "remark": "测试备注",
            "templatePointList": [
                {
                    "id": self.point_id,
                    "pointId": self.point_id,
                    "pointCode": self.pointCode,
                    "pointName": self.pointName,
                    "pointMemo": self.pointMemo,
                    "pointType": 1,
                    "dataType": "word",
                    "ratio": 1.000000
                }
            ],
            "labelIdList": ["938549a71d863e22a3fca23d4f766b03"]
        }
        result_template = DsIotTemplatePO().add_iotTemplate(headers=self.headers, body=body_template)
        sql = "select id from ds_iot_template where template_num = '%s'" % (self.templateNum)
        sql_result = DsIotTemplatePO().get_DB_data(sql=sql)
        self.templateId = sql_result[0]["id"]

        # 添加iot设备
        self.deviceId_iot = str(self.nowTime)
        body_device = {
            "iotDeviceBaseDTO": {
                "id": "",
                "attribute": "[{\"clearable\":true,\"__config__\":{\"formId\":105,\"defaultValue\":null,\"document\":\"https://element.eleme.cn/#/zh-CN/component/date-picker\",\"labelWidth\":null,\"label\":\"日期选择\",\"showLabel\":true,\"required\":true,\"renderKey\":\"1051604454071789\",\"layout\":\"colFormItem\",\"tagIcon\":\"date\",\"changeTag\":true,\"tag\":\"el-date-picker\",\"regList\":[],\"span\":24},\"readonly\":false,\"format\":\"yyyy-MM-dd\",\"value-format\":\"yyyy-MM-dd\",\"__vModel__\":\"field105\",\"style\":{\"width\":\"100%\"},\"disabled\":false,\"placeholder\":\"请选择日期选择\",\"type\":\"date\"}]",
                "attributeValue": "{\"field105\":\"2020-11-05\"}",
                "templateId": self.templateId,
                "deviceName": self.deviceName,
                "deviceId": self.deviceId_iot,
                "stationId": self.station_id,
                "iotId": "",
                "collectorId": self.deviceId_iot,
                "factoryName": "测试厂家名称",
                "deviceModel": "dt-123e",
                "productTime": "2020-11-05",
                "connectType": "5G",
                "protocolType": "UDP/TCP",
                "moreFlag": 0
            },
            "iotSubDeviceDTOList": [],
            "iotDevicePointDTOList": [
                {
                    "controlStatus": False,
                    "dataSort": None,
                    "dataType": "word",
                    "dataTypeName": "word",
                    "id": self.point_id,
                    "maxValue": None,
                    "minValue": None,
                    "pointCode": self.pointCode,
                    "pointId": self.point_id,
                    "pointMemo": self.pointMemo,
                    "pointName": self.pointName,
                    "pointType": "1",
                    "pointTypeName": "监测压力",
                    "pointUnit": None,
                    "pointUnitName": "",
                    "ratio": 1,
                    "templateId": self.templateId
                }]
        }
        result_device = DsIotDevicePO().add_iotDevice(headers=self.headers, body=body_device)

    def teardown_class(self):
        # 删除行业设备模板
        result = DsIndustryTemplatePO().dele_DsIndustryTemplate(headers=self.headers, templateId=self.template_id)
        # 删除iot设备
        sql = "select id from ds_iot_device where device_name = '%s'" % (self.deviceName)
        sql_result = DsIotDevicePO().get_DB_data(sql=sql)
        id = sql_result[0]["id"]
        result = DsIotDevicePO().dele_iotDevices(headers=self.headers, ids=id)
        # 删除iot模板
        id_sql = "select id from ds_iot_template where template_num = '%s'" % (self.templateNum)
        id_result = DsIotTemplatePO().get_DB_data(sql=id_sql)
        id = id_result[0]["id"]
        result = DsIotTemplatePO().dele_DsIotTemplate(headers=self.headers, id=id)
        # 删除站点
        result = DsStationPO().dele_station(headers=self.headers, ids=self.station_id)
        # 删除区域
        result = DsStationPO().dele_area(headers=self.headers, entityId=self.area_id)
        # 删除监测量
        sql = "select id from ds_point where point_code = '%s'" % self.pointCode
        db_res = DsPointPO().get_DB_data(sql=sql)
        response = DsPointPO().delete_point(point_id=db_res[0]["id"], headers=self.headers)
        assert response["resultData"] == "删除成功"

    @allure.story("新增行业设备信息，独立设备")
    def test_add_DsIndustryDevice(self):
        body = {
            "dsIndustryDeviceDTO": {
                "labelId": "",
                "deviceName": self.deviceInfo["deviceName"]+"standaloned",
                "deviceId": self.deviceInfo["deviceId"]+"standaloned",
                "templateName": self.templateName,
                "station": self.staion["stationName"],
                "deviceType": "industry_standaloned",
                "stationId": self.station_id,
                "templateId": self.template_id,
                "qrCode": "/upload/front/images/20201208/1336125320995659778.png",
                "attribute": "[{\"__config__\":{\"formId\":102,\"document\":\"https://element.eleme.cn/#/zh-CN/component/input\",\"labelWidth\":null,\"label\":\"多行文本\",\"showLabel\":true,\"required\":true,\"renderKey\":\"1021606784700502\",\"layout\":\"colFormItem\",\"tagIcon\":\"textarea\",\"changeTag\":true,\"tag\":\"a-textarea\",\"regList\":[],\"span\":24},\"readonly\":false,\"maxlength\":null,\"__vModel__\":\"field102\",\"style\":{\"width\":\"100%\"},\"disabled\":false,\"placeholder\":\"请输入多行文本\",\"show-word-limit\":false,\"type\":\"textarea\",\"autosize\":{\"minRows\":4,\"maxRows\":4}}]",
                "attributeValue": "[{\"field102\":\"填写的属性信息\"}]"
            },
            "dsIndustryPointDTO": [{
                "childIndustryName": None,
                "dataType": "uint",
                "deviceId": self.deviceId_iot,
                "deviceName": self.deviceName,
                "id": None,
                "industryId": None,
                "pointCode": self.pointCode,
                "pointId": self.deviceId_iot+"-" +self.point_id,
                "pointMemo": self.pointMemo,
                "pointName": self.pointName,
                "pointType": "4",
                "ratio": 1,
                "value": self.deviceId_iot+"-" +self.point_id
            }]
        }
        result = self.add_DsIndustryDevice(headers=self.headers,body=body)
        assert result["resultData"] == "添加成功"
        #校验数据库
        sql = "select count(*) ,id from ds_industry_device where device_name = '%s'" %(self.deviceInfo["deviceName"] +"standaloned")
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["count(*)"] == 1
        #获取设备id
        TestDsIndustryDevice.id_standaloned = sql_result[0]["id"]

    @allure.story("新增行业设备信息，成套设备")
    def test_add_DsIndustryDevice2(self):
        body = {
            "dsIndustryDeviceDTO": {
                "labelId": "",
                "deviceName": self.deviceInfo["deviceName"]+ "complete",
                "deviceId": self.deviceInfo["deviceId"]+"complete",
                "templateName": self.templateName,
                "station": self.staion["stationName"],
                "deviceType": "complete_equipment",
                "stationId": self.station_id,
                "templateId": self.template_id,
                "qrCode": "/upload/front/images/20201208/1336133209206415362.png",
                "attribute": "[{\"__config__\":{\"formId\":102,\"document\":\"https://element.eleme.cn/#/zh-CN/component/input\",\"labelWidth\":null,\"label\":\"多行文本\",\"showLabel\":true,\"required\":true,\"renderKey\":\"1021606784700502\",\"layout\":\"colFormItem\",\"tagIcon\":\"textarea\",\"changeTag\":true,\"tag\":\"a-textarea\",\"regList\":[],\"span\":24},\"readonly\":false,\"maxlength\":null,\"__vModel__\":\"field102\",\"style\":{\"width\":\"100%\"},\"disabled\":false,\"placeholder\":\"请输入多行文本\",\"show-word-limit\":false,\"type\":\"textarea\",\"autosize\":{\"minRows\":4,\"maxRows\":4}}]",
                "attributeValue": "[{\"field102\":\"测试属性文本\"}]"
            },
            "dsIndustryPointDTO": [{
                "childIndustryName": self.deviceInfo["deviceName"]+ "standaloned",
                "dataType": "uint",
                "deviceId": self.deviceId_iot,
                "deviceName": self.deviceName+ "('%s')"%(self.deviceInfo["deviceName"]+ "standaloned"),
                "id": self.id_standaloned + "-" + self.deviceId_iot+"-" +self.point_id,
                "industryId": self.id_standaloned ,
                "pointCode": self.pointCode,
                "pointId": self.deviceId_iot+"-" +self.point_id,
                "pointMemo": self.pointMemo,
                "pointName": self.pointName,
                "pointType": "4",
                "ratio": 1,
                "value": self.id_standaloned + "-" + self.deviceId_iot+"-" +self.point_id
            }],
            "dsIndustryChildRelDTO": [{
                "childId": self.id_standaloned ,
                "type": 0
            }]
        }
        result = self.add_DsIndustryDevice(headers=self.headers,body=body)
        assert result["resultData"] == "添加成功"
        #校验数据库
        sql = "select count(*),id from ds_industry_device where device_name = '%s'" %(self.deviceInfo["deviceName"] +"complete")
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["count(*)"] == 1
        # 获取设备id
        TestDsIndustryDevice.id_complete = sql_result[0]["id"]

    @allure.story("修改行业设备信息")
    def test_update_DsIndustryDevice(self):
        body = {
            "dsIndustryDeviceDTO": {
                "labelId": "",
                "deviceName": self.deviceInfo["deviceNameNew"]+"standaloned",
                "deviceId": self.deviceInfo["deviceId"]+"standaloned",
                "templateName": self.templateName,
                "station": self.staion["stationName"],
                "deviceType": "industry_standaloned",
                "stationId": self.station_id,
                "templateId": self.template_id,
                "qrCode": "/upload/front/images/20201208/1336125320995659778.png",
                "attribute": "[{\"__config__\":{\"formId\":102,\"document\":\"https://element.eleme.cn/#/zh-CN/component/input\",\"labelWidth\":null,\"label\":\"多行文本\",\"showLabel\":true,\"required\":true,\"renderKey\":\"1021606784700502\",\"layout\":\"colFormItem\",\"tagIcon\":\"textarea\",\"changeTag\":true,\"tag\":\"a-textarea\",\"regList\":[],\"span\":24},\"readonly\":false,\"maxlength\":null,\"__vModel__\":\"field102\",\"style\":{\"width\":\"100%\"},\"disabled\":false,\"placeholder\":\"请输入多行文本\",\"show-word-limit\":false,\"type\":\"textarea\",\"autosize\":{\"minRows\":4,\"maxRows\":4}}]",
                "attributeValue": "[{\"field102\":\"填写的属性信息\"}]",
                "id": self.id_standaloned
            },
            "dsIndustryPointDTO": [{
                "childIndustryName": None,
                "dataType": "uint",
                "deviceId": self.deviceId_iot,
                "deviceName": self.deviceName,
                "id": None,
                "industryId": None,
                "pointCode": self.pointCode,
                "pointId": self.deviceId_iot+"-" +self.point_id,
                "pointMemo": self.pointMemo,
                "pointName": self.pointName,
                "pointType": "4",
                "ratio": 1,
                "value": self.deviceId_iot+"-" +self.point_id
            }]
        }
        result = self.update_DsIndustryDevice(headers=self.headers,body=body)
        assert result["resultData"] == "修改成功"
        #校验数据库
        sql = "select count(*) ,id from ds_industry_device where device_name = '%s'" %(self.deviceInfo["deviceNameNew"] +"standaloned")
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["count(*)"] == 1

    @allure.story("生成设备二维码")
    def test_get_deviceQrCode(self):
        body = {
            "deviceId": "1211",
            "stationId": "222"
        }
        result = self.get_deviceQrCode(headers=self.headers,body=body)
        assert "png" in result["resultData"]

    @allure.story("根据行业设备id查详情")
    def test_get_detail(self):
        result = self.get_detail(headers=self.headers,industryId=self.id_standaloned)
        assert result["resultData"]["devicePointVOS"] is not None
        assert result["resultData"]["industryDeviceVO"]["id"] == self.id_standaloned

    @allure.story("行业设备excel导出")
    def test_export_excel(self):
        body = {"keyWord":"","labelId":"","currentPage":1,"pageSize":20,"orderBy":""}
        result = self.export_excel(headers=self.headers,body=body)

    @allure.story("根据条件查询行业设备信息列表")
    def test_get_list(self):
        body={
            "keyWord": "",
            "labelId": "",
            "currentPage": 1,
            "pageSize": 20,
            "orderBy": "",
            "stationIds": self.station_id #站点”设备测试“
        }
        result = self.get_list(headers=self.headers,body=body)
        assert result["count"] > 0
        assert len(result["resultData"]) > 0

    @allure.story("实时数据过滤")
    def test_search_realTimeData(self):
        body = {"industryId":self.id_standaloned,"keyWord":None}
        result = self.search_realTimeData(headers=self.headers,params=body)
        assert result["success"] == True
        assert result["status"] == "complete"

    @allure.story("行业设备id查实时数据")
    def test_get_realTimeData(self):
        result = self.get_realTimeData(headers=self.headers,industryId=self.id_standaloned)
        assert result["success"] == True
        assert result["status"] == "complete"

    @allure.story("根据条件查询行业设备模板")
    def test_get_templateList(self):
        body={
            "currentPage": 1,
            "delFlag": 0,
            "orderBy": "",
            "pageSize": 10,
            "templateName": "",
            "templateType": "",
            "tenantId": ""
        }
        result = self.get_templateList(headers=self.headers,params=body)
        assert result["count"] > 0
        assert len(result["resultData"]) > 0
        assert result["success"] == True

    @allure.story("根据ID删除行业设备信息")
    def test_dele_device(self):
        result = self.dele_device(headers=self.headers,dsIndustryDeviceId=self.id_complete)
        assert result["resultData"] == "删除成功"
        #校验数据库
        sql = "select count(*) ,id from ds_industry_device where device_name = '%s'" % (
                    self.deviceInfo["deviceName"] + "complete")
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["count(*)"] == 0

    @allure.story("批量删除行业设备信息")
    def test_remove_devices(self):
        body={
            "dsIndustryDeviceIds": [self.id_standaloned]
        }
        result = self.remove_devices(headers=self.headers,params=body)
        assert result["resultData"] == "删除成功"
        # 校验数据库
        sql = "select count(*) ,id from ds_industry_device where id = '%s'" % (self.id_standaloned)
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["count(*)"] == 0