#2021/07/21
'''
数据驱动用于管理测试数据，基于数据驱动行为，结合主流设计模式一起应用于自动化测试
关键字驱动即为selenium二次封装
数据与代码分离
测试代码与逻辑代码分离，测试代码调用逻辑代码
'''

import unittest

from WebUiKey.Keys import Key
from ddt import ddt,file_data

@ddt
class Case2(unittest.TestCase):
    #前置条件
    def setUp(self) -> None:
        self.key = Key('Chrome')


    #后置条件
    def tearDown(self) -> None:
        self.key.quit()

    @file_data('../Data/Search.yaml')
    def test_01(self, **kwargs):
        self.key.open(kwargs['url'])
        self.key.maxwindow()
        self.key.input(**kwargs['input'])
        self.key.click(**kwargs['click'])
        self.key.sleep(kwargs['sleep'])



if __name__ == '__main__':
    unittest.main()