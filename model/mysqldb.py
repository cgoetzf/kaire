import globals as g
import mysql.connector

class mysqlConn:

	def __init__(self):
		self.conn = mysql.connector.connect(user=g.MYSQL_USER, password=g.MYSQL_PASS, host=g.MYSQL_HOST, database=g.MYSQL_DB)
		
	def close(self):
		self.conn.close()

	def commit(self):
		self.conn.commit()
		
	def cursor(self):
		return self.conn.cursor()
	
	#return ID
	def insert(self, tablename, fields, dataset):
		cursor = self.cursor()
		fieldLen = len(fields)-1
		cmd = "INSERT INTO " + tablename + " ("
		for field in fields:
			cmd += field
			if fields.index(field) != fieldLen:
				cmd += ","
			else:
				cmd += ")"
		cmd += " VALUES ("
		for x in range(fieldLen+1):
			cmd += "%s"
			if x != fieldLen:
				cmd += ","
			else:
				cmd += ")"
		#print(cmd)
		cursor.execute(cmd, dataset)
		id = cursor.lastrowid
		self.commit()
		cursor.close()
		return id