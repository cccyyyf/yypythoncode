# coding=utf-8
import pytest
from objects.interface.utils.PropertiesUtil import ConfigUtil
from RootPath import RootPath
import os
import platform
import sys

conf = ConfigUtil(RootPath.getInterfaceIniPath()+'/ZHDD.ini')
case_path = os.path.dirname(RootPath.getInterfaceIniPath()).replace("resources", "cases")
report_path = os.path.dirname(RootPath.getInterfaceIniPath()).replace("resources", "reports")

run_cases = sys.argv

if __name__ == '__main__':
    # 重试次数
    rerunTimes = conf.get("ZHDD_INFO", "RERUN")
    # 多线程数
    threadTimes = conf.get("ZHDD_INFO", "THREAD")

    # 执行pytest单元测试，生成 Allure 报告需要的数据存在 /reports 目录
    if len(run_cases) == 1:
        pytest_cmd = ['--alluredir', './allure-results', '--reruns=%s' % rerunTimes]
    else:
        run_cases = sys.argv[1]
        pytest_cmd = [run_cases, '--alluredir', './allure-results', '-reruns=%s' % rerunTimes]

    pytest.main(pytest_cmd)

    if platform.system() == "Windows":
        '''
        适配Jenkins，Jenkins在Linux服务器，可以用jenkins来生成报告
        执行命令 allure generate ./allure-results -o ./report --clean ，生成测试报告
        '''
        allure_cmd = 'allure generate ./allure-results -o ' + report_path + ' --clean'
        os.system(allure_cmd)

