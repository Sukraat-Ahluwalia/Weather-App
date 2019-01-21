'''
@file: weather_app.py
@author: Sukraat Ahluwalia

Main weather app class
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
        self.__app_logger = logutils("../logging/server_errs.log", 40)
        self.__recipients = defaultdict()
        self.__city_weather = defaultdict()
        self.__cities = set()

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

    def dispatch_emails(self):
        sender = email_sender()
        sender.login_sender()

        for recipient in self.__recipients:
            recv_city = self.__recipients[recipient]
            msg = self.__city_weather[recv_city]
            sender.send_mail(msg, recipient)

        sender.quit_server()


def main():
    app_main = weather_app()
    main_logger = logutils("../logging/WeatherApp.log", 20)

    if app_main.fetch_recipients():
        app_main.fetch_weather()
        app_main.dispatch_emails()
        main_logger.set_message("Emails Sent Successfully")
    else:
        main_logger.set_message("System failed to send emails")

if __name__ == '__main__':
    main()
