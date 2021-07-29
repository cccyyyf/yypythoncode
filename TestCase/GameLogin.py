'''
2021/7/29
营收登录
'''

import unittest
from WebUiKey.Keys import Key
from ddt import ddt,file_data


@ddt
class GameLogin(unittest.TestCase):
    def setUp(self) -> None:
        self.key = Key('Chrome')

    def tearDown(self) -> None:
        self.key.quit()

    @file_data("../Data/GameLogin.yaml")
    def test_login1(self, **kwargs):
        self.key.open(kwargs['url'])
        self.key.maxwindow()
        self.key.sleep(kwargs['sleep'])
        self.key.input(**kwargs['inputname'])
        self.key.input(**kwargs['inputpwd'])
        # self.key.click(**kwargs['click'])
        # res = self.key.allege()
        # print(res)
        self.key.sleep(kwargs['sleep'])


if __name__ == '__main__':
    unittest.main()