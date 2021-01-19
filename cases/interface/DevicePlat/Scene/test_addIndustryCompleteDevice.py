# coding=utf-8
# Time : 2020/12/12 13:28
# Author : huxin
import allure
from objects.interface.DevicePlat.LoginPO import LoginPO
from objects.interface.DevicePlat.DsStationPO import DsStationPO
from objects.interface.DevicePlat.DsPointPO import DsPointPO
from objects.interface.DevicePlat.DsIndustryTemplatePO import DsIndustryTemplatePO
from objects.interface.DevicePlat.DsIndustryDevicePO import DsIndustryDevicePO
from objects.interface.DevicePlat.DsIotTemplatePO import DsIotTemplatePO
from objects.interface.DevicePlat.DsIotDevicePO import DsIotDevicePO
from objects.interface.utils.PropertiesUtil import *
from objects.interface.utils.DateTimeUtil import *
from RootPath import *
import random
import pytest


@allure.feature("场景：添加成套行业设备(1.添加监测量->2.添加区域/站点->3.添加行业设备模板->4.添加iot设备->5.添加独立行业设备->6.添加成套行业设备->7.删除行业设备、删除行业设备模板、站点、监测量等")
class TestaddIndustryCompleteDevice(DsStationPO,DsPointPO,DsIndustryTemplatePO,DsIndustryDevicePO,DsIotDevicePO,DsIotTemplatePO):

    def setup_class(self):
        self.headers = LoginPO().get_headers(role="wpg账号")
        public_path = RootPath.getDevicePlatPath() + "Public.yml"
        self.staion = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="站点管理")
        self.deviceInfo = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="行业设备信息")

        self.pointCode = "auto" + str(random.randint(1, 10000))
        self.pointName = "auto" + str(random.randint(1, 10000))
        self.pointMemo = "自动化测试_监测量名称" + str(random.randint(1, 10000))
        self.nowTime = get_time_stamp()
        self.deviceName = "自动化测试设备" + str(self.nowTime)

    def teardwon_class(self):
        pass

    @allure.story("1.添加监测量->2.添加区域/站点->3.添加行业设备模板->4.添加iot设备->5.添加独立行业设备->6.添加成套行业设备->7.删除行业设备、删除行业设备模板、站点、监测量等")
    def test_addIndustryCompleteDevice(self):
        #添加监测量
        body_point = {
            "pointCode": self.pointCode,
            "pointName": self.pointName,
            "pointMemo": self.pointMemo,
            "pointType": "1",
            "dataType": "word",
            "gatewayFlag": True
        }
        response_point = self.add_point(headers=self.headers, body=body_point)
        assert response_point["resultData"] == "新增成功"
        sql = "select id from ds_point where point_code = '%s'" % self.pointCode
        db_res = self.get_DB_data(sql=sql)
        point_id = db_res[0]["id"]

        #添加区域
        body_area = {
            "id": "",
            "areaName": self.staion["areaName"],
            "parentId": "0"
        }
        response_area = self.add_area(headers=self.headers, body=body_area)
        assert response_area["success"]==True
        area_id_sql = "SELECT id FROM ds_area where area_name = '%s'"%(self.staion["areaName"])
        id_result = self.get_DB_data(sql=area_id_sql)
        area_id = id_result[0]["id"]
        #添加站点
        body_staion = {
            "id": "",
            "stationName": self.staion["stationName"],
            "stationCode": "station01",
            "areaId": area_id,
            "shorthand": "pinyinjianxie01",
            "stationType": "PressurePoint",
            "lati": "1",
            "longi": "2",
            "addr": "接口自动化测试地址",
            "labelId": "",
            "remark": ""
        }
        result_staion = self.add_station(headers=self.headers,body=body_staion)
        assert result_staion["success"] == True
        sql_id = "SELECT id FROM ds_station where station_name = '%s'"%(self.staion["stationName"])
        id_result = self.get_DB_data(sql=sql_id)
        station_id = id_result[0]["id"]

        #添加行业设备模板
        templateName = "autoTest" + str(self.nowTime + 1)
        body={"templateName":templateName,"templateType":"Water_Plant","labelId":"","attribute":"[]"}
        result = self.add_IndustryTemplate(headers=self.headers,body=body)
        assert result["resultData"] == "添加成功"
        id_sql = "select id from ds_industry_template where template_name = '%s'" % (templateName)
        id_result = self.get_DB_data(sql=id_sql)
        template_id = id_result[0]["id"]

        #添加iot模板(gateway)
        templateNum = "autoTest" + str(self.nowTime + 1)
        body_template={
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
            "templateNum": templateNum,
            "templateName": "接口自动化测试名称" + str(self.nowTime),
            "templateType": "gateway",
            "collectorType": "HWGATEWAY",
            "topic": "test/test/test",
            "remark": "测试备注",
            "templatePointList": [
                {
                    "id": point_id,
                    "pointId": point_id,
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
        result_template = self.add_iotTemplate(headers=self.headers,body=body_template)
        assert result_template["resultData"] == "新增成功"
        sql = "select id from ds_iot_template where template_num = '%s'" % (templateNum)
        sql_result = DsIotTemplatePO().get_DB_data(sql=sql)
        templateId = sql_result[0]["id"]

        #添加iot设备
        deviceId_iot = str(self.nowTime)
        body_device={
            "iotDeviceBaseDTO": {
                "id": "",
                "attribute": "[{\"clearable\":true,\"__config__\":{\"formId\":105,\"defaultValue\":null,\"document\":\"https://element.eleme.cn/#/zh-CN/component/date-picker\",\"labelWidth\":null,\"label\":\"日期选择\",\"showLabel\":true,\"required\":true,\"renderKey\":\"1051604454071789\",\"layout\":\"colFormItem\",\"tagIcon\":\"date\",\"changeTag\":true,\"tag\":\"el-date-picker\",\"regList\":[],\"span\":24},\"readonly\":false,\"format\":\"yyyy-MM-dd\",\"value-format\":\"yyyy-MM-dd\",\"__vModel__\":\"field105\",\"style\":{\"width\":\"100%\"},\"disabled\":false,\"placeholder\":\"请选择日期选择\",\"type\":\"date\"}]",
                "attributeValue": "{\"field105\":\"2020-11-05\"}",
                "templateId": templateId,
                "deviceName": self.deviceName,
                "deviceId": deviceId_iot,
                "stationId": station_id,
                "iotId": "",
                "collectorId": deviceId_iot,
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
                "id": point_id,
                "maxValue": None,
                "minValue": None,
                "pointCode": self.pointCode,
                "pointId": point_id,
                "pointMemo": self.pointMemo,
                "pointName": self.pointName,
                "pointType": "1",
                "pointTypeName": "监测压力",
                "pointUnit": None,
                "pointUnitName": "",
                "ratio": 1,
                "templateId": templateId
            }]
        }
        result_device = self.add_iotDevice(headers=self.headers,body=body_device)
        assert "成功" in result_device["resultData"]
        #校验数据库
        sql = "select count(*) from ds_iot_device where device_name = '%s'" %(self.deviceName)
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["count(*)"] == 1

        #添加行业设备（独立）
        body = {
            "dsIndustryDeviceDTO": {
                "labelId": "",
                "deviceName": self.deviceInfo["deviceName"]+"standaloned",
                "deviceId": self.deviceInfo["deviceId"]+"standaloned",
                "templateName": templateName,
                "station": self.staion["stationName"],
                "deviceType": "industry_standaloned",
                "stationId": station_id,
                "templateId": template_id,
                "qrCode": "/upload/front/images/20201208/1336125320995659778.png",
                "attribute": "[{\"__config__\":{\"formId\":102,\"document\":\"https://element.eleme.cn/#/zh-CN/component/input\",\"labelWidth\":null,\"label\":\"多行文本\",\"showLabel\":true,\"required\":true,\"renderKey\":\"1021606784700502\",\"layout\":\"colFormItem\",\"tagIcon\":\"textarea\",\"changeTag\":true,\"tag\":\"a-textarea\",\"regList\":[],\"span\":24},\"readonly\":false,\"maxlength\":null,\"__vModel__\":\"field102\",\"style\":{\"width\":\"100%\"},\"disabled\":false,\"placeholder\":\"请输入多行文本\",\"show-word-limit\":false,\"type\":\"textarea\",\"autosize\":{\"minRows\":4,\"maxRows\":4}}]",
                "attributeValue": "[{\"field102\":\"填写的属性信息\"}]"
            },
            "dsIndustryPointDTO": [{
                "childIndustryName": None,
                "dataType": "word",
                "deviceId": deviceId_iot,
                "deviceName": self.deviceName,
                "id": None,
                "industryId": None,
                "pointCode": self.pointCode,
                "pointId": deviceId_iot +"-"+point_id,
                "pointMemo": self.pointMemo,
                "pointName": self.pointName,
                "pointType": "1",
                "ratio": 1,
                "value": point_id
            }]
        }
        result = self.add_DsIndustryDevice(headers=self.headers,body=body)
        assert result["resultData"] == "添加成功"
        #校验数据库
        sql = "select count(*) ,id from ds_industry_device where device_name = '%s'" %(self.deviceInfo["deviceName"] +"standaloned")
        sql_result = self.get_DB_data(sql=sql)
        #获取设备id
        id_standaloned = sql_result[0]["id"]

        #添加行业设备成套
        body = {
            "dsIndustryDeviceDTO": {
                "labelId": "",
                "deviceName": self.deviceInfo["deviceName"]+ "complete",
                "deviceId": self.deviceInfo["deviceId"]+"complete",
                "templateName": templateName,
                "station": self.staion["stationName"],
                "deviceType": "complete_equipment",
                "stationId": station_id,
                "templateId": template_id,
                "qrCode": "/upload/front/images/20201208/1336133209206415362.png",
                "attribute": "[{\"__config__\":{\"formId\":102,\"document\":\"https://element.eleme.cn/#/zh-CN/component/input\",\"labelWidth\":null,\"label\":\"多行文本\",\"showLabel\":true,\"required\":true,\"renderKey\":\"1021606784700502\",\"layout\":\"colFormItem\",\"tagIcon\":\"textarea\",\"changeTag\":true,\"tag\":\"a-textarea\",\"regList\":[],\"span\":24},\"readonly\":false,\"maxlength\":null,\"__vModel__\":\"field102\",\"style\":{\"width\":\"100%\"},\"disabled\":false,\"placeholder\":\"请输入多行文本\",\"show-word-limit\":false,\"type\":\"textarea\",\"autosize\":{\"minRows\":4,\"maxRows\":4}}]",
                "attributeValue": "[{\"field102\":\"测试属性文本\"}]"
            },
            "dsIndustryPointDTO": [{
                "childIndustryName": self.deviceInfo["deviceName"]+ "standaloned",
                "dataType": "word",
                "deviceId": deviceId_iot,
                "deviceName":self.deviceName+ "('%s')"%(self.deviceInfo["deviceName"]+ "standaloned"),
                "id": id_standaloned + "-"+deviceId_iot+"-"+point_id,
                "industryId": id_standaloned ,
                "pointCode": self.pointCode,
                "pointId": deviceId_iot+"-"+point_id,
                "pointMemo": self.pointMemo,
                "pointName": self.pointName,
                "pointType": "1",
                "ratio": 1,
                "value": id_standaloned + "-"+deviceId_iot+"-"+point_id
            }],
            "dsIndustryChildRelDTO": [{
                "childId": id_standaloned ,
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
        id_complete = sql_result[0]["id"]

        #删除行业设备-成套设备
        result = self.dele_device(headers=self.headers, dsIndustryDeviceId=id_complete)
        #删除行业设备-独立设备
        result = self.dele_device(headers=self.headers, dsIndustryDeviceId=id_standaloned)
        #删除行业设备模板
        result = self.dele_DsIndustryTemplate(headers=self.headers, templateId=template_id)
        #删除iot设备
        sql = "select id from ds_iot_device where device_name = '%s'" % (self.deviceName)
        sql_result = self.get_DB_data(sql=sql)
        id = sql_result[0]["id"]
        result = self.dele_iotDevices(headers=self.headers,ids=id)
        #删除iot模板
        id_sql = "select id from ds_iot_template where template_num = '%s'" % (templateNum)
        id_result = self.get_DB_data(sql=id_sql)
        id = id_result[0]["id"]
        result = self.dele_DsIotTemplate(headers=self.headers,id=id)
        #删除站点
        result = self.dele_station(headers=self.headers,ids=station_id)
        #删除区域
        result = self.dele_area(headers=self.headers,entityId=area_id)
        #删除监测量
        sql = "select id from ds_point where point_code = '%s'"% self.pointCode
        db_res = self.get_DB_data(sql=sql)
        response = self.delete_point(point_id=db_res[0]["id"],headers=self.headers)
        assert response["resultData"] == "删除成功"

