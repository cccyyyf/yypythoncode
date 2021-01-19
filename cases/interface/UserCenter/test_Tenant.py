# coding=utf-8
# Time : 2020/9/27 18:08
# Author : wanghui
from objects.interface.UserCenter.Tenant import TenantPO


class TestTenant(TenantPO):
    #调用获取租户列表接口
    def get_TenantList(self, *args):
        data = {"keyword": "", "activateFlag": [], "productId": [], "type": "", "currentPage": 1, "pageSize": 20}
        url = "http://10.10.15.213:8877/userCenterApi/tenant/list"
        headers = {'Content-Type': 'application/json', 'Authorization': str(args)}
        try:
            response = self.do_post(url=url, params=data, headers=headers)
            res = response
            return res
        except Exception as e:
            print("获取租户列表失败")
            print(e)

    # 验证租户列表数据
    def test_verfiyTenantList(self):
        login_data = {"url": "http://10.10.15.213:8877/userCenterApi/auth/login", "loginName": "admin",
                      "password": "123456"}
        login_token = self.getToken(**login_data)
        res = self.get_TenantList(*login_token)
        print(res["count"])
        # 断言返回值
        assert res["count"] == 23




# 调试代码就把main开关打开
# post方法请求示例
if __name__ == '__main__':
    test_fun = TestTenant()
    print(test_fun.test_verfiyTenantList())

