import allure
import pytest

from objects.interface.ErGong.SynUserInfoPO import SynUserInfoPO, RootPath, PropertiesUtil


@allure.feature("获取用户")
class TestUser(SynUserInfoPO):
    public_path = RootPath.getErGongPath() + "Public.yml"
    request_info = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="接口信息")

    def setup_class(self):
        self.headers = self.request_info["headers"]

    @allure.story("登录-正常登录-回归")
    def test_login_correct(self):
        body = {
            "loginName": "datong",
            "password": "123456"
        }
        result = self.login(headers=self.headers,body=body)
        assert result["status"] == "complete"


if __name__ == '__main__':
    pytest.main()
