# -*- coding: utf-8 -*-
# @Author  : Felix.Ma
# @Time    : 2021/1/7 10:41

import allure
from objects.interface.ErGong.RealDataPO import RealDataPO
from cases.interface.ErGong.public import headers, query_device_service, get_pv_from_sv
from objects.interface.utils.DateTimeUtil import get_current_date, get_now, get_time_difference


@allure.feature("实时数据")
class TestRealData(RealDataPO):

    def setup_class(self):
        self.headers = headers
        self.deviceId = "20030277"
        self.point_name = "InletPressure"

    def teardown_class(self):
        pass

    @allure.story("实时数据列表")
    def test_get_list(self):
        response = self.get_list(headers=self.headers, params={"devId": self.deviceId})
        assert response["status"] == "complete"
        count = len(response["resultData"])
        sql_result = self.get_db_dict(dict_sql=query_device_service(self.deviceId))
        assert sql_result[0]["count(*)"] == count
        # 校验进口压力
        result = response["resultData"][0]
        assert result["code"] == self.point_name
        assert result["date"] == str(get_current_date())
        today = result["date"]
        current = result["dateTime"]
        # 与当前时间误差不超过2分钟
        assert get_time_difference(str(get_now()), today+' '+current) <= 120
        # 获取倍率
        sql_result_ratio = self.get_db_dict(dict_sql=query_device_service(self.deviceId, query="ratio",
                                                                          params=f"and pt.point_name='{self.point_name}'"))
        ratio = sql_result_ratio[0]['ratio']
        # self.get_redis("mis:/device/20030277/realtime", "/data")
        # 秒表里的pv
        sql_result_pv = self.get_db_dict(dict_sql=get_pv_from_sv(str(get_current_date()).replace('-', ''),
                                                                 self.deviceId, self.point_name))
        final_pv = round(float(ratio)*(sql_result_pv[0]['pv']), 2)
        assert final_pv == round(float(final_pv), 2)






