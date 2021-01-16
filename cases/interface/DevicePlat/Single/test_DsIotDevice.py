# coding=utf-8
# Time : 2020/11/5 14:19
# Author : huxin
from objects.interface.DevicePlat.DsIotDevicePO import DsIotDevicePO
from objects.interface.DevicePlat.DsIotTemplatePO import DsIotTemplatePO
from objects.interface.DevicePlat.DsPointPO import DsPointPO
from objects.interface.DevicePlat.DsStationPO import DsStationPO
from objects.interface.DevicePlat.LoginPO import LoginPO
from objects.interface.utils.DateTimeUtil import *
import allure
import pytest
import random


@allure.feature("Iot设备信息")
class TestDsIotDevice(DsIotDevicePO):

    nowTime = get_time_stamp()
    deviceName = "自动化测试设备" + str(nowTime)

    #iot模板使用
    templateNum = "autoTest" + str(nowTime)
    templateId = ""

    def setup_class(self):
        self.headers = LoginPO().get_headers(role="wpg账号")
        # 新增监测量
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

        #新建iot设备模板供使用
        body = {
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
        result = DsIotTemplatePO().add_iotTemplate(headers=self.headers, body=body)
        sql = "select id from ds_iot_template where template_num = '%s'" % (self.templateNum)
        sql_result = DsIotTemplatePO().get_DB_data(sql=sql)
        TestDsIotDevice.templateId = sql_result[0]["id"]

        #添加区域
        self.temp = str(random.randint(1,10000))
        self.areaName = "AutoAreaName" + self.temp
        self.stationName = "站点名称接口自动化测试" + self.temp
        self.stationCode = "AutoCode" + str(random.randint(1,99))
        self.shorthand = "AutoPin" + str(random.randint(1,99))
        body_area = {
            "id": "",
            "areaName": self.areaName,
            "parentId": "0"
        }
        response_area = DsStationPO().add_area(headers=self.headers, body=body_area)
        area_id_sql = "SELECT id FROM ds_area where area_name = '%s'"%(self.areaName)
        id_result = DsStationPO().get_DB_data(sql=area_id_sql)
        self.area_id = id_result[0]["id"]
        #添加站点
        body_staion = {
            "id": "",
            "stationName": self.stationName,
            "stationCode": self.stationCode,
            "areaId": self.area_id,
            "shorthand": self.shorthand,
            "stationType": "PressurePoint",
            "lati": "1",
            "longi": "2",
            "addr": "接口自动化测试地址",
            "labelId": "",
            "remark": ""
        }
        result_staion = DsStationPO().add_station(headers=self.headers,body=body_staion)

        sql_id = "SELECT id FROM ds_station where station_name = '%s'"%(self.stationName)
        id_result = DsStationPO().get_DB_data(sql=sql_id)
        self.station_id = id_result[0]["id"]

    def teardown_class(self):
        #删除iot模板
        sql= "delete from ds_iot_template where template_num = '%s'" % (self.templateNum)
        sql_result = DsIotTemplatePO().get_DB_data(sql=sql)

        #删除监测量数据
        response = DsPointPO().delete_point(point_id=self.point_id, headers=self.headers)
        #删除站点
        result = DsStationPO().dele_station(headers=self.headers,ids=self.station_id)
        #删除区域
        result = DsStationPO().dele_area(headers=self.headers,entityId=self.area_id)

    @allure.story("新增IOT设备-无子设备")
    def test_add_iotDevice(self):
        body={
            "iotDeviceBaseDTO": {
                "id": "",
                "attribute": "[{\"clearable\":true,\"__config__\":{\"formId\":105,\"defaultValue\":null,\"document\":\"https://element.eleme.cn/#/zh-CN/component/date-picker\",\"labelWidth\":null,\"label\":\"日期选择\",\"showLabel\":true,\"required\":true,\"renderKey\":\"1051604454071789\",\"layout\":\"colFormItem\",\"tagIcon\":\"date\",\"changeTag\":true,\"tag\":\"el-date-picker\",\"regList\":[],\"span\":24},\"readonly\":false,\"format\":\"yyyy-MM-dd\",\"value-format\":\"yyyy-MM-dd\",\"__vModel__\":\"field105\",\"style\":{\"width\":\"100%\"},\"disabled\":false,\"placeholder\":\"请选择日期选择\",\"type\":\"date\"}]",
                "attributeValue": "{\"field105\":\"2020-11-05\"}",
                "templateId": self.templateId,
                "deviceName": self.deviceName,
                "deviceId": str(self.nowTime),
                "stationId": self.station_id,
                "iotId": "",
                "collectorId": str(self.nowTime),
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
                "dataType": "uint",
                "dataTypeName": "uint",
                "id": self.point_id,
                "maxValue": None,
                "minValue": None,
                "pointCode": self.pointCode,
                "pointId": self.point_id,
                "pointMemo": self.pointMemo,
                "pointName": self.pointName,
                "pointType": "13",
                "pointTypeName": "泵房状态",
                "pointUnit": None,
                "pointUnitName": "",
                "ratio": 1,
                "templateId": self.templateId
            }
            ]
        }
        result = self.add_iotDevice(headers=self.headers,body=body)
        assert result["success"] == True
        assert "成功" in result["resultData"]

        #校验数据库
        sql = "select count(*) from ds_iot_device where device_name = '%s'" %(self.deviceName)
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["count(*)"] == 1

    @allure.story("新增IOT设备-有子设备")
    def test_add_iotDevice_sub(self):
        body = {
            "iotDeviceBaseDTO": {
                "id": "",
                "attribute": "[{\"clearable\":true,\"__config__\":{\"formId\":105,\"defaultValue\":null,\"document\":\"https://element.eleme.cn/#/zh-CN/component/date-picker\",\"labelWidth\":null,\"label\":\"日期选择\",\"showLabel\":true,\"required\":true,\"renderKey\":\"1051604454071789\",\"layout\":\"colFormItem\",\"tagIcon\":\"date\",\"changeTag\":true,\"tag\":\"el-date-picker\",\"regList\":[],\"span\":24},\"readonly\":false,\"format\":\"yyyy-MM-dd\",\"value-format\":\"yyyy-MM-dd\",\"__vModel__\":\"field105\",\"style\":{\"width\":\"100%\"},\"disabled\":false,\"placeholder\":\"请选择日期选择\",\"type\":\"date\"}]",
                "attributeValue": "{\"field105\":\"2020-11-05\"}",
                "templateId": self.templateId,
                "deviceName": self.deviceName + "子",
                "deviceId": str(self.nowTime + 1 ),
                "stationId": self.station_id,
                "iotId": "",
                "collectorId": str(self.nowTime + 1),
                "factoryName": "测试厂家名称",
                "deviceModel": "dt-123e",
                "productTime": "2020-11-05",
                "connectType": "5G",
                "protocolType": "UDP/TCP",
                "moreFlag": 1
            },
            "iotSubDeviceDTOList": [
                {
                "subdeviceId": str(self.nowTime + 1 ) + "01",
                "deviceName": "子设备名称1" + str(self.nowTime),
                "deviceIds": [],
                "isIndustry": False,
                "iotSubDevicePointList": [
                {
                    "controlStatus": False,
                    "dataSort": None,
                    "dataType": "uint",
                    "dataTypeName": "uint",
                    "id": self.point_id,
                    "maxValue": None,
                    "minValue": None,
                    "pointCode": self.pointCode,
                    "pointId": self.point_id,
                    "pointMemo": self.pointMemo,
                    "pointName": self.pointName,
                    "pointType": "13",
                    "pointTypeName": "泵房状态",
                    "pointUnit": None,
                    "pointUnitName": "",
                    "ratio": 1,
                    "templateId": self.templateId,
                    "value": self.point_id
                }]
                },
                {
                "subdeviceId": str(self.nowTime + 1 ) + "02",
                "deviceName": "子设备名称2"+ str(self.nowTime),
                "deviceIds": [],
                "isIndustry": False,
                "iotSubDevicePointList": [{
                    "controlStatus": False,
                    "dataSort": None,
                    "dataType": "uint",
                    "dataTypeName": "uint",
                    "id": self.point_id,
                    "maxValue": None,
                    "minValue": None,
                    "pointCode": self.pointCode,
                    "pointId": self.point_id,
                    "pointMemo": self.pointMemo,
                    "pointName": self.pointName,
                    "pointType": "13",
                    "pointTypeName": "泵房状态",
                    "pointUnit": None,
                    "pointUnitName": "",
                    "ratio": 1,
                    "templateId": self.templateId,
                    "value": self.point_id
                }]
                }
            ],
            "iotDevicePointDTOList": []
        }
        result = self.add_iotDevice(headers=self.headers, body=body)
        assert result["success"] == True
        assert "成功" in result["resultData"]

        #校验数据库
        sql = "select count(*) from ds_iot_device where device_name = '%s'" %(self.deviceName + "子")
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["count(*)"] == 1

    @allure.story("修改iot设备")
    def test_modify_iotDevice(self):
        #获取设备id
        sql_id = "select id from ds_iot_device where device_name = '%s'" %(self.deviceName)
        sql_result_id = self.get_DB_data(sql=sql_id)

        body={
            "iotDeviceBaseDTO": {
                "id": sql_result_id[0]["id"],
                "attribute": "[{\"clearable\":true,\"__config__\":{\"formId\":105,\"defaultValue\":null,\"document\":\"https://element.eleme.cn/#/zh-CN/component/date-picker\",\"labelWidth\":null,\"label\":\"日期选择\",\"showLabel\":true,\"required\":true,\"renderKey\":\"1051604454071789\",\"layout\":\"colFormItem\",\"tagIcon\":\"date\",\"changeTag\":true,\"tag\":\"el-date-picker\",\"regList\":[],\"span\":24},\"readonly\":false,\"format\":\"yyyy-MM-dd\",\"value-format\":\"yyyy-MM-dd\",\"__vModel__\":\"field105\",\"style\":{\"width\":\"100%\"},\"disabled\":false,\"placeholder\":\"请选择日期选择\",\"type\":\"date\"}]",
                "attributeValue": "{\"field105\":\"2020-11-05\"}",
                "templateId": self.templateId,
                "deviceName": self.deviceName,
                "deviceId": str(self.nowTime),
                "stationId": self.station_id,
                "iotId": "",
                "collectorId": str(self.nowTime),
                "factoryName": "测试厂家名称",
                "deviceModel": "dt-123e",
                "productTime": "2020-11-05",
                "connectType": "4G",
                "protocolType": "UDP/TCP",
                "moreFlag": 0
            },
            "iotSubDeviceDTOList": [],
            "iotDevicePointDTOList": [
                {
                    "controlStatus": False,
                    "dataSort": None,
                    "dataType": "uint",
                    "dataTypeName": "uint",
                    "id": self.point_id,
                    "maxValue": None,
                    "minValue": None,
                    "pointCode": self.pointCode,
                    "pointId": self.point_id,
                    "pointMemo": self.pointMemo,
                    "pointName": self.pointName,
                    "pointType": "13",
                    "pointTypeName": "泵房状态",
                    "pointUnit": None,
                    "pointUnitName": "",
                    "ratio": 1,
                    "templateId": self.templateId,
                    "value": self.point_id
            }
            ]
        }
        result = self.modify_iotDevice(headers=self.headers,body=body)
        assert result["resultData"] == "修改成功"

        #校验数据库
        sql = "select connect_type from ds_iot_device where device_name = '%s'" %(self.deviceName)
        sql_result = self.get_DB_data(sql=sql)
        assert sql_result[0]["connect_type"] == "4G"

    @allure.story("验证设备ID的唯一性校验")
    def test_check_only(self):
        body={
            "iotDeviceBaseDTO": {
                "id": "",
                "attribute": "[{\"clearable\":true,\"__config__\":{\"formId\":105,\"defaultValue\":null,\"document\":\"https://element.eleme.cn/#/zh-CN/component/date-picker\",\"labelWidth\":null,\"label\":\"日期选择\",\"showLabel\":true,\"required\":true,\"renderKey\":\"1051604454071789\",\"layout\":\"colFormItem\",\"tagIcon\":\"date\",\"changeTag\":true,\"tag\":\"el-date-picker\",\"regList\":[],\"span\":24},\"readonly\":false,\"format\":\"yyyy-MM-dd\",\"value-format\":\"yyyy-MM-dd\",\"__vModel__\":\"field105\",\"style\":{\"width\":\"100%\"},\"disabled\":false,\"placeholder\":\"请选择日期选择\",\"type\":\"date\"}]",
                "attributeValue": "{\"field105\":\"2020-11-05\"}",
                "templateId": self.templateId,
                "deviceName": self.deviceName,
                "deviceId": str(self.nowTime),
                "stationId": self.station_id,
                "iotId": "",
                "collectorId": str(self.nowTime),
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
                    "dataType": "uint",
                    "dataTypeName": "uint",
                    "id": self.point_id,
                    "maxValue": None,
                    "minValue": None,
                    "pointCode": self.pointCode,
                    "pointId": self.point_id,
                    "pointMemo": self.pointMemo,
                    "pointName": self.pointName,
                    "pointType": "13",
                    "pointTypeName": "泵房状态",
                    "pointUnit": None,
                    "pointUnitName": "",
                    "ratio": 1,
                    "templateId": self.templateId,
                    "value": self.point_id
            }
            ]
        }
        result = self.check_only(headers=self.headers,body=body)
        assert result["success"] == False
        assert "设备ID已经存在" in result["errorMessage"]

    @allure.story("查看设备详情")
    def test_get_detail(self):
        #获取id
        sql = "select id from ds_iot_device where device_name = '%s'" %(self.deviceName)
        sql_result = self.get_DB_data(sql=sql)
        id = sql_result[0]["id"]
        result = self.get_detail(headers=self.headers,id=id)
        assert result["success"] == True
        assert result["resultData"]["dsIotDeviceVO"]["factoryName"] == "测试厂家名称"


    @allure.story("获取Iot设备连接方式字典列表")
    def test_get_connectionType(self):
        body = {}
        result = self.get_connectionType(headers=self.headers,body=body)
        assert result["success"] == True
        assert len(result["resultData"]) > 2

    @allure.story("分页查询IOT设备信息")
    def test_get_listPage(self):
        body = {"keyWord":"","currentPage":1,"pageSize":20,"orderBy":"","stationId":self.station_id}
        result = self.get_listPage(headers=self.headers,body=body)
        assert result["success"] == True
        assert result["count"] > 0
        assert result["resultData"][0]["stationId"] == self.station_id

    @allure.story("选择iot设备模板")
    def test_get_templateDetails(self):
        body={}
        result = self.get_templateDetails(headers=self.headers,body=body,id=self.templateId)
        assert result["success"] == True
        assert result["resultData"]["templateNum"] ==self.templateNum

    @allure.story("删除iot设备")
    def test_dele_iotDevices(self):
        sql = "select id from ds_iot_device where device_name = '%s'" % (self.deviceName)
        sql_result = self.get_DB_data(sql=sql)
        id = sql_result[0]["id"]

        result = self.dele_iotDevices(headers=self.headers,ids=id)
        assert result["resultData"] == "删除成功"
        #校验数据
        sql_check = "select count(*) from ds_iot_device where device_name = '%s'" % (self.deviceName)
        sql_check_result = self.get_DB_data(sql=sql_check)
        assert sql_check_result[0]["count(*)"] == 0

        #删除iot设备2
        sql2 = "select id from ds_iot_device where device_name = '%s'" % (self.deviceName + "子")
        sql_result2 = self.get_DB_data(sql=sql2)
        id2 = sql_result2[0]["id"]
        result = self.dele_iotDevices(headers=self.headers, ids=id2)
