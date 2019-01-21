'''
@file - email_sender.py
@author - Sukraat Ahluwalia

Class to send an email to a recipient using the SMTP
protocol over SSL.
'''

import sys
sys.path.append("../")

import json
import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from utilities.logutils import logutils
from utilities.secrets_manager import secrets_manager

class email_sender:
    '''
    Constructor

    Variables -

    port                The port no used by SMTP over SSL
    smtp_server         The SMTP server to use
    smtp_server_obj     An object representing the SMTP server
    email_logger        Logging object for this class
    __sender_email      Sender Email ID
    __passwd            Sender's email password
    '''
    def __init__(self):
        self.port = 465
        self.smtp_server = "smtp.gmail.com"
        self.smtp_serv_obj = smtplib.SMTP_SSL(self.smtp_server, self.port)
        self.email_logger = logutils("../logging/server_errs.log", 40)
        self.__sender_email = str()
        self.__passwd = str()

    '''
    Method that logs in to the senders email. 
    
    The username and password are stored in AWS Secrets Manager.
    A call is made to the secrets manager utility class to fetch
    them based on the secret name stored in config_email.json.
    
    Once fetched it uses the credentials to log into the email.
    '''
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

    '''
    Method to send the email.
    
    @:param message     The message to be sent represented as a list
                        [subject. message body]
    @:param recv_addr   The recipients email address
    '''
    def send_mail(self, message, recv_addr):
        '''
        Construct a MIME message assigning the sender, subject
        and message body fields to send the email
        '''
        msg = MIMEMultipart()
        msg['From'] = self.__sender_email + "@gmail.com"
        msg['To'] = recv_addr
        msg['Subject'] = message[0]
        msg.attach(MIMEText(message[1], 'plain'))

        self.smtp_serv_obj.sendmail(self.__sender_email, recv_addr, msg.as_string())

    '''
    Method to quit the connection to the SMTP server
    '''
    def quit_server(self):
        self.smtp_serv_obj.quit()