# -*- coding: utf-8 -*-
import pytest
from objects.webpage.utils.PropertiesUtil import ConfigUtil
from RootPath import RootPath
import os

conf = ConfigUtil(RootPath.getWebIniPath())
case_path = os.path.dirname(RootPath.getWebIniPath()).replace("resources", "cases")
report_path = os.path.dirname(RootPath.getWebIniPath()).replace("resources", "reports")

if __name__ == '__main__':
    # 重试次数
    rerunTimes = conf.get("SZ_INFO", "RERUN")
    # 多线程数
    threadTimes = conf.get("SZ_INFO", "THREAD")

    # 执行pytest单元测试，生成 Allure 报告需要的数据存在 /reports 目录
    pytest.main(['--alluredir', './temp',"--reruns=%s" % rerunTimes])
    # 执行命令 allure generate ./temp -o ./report --clean ，生成测试报告
    allure_cmd = 'allure generate ./temp -o ' + report_path + ' --clean'
    os.system(allure_cmd)

