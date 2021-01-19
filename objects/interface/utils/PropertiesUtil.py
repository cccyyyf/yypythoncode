# coding=utf-8
import os, json
import yaml
import configparser


class PropertiesUtil:
    @classmethod
    def loadLocatorValueFromYml(cls, path, key, para=None):
        """
        path,key必填，para不传时会把key下面所有参数获取(返回字典类型)，para传值会返回参数对应的值
        """
        f = open(path, encoding='utf-8')
        res = yaml.load(f, Loader=yaml.FullLoader)
        if para is None:
            value = res.get(key)
        else:
            value = res.get(key)[para]
        f.close()
        return value


class ConfigUtil:
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
        active_section = self.cf.get(section, key)
        #return self.cf.get(active_section, key)
        return active_section
