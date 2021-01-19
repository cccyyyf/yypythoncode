# coding=utf-8
# Time : 2020/12/10 17:02
# Author : huxin
from objects.interface.DevicePlat.DsIndustryAccountPO import DsIndustryAccountPO
from objects.interface.DevicePlat.DsIndustryDevicePO import DsIndustryDevicePO
from objects.interface.DevicePlat.LoginPO import LoginPO
from objects.interface.utils.PropertiesUtil import *
from RootPath import *
from objects.interface.utils.DateTimeUtil import *
import allure
import pytest

@allure.feature("设备台账信息对外接口")
class TestOutDsIndustryAccount(DsIndustryAccountPO):

    id_standaloned = ""
    bussinessId = str(get_time_stamp())
    id_account = ""
    record_id = ""
    def setup_class(self):
        self.headers = LoginPO().get_headers(role="wpg账号")
        public_path = RootPath.getDevicePlatPath() + "Public.yml"
        self.deviceInfo = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="行业设备信息")

        #新增一台行业设备
        body = {
            "dsIndustryDeviceDTO": {
                "labelId": "",
                "deviceName": self.deviceInfo["deviceName"]+"standaloned",
                "deviceId": self.deviceInfo["deviceId"]+"standaloned",
                "templateName": "测试专用行业模板01",
                "station": "设备测试",
                "deviceType": "industry_standaloned",
                "stationId": "c4097b56e58493988f133585d2bfa898",
                "templateId": "61d7443ade1c9315fac2c08b92c6272e",
                "qrCode": "/upload/front/images/20201208/1336125320995659778.png",
                "attribute": "[{\"__config__\":{\"formId\":102,\"document\":\"https://element.eleme.cn/#/zh-CN/component/input\",\"labelWidth\":null,\"label\":\"多行文本\",\"showLabel\":true,\"required\":true,\"renderKey\":\"1021606784700502\",\"layout\":\"colFormItem\",\"tagIcon\":\"textarea\",\"changeTag\":true,\"tag\":\"a-textarea\",\"regList\":[],\"span\":24},\"readonly\":false,\"maxlength\":null,\"__vModel__\":\"field102\",\"style\":{\"width\":\"100%\"},\"disabled\":false,\"placeholder\":\"请输入多行文本\",\"show-word-limit\":false,\"type\":\"textarea\",\"autosize\":{\"minRows\":4,\"maxRows\":4}}]",
                "attributeValue": "[{\"field102\":\"填写的属性信息\"}]"
            },
            "dsIndustryPointDTO": [{
                "childIndustryName": None,
                "dataType": "uint",
                "deviceId": "12345678906",
                "deviceName": "宏电DTU-测试01",
                "id": None,
                "industryId": None,
                "pointCode": "TL00",
                "pointId": "12345678906-07f9e4767dce0a7995c6c18c5cd872e3",
                "pointMemo": "水箱液位",
                "pointName": "TankLevel",
                "pointType": "15",
                "ratio": 1,
                "value": "12345678906-07f9e4767dce0a7995c6c18c5cd872e3"
            }]
        }
        result = DsIndustryDevicePO().add_DsIndustryDevice(headers=self.headers,body=body)
        sql = "select count(*) ,id from ds_industry_device where device_name = '%s'" %(self.deviceInfo["deviceName"] +"standaloned")
        sql_result = DsIndustryDevicePO().get_DB_data(sql=sql)
        #获取设备id
        TestOutDsIndustryAccount.id_standaloned = sql_result[0]["id"]

        #新增一条台账记录
        body2 = {
            "bussinessId": self.bussinessId,
            "type": "accMaintainRecord",
            "deviceId": self.deviceInfo["deviceId"]+"standaloned",
            "deviceName": self.deviceInfo["deviceName"]+"standaloned",
            "accountName": "autotest设备保养",
            "accountType": "accSecDeviceMaintain",
            "happenTime": "2020-12-06 12:00:00",
            "finishTime": "2020-12-07 12:00:00",
            "remark": "",
            "address": "",
            "workorderFlag": "0"
        }
        result2 = DsIndustryAccountPO().add_DsIndustryAccount(headers=self.headers,params=body2)
        #校验数据库
        sql2 = "select record_id,id from ds_industry_account where bussiness_id = '%s'" %(self.bussinessId)
        sql_result2 = DsIndustryAccountPO().get_DB_data(sql=sql2)
        TestOutDsIndustryAccount.id_account = sql_result2[0]["id"]
        TestOutDsIndustryAccount.record_id = sql_result2[0]["record_id"]

    def teardown_class(self):
        #删除台账信息
        result = DsIndustryAccountPO().dele_DsIndustryAccount(headers=self.headers, bussinessId=self.bussinessId)
        #删除行业设备
        result = DsIndustryDevicePO().dele_device(headers=self.headers, dsIndustryDeviceId=self.id_standaloned)


    @allure.story("查询台账详情")
    def test_get_detail(self):
        result = self.get_detail(headers=self.headers,entityId=self.id_account)
        assert result["success"] == True
        assert result["resultData"]["accountName"] == "autotest设备保养"

    @allure.story("根据行业设备编码查询台账详情")
    def test_get_DetailByIndustryDeviceId(self):
        body = {
            "industryDeviceId": self.deviceInfo["deviceId"]+"standaloned",
            "recordId": self.record_id
        }
        result = self.get_DetailByIndustryDeviceId(headers=self.headers,params=body)
        assert result["success"] == True
        assert result["resultData"]["accountName"] == "autotest设备保养"

    @allure.story("查询台账列表")
    def test_query_DsIndustryAccount(self):
        body = {
            "keyWord": self.deviceInfo["deviceName"]+"standaloned",
            "labelId": "",
            "stationIds": "c4097b56e58493988f133585d2bfa898",
            "happenStartTime": "",
            "happenEndTime": "",
            "currentPage": 1,
            "pageSize": 20
        }
        result = self.query_DsIndustryAccount(headers=self.headers,params=body)
        assert result["count"] > 0
        assert result["resultData"][0]["accountName"] == "autotest设备保养"



