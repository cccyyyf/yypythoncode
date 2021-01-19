import allure

from RootPath import RootPath
from objects.interface.InstallMeter.Login.LoginPO import LoginPO
import pytest

from objects.interface.utils.PropertiesUtil import *


@allure.feature("登录测试管理")
class TestLogin(LoginPO):

    public_path = RootPath.getInterfaceIniPath() + "InstallMeter/PublicCase.yml"
    pos_logincase = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="positive_logincase")
    neg_logincase = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="negative_logincase")

    @pytest.mark.parametrize("positive", pos_logincase)   #参数化，每组参数独立运行一次
    def test_posilogin(self,positive):
        res = self.getToken(**self.pos_logincase[positive])   #**字典，*元组
        # 断言请求状态
        assert res["status"] == 'complete'
        # 断言数据库
        sql = "select * FROM org_user where login_name = '%s'" % self.pos_logincase[positive]["loginName"]
        db_result = self.get_DB_data(sql=sql)
        print(db_result)
        assert db_result[0]["login_name"].upper() == self.pos_logincase[positive]["loginName"].upper()

    @pytest.mark.parametrize("negative" ,neg_logincase)
    def test_negalogin(self,negative):
        res = self.getToken(**self.neg_logincase[negative])
        # 断言请求状态
        assert res["status"]== 'error'


