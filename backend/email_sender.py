'''
@file - email_sender.py
@author - Sukraat Ahluwalia

Class to send an email to a recipient using SMTP ()
'''

import sys
sys.path.append("../")

import json
import smtplib
import ssl

from utilities import logutils
from utilities import secrets_manager

class email_sender:
    def __init__(self):
        self.port = 587
        self.context = ssl.create_default_context()
        self.smtp_server = "smtp.gmail.com"
        self.smtp_serv_obj = smtplib.SMTP(self.smtp_server, self.port)
        self.smtp_serv_obj.starttls(self.context)
        self.email_logger = logutils("../logging/server_errs.log", "warn")
        self.__sender_email = str()
        self.__passwd = str()

    def login_sender(self):
        with open('../config/config_email.json') as json_file:
            secret_creds = json.load(json_file)

        secret_name = secret_creds["em_sname"]
        region = secret_creds["region"]

        awssm_obj = secrets_manager(secret_name, region)
        login_json = awssm_obj.fetch_secrets()

        login_creds = json.loads(login_json)
        self.__sender_email = login_creds["email"]
        self.__passwd = login_creds["password"]

        self.smtp_serv_obj.login(self.__sender_email, self.__passwd)

    def send_mail(self, message, recv_addr):
        self.smtp_serv_obj.sendmail(self.__sender_email, recv_addr, message)

    def quit_server(self):
        self.smtp_serv_obj.quit()