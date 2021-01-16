# coding=utf-8
# Time : 2020/9/11 16:08
# Author : huxin
import os
import allure
from objects.interface.ZHDD.Alarm.AlarmPO import AlarmPO
from objects.interface.utils.Decorators import *
from objects.interface.utils.DateTimeUtil import *


@allure.feature("报警类别占比")
class TestAlarmProportion(AlarmPO):

    def setup_class(self):
        pass

    def teardown_class(self):
        pass

    @allure.story("获取报警类别占比信息_不输入查询条件")
    @dbcheck("校验不输入入参接口返回值")
    def test_getAlarmProportion(self):
        body = {}
        result = self.getAlarmData(loginName="root", password="Abc12345", body=body)
        # 断言返回值
        assert result["status"] == "complete"
        assert len(result["resultData"]["series"]) > 0
        # 断言数据库
        sql = "select max_data from stats_alarm where site_code='%s' and point_name='%s' order by start_time desc " \
              "limit 1" % (20200904, "PipePressure")
        db_result = self.get_DB_data(sql=sql)
        assert db_result[0]["max_data"] == 0.35

    @allure.story("获取报警类别占比信息_查询条件输入特定日期")
    @dbcheck("校验输入特定日期区间接口返回值")
    def test_getAlarmProportion2(self):
        body = {"startTime":get_last_date(3), "endTime":get_current_date()}
        result = self.getAlarmData(loginName="root", password="Abc12345", body=body)
        # 断言返回值
        assert result["status"] == "complete"
        assert len(result["resultData"]["series"]) > 0
        # 断言数据库
        sql = "select max_data from stats_alarm where site_code='%s' and point_name='%s' order by start_time desc " \
              "limit 1" % (20200904, "PipePressure")
        db_result = self.get_DB_data(sql=sql)
        assert db_result[0]["max_data"] == 0.35