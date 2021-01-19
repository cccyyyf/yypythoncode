# -*- coding: utf-8 -*-
# @Author  : Felix.Ma
# @Time    : 2021/1/5 17:18

import allure
from objects.interface.ErGong.AlarmPO import AlarmPO
from cases.interface.ErGong.public import headers


@allure.feature("报警管理")
class TestAlarm(AlarmPO):

    def setup_class(self):
        self.headers = headers

    def teardown_class(self):
        pass

    @allure.story("查询当前报警数")
    def test_index_alarm_count(self):
        response = self.get_index_alarm_count(headers=self.headers)
        assert response["status"] == "complete"
        count = response['resultData']
        sql = """
        SELECT count(*)
        FROM (SELECT concat(alarm.device_code, '+', alarm.function_name, '+',
                    date_format(alarm.start_date, '%Y-%m-%d %H:%i:%s')) as id
        from waterdb_ds.alarm_statistics alarm
               JOIN alarm_task_description atd ON atd.function_name = alarm.function_name
               JOIN device dev ON dev.id = alarm.device_code
               JOIN device_pump_house ph ON ph.id = dev.id_pump_house
        WHERE alarm_status = '1'
        GROUP BY id) t
        """
        sql_result = self.get_db_dict(dict_sql=sql)
        assert sql_result[0]["count(*)"] == count
