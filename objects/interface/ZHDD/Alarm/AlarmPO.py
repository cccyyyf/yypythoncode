# coding=utf-8
# Author: huxin
# Time : 2020/9/13:22:52

import allure
from objects.interface.baseObjects.BaseObj import BaseObj
from objects.interface.utils.DBRequest import *
from RootPath import RootPath
from configparser import ConfigParser
import json



class AlarmPO(BaseObj):

    @allure.step("获取token")
    def getToken(self, loginName, password):
        """
        获取token值
        """
        url = 'http://122.112.215.244/apiPortalUser/sso/login'
        body = {'loginName': loginName, 'password': password}
        try:
            response = self.do_post(url=url, params=body)
            token = response["resultData"]["token"]
            return token
        except Exception as e:
            print("获取token失败")
            print(e)

    @allure.step("获取告警信息")
    def getAlarmData(self,loginName,password,body):
        headers = self.getParas(yamlName='HomePage.yml', key='公共变量', paraName='headers')
        Authorization = self.getToken(loginName,password)
        headers.update({"Authorization": Authorization})
        url = self.getParas(yamlName='HomePage.yml', key='接口地址',
                            paraName='url') + "/apiPipe/homepage/getAlarmProportion"
        result = self.do_post(url=url, params=body, headers=headers)
        return result

    def get_DB_data(self,sql) -> list:
        """
        根据sql获取数据库的值
        """
        ini_file = RootPath.getInterfaceIniPath() + "ZHDD.ini"
        content = ConfigParser()
        content.read(ini_file)
        db_info = content.get("ZHDD_INFO", "db_info")
        db_info = json.loads(db_info)
        result = db_query(db_info["waterdb_pipe"],sql)
        return result