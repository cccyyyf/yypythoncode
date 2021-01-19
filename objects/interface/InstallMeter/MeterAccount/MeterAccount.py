import allure
import objects.interface.utils.common as common
from objects.interface.baseObjects.BaseObj import BaseObj


class MeterAccountPO(BaseObj):
    def getHeader(self):
        header = self.getParas(yamlName='InstallMeter/HomePage.yml', key='公共变量', paraName='headers')
        token = common.gettoken()
        header.update({"Authorization": token})
        return header

    def geturl(self):
        return self.getParas(yamlName='InstallMeter/HomePage.yml', key='168服务器接口地址',
                            paraName='url')


    # post接口
    @allure.step("post请求")
    def meterAccountpost(self, body, url):
        url = self.geturl() + url
        header = self.getHeader()
        try:
            res = self.do_post(url=url, params=body, headers=header)
            return res
        except Exception as e:
            print("失败!")
            print(e)

    # put接口
    @allure.step("put请求")
    def meterAccountput(self, body, url):
        url = self.geturl() + url
        header = self.getHeader()
        try:
            res = self.do_put(url=url, params=body, headers=header)
            return res
        except Exception as e:
            print("失败!")
            print(e)

    # get接口，需要参数
    @allure.step("get请求")
    def meterAccountget(self, body, url):
        url = self.geturl() + url
        header = self.getHeader()
        try:
            res = self.do_get_canshu(url=url, params=body, headers=header)
            return res
        except Exception as e:
            print("失败!")
            print(e)

    #delete接口
    @allure.step("delete请求")
    def meterAccountdel(self,body,url):
        url = self.geturl() + url
        header = self.getHeader()
        try:
            res = self.do_delete(url=url,params=body,headers=header)
            return res
        except Exception as e:
            print("失败！")
            print(e)


