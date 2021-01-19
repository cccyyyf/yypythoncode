import pymysql
from RootPath import RootPath
from objects.webpage.utils.PropertiesUtil import ConfigUtil

conf = ConfigUtil(RootPath.getSzWebIniPath())


class DbUilts():
	conn = None

	def __init__(self, key):
		self.get_db(key)

	def get_db(self, db):
		db = conf.get("SZ_ACTIVE", db)
		user = conf.get("SZ_ACTIVE", db + "_userName")
		password = conf.get("SZ_ACTIVE", db + "_passWord")
		port = int(conf.get("SZ_ACTIVE", db + "_port"))
		host = conf.get("SZ_ACTIVE", db + "_ip")
		self.conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset='utf8')

	def executeSqlReturnOneCell(self, sql):
		res = ""
		cursor = self.conn.cursor()
		effect_row = cursor.execute(sql)
		self.conn.commit()
		if effect_row:
			res = cursor.fetchall()
		cursor.close()
		self.conn.close()
		return res[0][0]

	def executeSql(self, sql):
		effect_row = 0
		cursor = self.conn.cursor()
		try:
			effect_row = cursor.execute(sql)
			self.conn.commit()
		except:
			self.conn.rollback()
		cursor.close()
		self.conn.close()
		return effect_row