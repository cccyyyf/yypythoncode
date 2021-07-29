#2021/07/25
#github登录

from WebUiKey.Keys import Key
from ddt import ddt,file_data
import unittest

@ddt
class GitLogin(unittest.TestCase):
    def setUp(self):
        self.key = Key('Chrome')

    def tearDown(self) -> None:
        self.key.quit()

    @file_data('../Data/Login.yaml')
    def test_login(self,**kwargs):
        self.key.open(kwargs['url'])
        self.key.click(**kwargs['click'])


if __name__ == '__main__':
    unittest.main()