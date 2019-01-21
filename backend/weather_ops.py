'''
@file: weather_ops.py
@author: Sukraat Ahluwalia

Class that sends requests to the Weather API and contains
methods for storing and returning weather based data
'''
import sys
sys.path.append("../")

import json
import os
import requests as req
from datetime import datetime as dt
from datetime import timedelta as tdelta
from utilities.logutils import logutils

'''
Class for weather data based operations.
'''
class weather_ops:
    '''
    Constructor

    Class Variables
    __hist_weather_req      Request string to be passed to the historical weather API
    __curr_weather_req      Request string passed to the current weather API
    __start_date            Start date parameter for the weather request
    __end_date              End date parameter for the weather request
    __start_date_str        String representation of the start date
    __end_date_str          String representation of the end date
    __api_key               API key for the Weather API, stored as an environment variable
    __w_log_obj             Object for logging utilities

    '''
    def __init__(self):
        self.__hist_weather_req = "https://api.weatherbit.io/v2.0/history/daily?city="
        self.__curr_weather_req = "https://api.weatherbit.io/v2.0/current?city="
        self.__start_date = dt.today()
        self.__end_date = self.__start_date + tdelta(days=1)
        self.__start_date_str = "&start_date=" + self.__start_date.strftime("%Y-%m-%d")
        self.__end_date_str = "&end_date="+self.__end_date.strftime("%Y-%m-%d")
        self.__api_key = "&key=" + os.environ['WEATHER_API_KEY']
        self.__w_log_obj = logutils("../logging/server_errs.log", 40)

    '''        
    Method to send a request to the Weather API for a particular city. Fetches historical average 
    temperature among other things. 
    
    @:param     city_name   Name of the city 
    @:return    JSON output with current temparature or failure in case the request to the API failed
    '''
    def fetch_hist_weather(self, city_name):
        hist_req_str = self.__hist_weather_req+city_name+self.__start_date_str+self.__end_date_str+self.__api_key
        hist_res = req.get(hist_req_str)
        json_str = ""

        if hist_res.status_code == 200:
            h_weather_json = json.loads(hist_res.text)
            # The temperature is stored in the data part of the JSON
            # as a list hence the [0] key to access it
            avg_temp = h_weather_json["data"][0]["temp"]
            json_str = json.dumps({"avg_temp":avg_temp})

        else:
            status_code = str(hist_res.status_code)
            message = "Call to Weather API for historical weather failed with status code HTTP " + status_code
            self.__w_log_obj.set_message(message)
            json_str = json.dumps({"avg_temp":"failed"})

        return json_str


    '''
    Method to send a request to the Weather API to fetch the current temperature and weather among other
    things
    
    @:param     city_name   Name of the city
    @:return    JSON output with current temparature or failure in case the request to the API failed
    '''
    def fetch_curr_weather(self, city_name):
        curr_req_str = self.__curr_weather_req+city_name+self.__api_key
        curr_res = req.get(curr_req_str)
        curr_json_str = ""

        if curr_res.status_code == 200:
            c_weather_json = json.loads(curr_res.text)
            # In this response as well the data part of the JSON
            # response is stored as a list, hence the use of [0]
            # to access it.
            curr_temp = c_weather_json["data"][0]["temp"]
            curr_feels_like = c_weather_json["data"][0]["app_temp"]
            curr_condition = c_weather_json["data"][0]["weather"]["description"]

            curr_json_str = json.dumps({"temp":curr_temp, "app_temp": curr_feels_like, "weather":curr_condition})
        else:
            status_code = str(curr_res.status_code)
            message = "Call to Weather API for current weather failed with status code HTTP " + status_code
            self.__w_log_obj.set_message(message)
            curr_json_str = json.dumps({"temp":"failed", "app_temp":"failed", "weather":"failed"})

        return curr_json_str