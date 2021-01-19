import os, json
from RootPath import RootPath
import yaml
from selenium.webdriver.common.by import By
import configparser


class PropertiesUtil:
    @classmethod
    def loadLocatorValueFromYml(cls, path, key):
        f = open(path, encoding='utf-8')
        res = yaml.load(f, Loader=yaml.FullLoader)
        locator = res.get(key)["locator"].upper()
        value = res.get(key)["value"]
        f.close()
        return (eval("By." + locator), value)


class ConfigUtil(object):
    def __init__(self, path):
        self.path = path

        if not os.path.exists(self.path):
            raise IOError('file {} not found!'.format(self.path))
        try:
            self.cf = configparser.ConfigParser()
            self.cf.read(self.path)
        except Exception as e:
            raise IOError(str(e))

    def get(self, section, key):
        #active_section = self.cf.get(section, key)
        return self.cf.get(section, key)
