'''
@file: db_conn.py
@author: Sukraat Ahluwalia

Classes for DB utilities including connection to AWS secrets manager
and MySQL. 
'''
import sys
sys.path.append("../")

import json
import mysql.connector as mysql_conn

from utilities import logutils
from utilities import secrets_manager

class db_conn:
	#constructor
	def __init__(self, email_id, location):
		self.__email_id = email_id
		self.__location = location
		self.__client_log = logutils('../logging/client_errs.log', 'warn')

	'''
	Checks whether the email address exists in the database. If it does
	then return failure, else insert the record in the database and return
	success
	'''
	def check_insert(self):
		with open('../config/config_prod.json') as json_file:
			secret_creds = json.load(json_file)

		secret_name = secret_creds["secret_name"]
		region = secret_creds["region"]

		awssm_obj = secrets_manager(secret_name, region)
		sm_string = awssm_obj.fetch_secrets()

		if len(sm_string) == 0:
			self.__client_log.set_message("Call to Secrets Manager failed on client side")
			return False

		sm_string = json.loads(sm_string)

		db_config = {
			'host' : sm_string["host"],
			'user' : sm_string["username"],
			'password' : sm_string["password"],
			'database' : sm_string["dbname"]
		}
		
		'''
		Just like the function above, establish connection to the
		service then execute queries. In case of failure determine the
		error and log it into the log files.

		First check if the record already exists. If it does then error out
		else insert and return success.
		'''
		try:
			conn = mysql_conn.connect(**db_config)
		except mysql_conn.Error as mysql_err:
			db_err_str = ""
			if mysql_err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				db_err_str = " Access Denied while connecting to DB at "
			else:
				db_err_str = " Error occurred while connecting to DB at "
			self.__client_log.set_message(db_err_str)
		else:
			cursor = conn.cursor(buffered=True)
			query = ("SELECT COUNT(%s) from addresses where email_addr=%s")
			cursor.execute(query , (self.__email_id, self.__email_id))

			if cursor.rowcount > 1:
				return False

			ins_query = ("INSERT INTO addresses VALUES(%s, %s)")
			cursor.execute(ins_query, (self.__email_id, self.__location))

			conn.commit()
			cursor.close()
			conn.close()

		return True	
			
