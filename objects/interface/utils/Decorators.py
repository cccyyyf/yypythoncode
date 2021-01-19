# coding=utf-8

import allure
import requests
from urllib import parse
import json



#post方法，减少重复部分内容
def post(url):
    def NewFunc(fun):
        def wrapper(self,headers, params):
            try:
                if headers['Content-Type'] == 'application/x-www-form-urlencoded':
                    # 字典转换k1=v1 & k2=v2 模式
                    data = parse.urlencode(params)
                else:
                    data = json.dumps(params)
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

        return wrapper
    return NewFunc

# 添加返回值校验,无参数固定值
def responseNoPara(func):
    def wrapper(self):
        func(self)
        allure.attach(body='response["success"] == True', name="检验返回值")
        return func
    return wrapper

# 添加返回值校验，手动填写校验内容
def responseAdd(content):
    def assertFunc(func):
        def wrapper(self):
            func(self)
            allure.attach(body=content, name="检验返回值")
            return func

        return wrapper

    return assertFunc

# 添加数据库校验，手动填写校验内容
def dbcheck(content):
    def assertFunc(func):
        def wrapper(self):
            func(self)
            allure.attach(body=content, name="数据库校验")
            return func

        return wrapper

    return assertFunc