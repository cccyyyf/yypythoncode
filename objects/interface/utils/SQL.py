import pymysql


def search(sql):
    db = pymysql.connect(host="10.10.15.168", user="wpg", password="Wpg@_@MySQL2oIg", db="waterdb_bz_dev")
    cursor = db.cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    db.close()
    return res
