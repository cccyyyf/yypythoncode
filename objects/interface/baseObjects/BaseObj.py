# coding=utf-8
import base64
import json
import requests
from urllib import parse
from RootPath import RootPath
from objects.interface.utils.PropertiesUtil import PropertiesUtil


class BaseObj(object):

    @staticmethod
    def do_post(url, params, headers={"Content-Type":"application/json"}):
        try:
            if headers['Content-Type'] == 'application/x-www-form-urlencoded':
                # 字典转换k1=v1 & k2=v2 模式
                data = parse.urlencode(params)
            else:
                data =json.dumps(params)
            response = requests.post(url, data=data, headers=headers)
            print("*******************************************************************************")
            print("Request: " + url)
            print(json.dumps(params))
            if response.status_code != 200 and response.status_code != 401:
                raise Exception("请求失败，status_code=" + str(response.status_code))
            print("-------------------------------------------------------------------------------")
            result = json.loads(str(response.content, 'utf-8'))
            print("Response: ")
            print(result)
            print("*******************************************************************************")
            return result
        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(e)

    @staticmethod
    def do_post_base64encode(url, params,headers={"Content-Type":"application/json"}):
        """
        入参base64加密，出参正常
        """
        try:
            body_str = json.dumps(params)  # 将dic转换成str
            body_b = body_str.encode("utf-8")  # 将str转换成二进制
            body_encode = base64.b64encode(body_b)  # 进行base64加密
            response = requests.post(url, data=body_encode, headers=headers)
            if response.status_code != 200:
                raise Exception("请求失败，status_code=" + str(response.status_code))
            response = response.text

            print()
            print("*******************************************************************************")
            print("Request: " + url)
            print(json.dumps(params))
            print("-------------------------------------------------------------------------------")
            result = json.loads(response)
            print("Response: ")

            print(result)

            print("*******************************************************************************")
            return result
        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(e)

    @staticmethod
    def do_get(url, headers):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise Exception("请求失败，status_code=" + str(response.status_code))
            print("*******************************************************************************")
            print("Request: " + url)
            print("-------------------------------------------------------------------------------")
            result = json.loads(response.text)
            print("Response: ")
            print(result)
            print("*******************************************************************************")
            return result

        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(e)

    @staticmethod
    def do_get_base64decode(url):
        try:
            response_base64 = requests.get(url)
            if response_base64.status_code != 200:
                raise Exception("请求失败，status_code=" + str(response_base64.status_code))
            response = str(base64.b64decode(response_base64.text, ), 'utf-8')
            print("*******************************************************************************")
            print("Request: " + url)
            print("-------------------------------------------------------------------------------")
            result = json.loads(response)
            print("Response: ")
            print(result)
            print("*******************************************************************************")
            return result
        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(e)

    @staticmethod
    def getParas(yamlName, key, paraName=None):
        '''
        读取yaml文件具体参数值,
        path,key必填，
        para不传时会把key下面所有参数获取(返回字典类型)，para传值会返回参数对应的值
        '''
        path = RootPath.getInterfaceIniPath()
        Parameter = PropertiesUtil.loadLocatorValueFromYml(path=path + yamlName, key=key, para=paraName)
        return Parameter

    @staticmethod
    def do_post_base64decode(url, params, headers):
        """
        入参正常，出参base64加密
        """

        try:
            response_base64 = requests.post(url, data=json.dumps(params), headers=headers)
            if response_base64.status_code != 200:
                raise Exception("请求失败，status_code=" + str(response_base64.status_code))
            response = str(base64.b64decode(response_base64.content, ), 'utf-8')
            print()
            print("*******************************************************************************")
            print("Request: " + url)
            print(json.dumps(params))
            print("-------------------------------------------------------------------------------")
            result = json.loads(response)
            print("Response: ")

            print(result)

            print("*******************************************************************************")
            return result
        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(e)

    @staticmethod
    def do_put(url, params, headers) -> dict:
        try:
            print("*******************************************************************************")
            print("Request: " + url)
            response = requests.put(url, json=params,headers=headers)
            if response.status_code != 200:
                raise Exception("请求失败，status_code=" + str(response.status_code))
            print("-------------------------------------------------------------------------------")
            print("Response: ")
            print(response.json())
            print("*******************************************************************************")
            return response.json()
        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(e)

    @staticmethod
    def do_delete(url, headers) -> dict:
        try:
            print("*******************************************************************************")
            print("Request: " + url)
            response = requests.delete(url,headers=headers)
            if response.status_code != 200:
                raise Exception("请求失败，status_code=" + str(response.status_code))
            print("-------------------------------------------------------------------------------")
            print("Response: ")
            print(response.json())
            print("*******************************************************************************")
            return response.json()
        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(e)

