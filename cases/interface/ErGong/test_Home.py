# -*- coding: utf-8 -*-
# @Author  : Felix.Ma
# @Time    : 2021/1/5 15:35

import allure
from objects.interface.ErGong.HomePO import HomePO
from cases.interface.ErGong.public import headers, root_pump_house_sql


@allure.feature("主页管理")
class TestHomePO(HomePO):

    def setup_class(self):
        self.headers = headers

    def teardown_class(self):
        pass

    @allure.story("泵房设备二级树")
    def test_home_tree(self):
        response = self.home_tree(headers=self.headers, params={})
        assert response["status"] == "complete"
        count = len(response["resultData"])
        sql_result = self.get_DB_data(sql=root_pump_house_sql())
        assert sql_result[0]["count(*)"] == count

    @allure.story("地图所有泵房")
    def test_all_pump_house(self):
        response = self.all_pump_house(headers=self.headers,
                                       params={"fuzzyQuery":"","pumpHouseType":["8","1","2","3","4","5","6","7","9"]})
        assert response["status"] == "complete"
        count = len(response["resultData"])
        sql_result = self.get_DB_data(sql=root_pump_house_sql("and ph.pump_house_type in ('1','2','3','4','5','6','7','8','9')"))
        assert sql_result[0]["count(*)"] == count

