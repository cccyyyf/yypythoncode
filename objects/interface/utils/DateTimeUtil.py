# coding=utf-8
import datetime
import time


def get_current_date():
    """
    :return: 当期日期
    """
    return (datetime.date.today()).strftime("%Y-%m-%d")


def get_now():
    """

    Returns: 当前时间

    """
    return (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")


def get_datetime_format(time_str):
    """

    Args:
        time_str: 字符串

    Returns: datetime格式

    """
    return datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")


def get_time_difference(a, b):
    """

    Args:
        a:
        b:

    Returns: 两时间之前的秒级时间差(绝对值)

    """
    return abs((get_datetime_format(a) - get_datetime_format(b)).seconds)


def get_future_date(days):
    """
    :param days: 未来天数
    :return: 未来日期
    """
    return (datetime.date.today() + datetime.timedelta(days=days)).strftime("%Y-%m-%d")

def get_last_date(days):
    """
    获取过去某天的日期
    """
    return (datetime.date.today() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")

def get_time_stamp():
    """
    :return: 时间戳
    """
    return int(round(time.time() * 1000))


def cal_future_date(str_date, days):
    """
    :param str_date: 日期
    :param days: 天数
    :return: 未来日期
    """
    d_date = datetime.datetime.strptime(str_date, "%Y-%m-%d")
    return (d_date + datetime.timedelta(days=days)).strftime("%Y-%m-%d")


def compare_airline_date(dep_time, arr_time, duration):
    """
    -1 - 出发到达时间计算错误
    return跨天天数
    """
    dep = list()
    arr = list()
    dur = list()
    dep_s = str.split(dep_time, ":")
    dep.append(int(dep_s[0]))
    dep.append(int(dep_s[1]))
    arr_s = str.split(arr_time, ":")
    arr.append(int(arr_s[0]))
    arr.append(int(arr_s[1]))
    dur.append(int(str.split(duration, "h")[0]))
    dur.append(int(str.split(str.split(duration, "h")[1], "m")[0]))
    if (dep[1]+dur[1]) % 60 != arr[1] or ((dep[0]+dur[0]) % 24)+int((dep[1]+dur[1]) / 60) != arr[0]:
        return -1
    else:
        return int((dep[0]+dur[0]+((dep[1]+dur[1]) / 60)) / 24)
