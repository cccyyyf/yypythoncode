# -*- coding: utf-8 -*-
# @Author  : Felix.Ma
# @Time    : 2021/1/5 16:29

import allure
from objects.interface.ErGong.ElectronicInspectPO import ElectronicInspectPO
from cases.interface.ErGong.public import headers
from objects.interface.utils import DateTimeUtil


@allure.feature("电子巡检")
class TestElectronicInspect(ElectronicInspectPO):

    def setup_class(self):
        self.headers = headers

    def teardown_class(self):
        pass

    @allure.story("查询当天的所有巡检任务")
    def test_query_electronic_inspect(self):
        response = self.query_all_electronic_inspect(headers=self.headers)
        assert response["status"] == "complete"
        allTaskCount = response['resultData']['allTaskCount']
        today = DateTimeUtil.get_current_date()
        sql = f"select count(*) from electronic_inspect where create_time>= '{str(today)}' and create_user='1'"
        sql_result = self.get_db_dict(dict_sql=sql)
        assert sql_result[0]["count(*)"] == allTaskCount
