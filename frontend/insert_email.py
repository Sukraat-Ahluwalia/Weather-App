'''
@file: insert_email.py
@author: Sukraat Ahluwalia

Receives email address and location from the client side
To insert into the database.
'''
from flask import request, redirect, render_template
from flask import Flask
from db_conn import db_conn
app = Flask(__name__)

@app.route('/insert_db', methods = ['POST'])
def insert_db():
	email_str = request.form["email_address"]
	location = request.form["location"]

	# In case of success render the success webpage
	# otherwise render the failure page in case
	# of failure or if the email already exists in the
	# database
	conn_obj = db_conn(email_str, location)
	if conn_obj.check_insert():
		return render_template('success.html')

	return render_template('failure.html')
