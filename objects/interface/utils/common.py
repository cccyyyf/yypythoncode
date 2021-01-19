import requests


def gettoken():
    url = "http://10.10.15.168:8999/sso/login"  # 构造请求
    data = {
        "loginName": "linhz",
        "password": "Lhz123456",
    }
    res = requests.post(url=url, json=data)
    token = res.json().get("resultData").get("token")
    return token



