'''
@file: db_conn.py
@author: Sukraat Ahluwalia

Classes for DB utilities including connection to AWS secrets manager
and MySQL. 
'''
import json
import boto3
import logging
import datetime as dtime
import mysql.connector as mysql_conn
from botocore.exceptions import ClientError

class db_conn:
	#constructor
	def __init__(self, email_id, location):
		self.email_id = email_id
		self.location = location
		logging.basicConfig(filename='../../logging/client_errs.log')
	'''
	@function get_secrets
	Connects with AWS Secrets Manager to get the
	DB credentials. Returns an error upon failure

	On success returns the DB credentials
	'''
	def get_secrets(self):
		secret_str = ""
		
		#load the credentials to be sent to secrets manager
		with open('../../config/config_prod.json') as json_file:
			secrets_creds = json.load(json_file)

		secret_name = secret_creds["secret_name"]
		region = secret_creds["region"]


		aws_session = boto3.session.Session()
		sm_client = aws_session.client(
			service_name='secretsmanager',
			region_name=region
		)

		try:
			awssm_response = sm_client.get_secret_value(SecretId=secret_name)
		except ClientError as cl_err:
			'''
			Determine the correct error and log it into
			the log files with the current time
			'''
			sm_err_str = ""
			if cl_err.response['Error']['Code'] == 'DecryptionFailureException':
				sm_err_str = " Decryption Failure for Secrets Manager" 
				raise cl_err		
			elif cl_err.response['Error']['Code'] == 'ResourceNotFoundException':
				sm_err_str = " Resource Not Found Error for Secrets Manager" 
			elif cl_err.response['Error']['Code'] == 'InvalidRequestException':
				sm_err_str = " Invalid Request to Secrets Manager" 
			else:
				sm_err_str = "Error Occured for Secrets Manager " 
			logging.debug(dt.datetime.now() + sm_err_str)
		else:
			if 'SecretString' in awssm_response:
				secret_str = awssm_response['SecretString']
		

		return secret_str


	'''
	Checks whether the email address exists in the database. If it does
	then return failure, else insert the record in the database and return
	success
	'''
	def check_insert(self):
		sm_string = self.get_secrets()		
		
		if len(sm_string) == 0:
			logging.debug(dt.datetime.now() + " Call to Secrets Manager Failed")	
			return False

		sm_string_vals = json.load(sm_string)
		db_config = {
			'host' : sm_string_vals["host"],
			'user' : sm_string_vals["user"],
			'password' : sm_string_vals["password"],
			'database' : sm_string_vals["dbname"]
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
			logging.debug(dt.datetime.now() + db_err_str)
		else:
			cursor = conn.cursor()
			query = ("SELECT COUNT(%s) from addresses where email_addr=%s")
			cursor.execute(query , (self.email_id, self.email_id))

			if len(cursor) > 0:
				return False


			ins_query = ("INSERT INTO addresses VALUES(%s, %s)")
			cursor.execute(ins_query, (self.email_id, self.location))

			conn.commit()
			cursor.close()
			conn.close()

		return True	
			
