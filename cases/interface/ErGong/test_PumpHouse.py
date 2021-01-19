# -*- coding: utf-8 -*-
# @Author  : Felix.Ma
# @Time    : 2021/1/6 9:16

import allure
from objects.interface.ErGong.PumpHousePO import PumpHousePO
from cases.interface.ErGong.public import headers, root_pump_house_sql


@allure.feature("泵房管理")
class TestPumpHousePO(PumpHousePO):

    def setup_class(self):
        self.headers = headers

    def teardown_class(self):
        pass

    @allure.story("首页泵房运行信息返回动态配置信息数据")
    def test_pump_run_info(self):
        response = self.pump_run_info(headers=self.headers, params={"pageNum":1,"pageSize":40,"pumpList":[]})
        assert response["status"] == "complete"
        count = response["resultData"]["total"]
        sql_result = self.get_db_dict(dict_sql=root_pump_house_sql())
        assert sql_result[0]["count(*)"] == count
