'''
@file: weather_app.py
@author: Sukraat Ahluwalia

The main weather app class. Fetches the recipients from the database
Uses associated utility files to send emails.
'''

import sys
sys.path.append("../")

from collections import defaultdict
from email_sender import email_sender
from message_builder import message_builder
from weather_ops import weather_ops
from utilities.logutils import logutils
from utilities.secrets_manager import secrets_manager

import json
import mysql.connector as mysql_conn

class weather_app:
    def __init__(self):
        '''
        Constructor

        Variables -

        __app_logger    The logging object for this class
        __recipients    A dictionary for email ids associated with their
                        location
        __city_weather  A dictionary that stores the city name and a message
                        containing the weather information to be sent to all
                        recipients that live in this city

        __cities        A set of city names in the DB, used when fetching weather
                        data to avoid making repeated calls for each city to the
                        weather API
        '''
        self.__app_logger = logutils("../logging/server_errs.log", 40)
        self.__recipients = defaultdict()
        self.__city_weather = defaultdict()
        self.__cities = set()

    '''
    Connects to the MySQL database to fetch the email addresses
    for recipients and their city name.
    
    The results are populated in the __recipients class variable
    
    :@return a boolean value indicating success or failure
    '''
    def fetch_recipients(self):
    	with open("../config/config_prod.json") as json_file:
            secret_creds = json.load(json_file)

        secret_name = secret_creds["secret_name"]
        region = secret_creds["region"]

        awssm_obj = secrets_manager(secret_name, region)
        sm_string = awssm_obj.fetch_secrets()

        if len(sm_string) == 0:
            self.__app_logger("Call to Secrets Manager Failed for Weather App")
            return False

        sm_string = json.loads(sm_string)

        db_config = {
            'host': sm_string["host"],
            'user': sm_string["username"],
            'password': sm_string["password"],
            'database': sm_string["dbname"]
        }

        try:
            conn = mysql_conn.connect(**db_config)
        except mysql_conn.Error as mysql_err:
            db_err_str = ""
            if mysql_err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                db_err_str = "Access Denied while connecting to DB for Weather App"
            else:
                db_err_str = "Error occurred while connecting to DB for Weather App"
            self.__app_logger.set_message(db_err_str)
            return False
        else:
            cursor = conn.cursor(buffered=True)
            query = ("SELECT * from addresses")
            cursor.execute(query)

            resultset = cursor.fetchall()

            for email_addr, city in resultset:
                self.__recipients[email_addr] = city
                self.__cities.add(city)

            cursor.close()
            conn.close()

        return True

    '''
    Sends a GET request to the Weather API using the weather_ops class
    only once for each city in the __cities set
    
    populates the __city_weather class variable. Once a new city's weather data
    has been obtained it calls the message builder class to check for the weather
    conditions to build a suitable email to be sent for the city. 
    '''
    def fetch_weather(self):
        weather_ops_obj = weather_ops()
        msg_build = message_builder()

        for city in self.__cities:
            if city not in self.__city_weather.keys():
                h_json = json.loads(weather_ops_obj.fetch_hist_weather(city))
                c_json = json.loads(weather_ops_obj.fetch_curr_weather(city))

                res_json = json.dumps({"temp":c_json["temp"], "avg":h_json["avg_temp"],
                                       "feels":c_json["app_temp"],"weather":c_json["weather"]})


                c_message = msg_build.construct(city, res_json)
                self.__city_weather[city] = c_message

    '''
    Iterates over recipients to fetch the messages stored in __city_weather
    keyed by the city names, uses the email_sender class to establish an SMTP server
    to send the emails. Calls quit_server() to log off from the SMTP server
    '''
    def dispatch_emails(self):
        sender = email_sender()
        sender.login_sender()

        for recipient in self.__recipients:
            recv_city = self.__recipients[recipient]
            msg = self.__city_weather[recv_city]
            sender.send_mail(msg, recipient)

        sender.quit_server()

'''
Main method for this file. 
'''
def main():
    app_main = weather_app()
    #log with logging level INFO
    main_logger = logutils("../logging/WeatherApp.log", 20)

    '''
    Send emails only if the connection to the DB is successful. In case of failure
    there is no recipient list to use to send emails to, in that cases exit logging
    a failure message in the WeatherApp.log file
    '''
    if app_main.fetch_recipients():
        app_main.fetch_weather()
        app_main.dispatch_emails()
        main_logger.set_message("Emails Sent Successfully")
    else:
        main_logger.set_message("System failed to send emails")

if __name__ == '__main__':
    main()
