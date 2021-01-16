# coding=utf-8
# Time : 2020/10/15 11:14
# Author : huxin

import os, sys
import jenkins
import json
import requests

"""
将jenkins生成的allure报告发送到钉钉群
"""
# 获取jenkins信息
jenkins_info = sys.argv
job_name = jenkins_info[1]
sys_name = jenkins_info[2]
#sys_name = "设备管理平台"
dd_url = jenkins_info[3]


jenkins_url = "http://10.10.15.132:28080/"
server = jenkins.Jenkins(jenkins_url, username='admin', password='jenkins')

#job_name = "job/autoTest_DevicePlat/"
job_url = jenkins_url + job_name
# 获取最后一次构建数
job_last_number = server.get_info(job_name)['lastBuild']['number']
report_url = job_url + str(job_last_number) + '/allure'
#print(22, report_url)


def send_dd():
    report_data = {}
    RootDir = os.path.abspath(os.path.dirname((__file__)))
    # 测试使用
    f = open(RootDir + '/allure-report/export/prometheusData.txt', 'r')
    # jenkins使用

    for lines in f:
        for c in lines:
            launch_name = lines.strip('\n').split(' ')[0]
            num = lines.strip('\n').split(' ')[1]
            report_data.update({launch_name: num})
    f.close()
    total_num = report_data.get('launch_retries_run')
    passed_num = report_data.get('launch_status_passed')
    failed_num = int(total_num) - int(passed_num)

    if int(total_num) == 0:
        rate = 0
    else:
        rate = round(int(passed_num)/int(total_num), 4)*100

    #dd_url = 'https://oapi.dingtalk.com/robot/send?access_token=4c5f5152e14ed60c906f8c7b49d1c976dab1228180068684c78c97378a7c9b7e'
    content = {"msgtype": "text",
               "text": {
                   "content": "《" + sys_name + "》" + "接口自动化测试脚本执行完毕\n运行成功率： " + str(rate) + "%" + "\n运行总数： " + total_num + "\n通过数量： " + passed_num +
                              "\n失败数量： " + str(failed_num) + "\n报告地址：\n" + report_url + "\n构建地址：\n" + job_url}
               }

    try:
        response = requests.post(url=dd_url, data=json.dumps(content), headers={'Content-Type': 'application/json'})
        print(response.content)
    except Exception as e:
        print("钉钉连接失败")
        print(e)


if __name__ == '__main__':
    send_dd()
