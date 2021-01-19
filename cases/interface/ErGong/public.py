# -*- coding: utf-8 -*-
# @Author  : Felix.Ma
# @Time    : 2021/1/5 16:15
from objects.interface.baseObjects.LoginPO import LoginPO

par_dir = 'resources/interface/ErGong/'
yml_name = 'Public.yml'
login_api_url = '/sso/login'
headers = LoginPO().get_headers("root账号", par_dir, yml_name, login_api_url)


def root_pump_house_sql(params='and true'):
    sql = f"""
        select count(*)
        from (
         select ph.*
         from waterdb_ii.device_pump_house ph
                  inner join waterdb_ii.device rd on ph.id = rd.id_pump_house
         where ph.del_flag = 0
           and rd.del_flag = 0
           {params}
         GROUP BY ph.id) a
        """
    return sql


def query_device_service(deviceId, query='count(*)', params='and true'):
    sql = f"""
    SELECT {query}
    FROM waterdb_ii.point_type pt
         LEFT JOIN waterdb_ii.device_service ds on pt.point_name = ds.point_name
    WHERE pt.point_type = 'real_data'
    AND ds.node_display = '1'
    AND ds.id_device = {deviceId}
    {params}
    ORDER BY ds.data_sort
    """
    return sql


def get_pv_from_sv(today, device, point):
    """

    Args:
        today: 20210114
        device: 20030277//InletPressure

    Returns: 获取秒表里的pv

    """
    sql = f"""
    select pv from waterdb_ds.service_values_{today}
    where ID_DEVICE='{device}'
    and TAG_NAME='{point}'
    order by DATE_TIME desc
    limit 1
    """
    return sql