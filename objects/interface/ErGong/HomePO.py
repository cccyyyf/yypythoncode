from objects.interface.baseObjects.BaseObj import *
from objects.interface.utils.DBRequest import db_query
from objects.interface.utils.Decorators import post
from objects.interface.utils.PropertiesUtil import *
from RootPath import *
import allure


class HomePO(BaseObj):
    public_path = RootPath.getErGongPath() + "Public.yml"
    request_info = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="接口信息")
    DB_info = PropertiesUtil.loadLocatorValueFromYml(path=public_path, key="DB信息")

    @allure.step("获取数据库中的信息")
    def get_DB_data(self, sql) -> list:
        """
        根据sql获取数据库的值
        """
        result = db_query(self.DB_info["devicecenter"], sql)
        return result

    @allure.step("设备树接口")
    @post(request_info["url"] + "/home/tree")
    def home_tree(self, headers, params):
        pass

    @allure.step("地图所有泵房")
    @post(request_info["url"] + "/home/allPumpHouse")
    def all_pump_house(self, headers, params):
        pass
