'''
@file: message_builder.py
@author: Sukraat Ahluwalia

Class for building messages
'''

import json

class message_builder:
    def __init__(self):
        self.__subjects = ["Enjoy a discount on us.",
                         "It's nice out! Enjoy a discount on us.",
                         "Not so nice out? That's okay, enjoy a discount on us.",
                          ]
        self.__failure_message = "Our system was down, enjoy a discount on us anyway"

    def construct(self, city, json_str):
        weather_data = json.loads(json_str)
        curr_temp = weather_data["temp"]
        avg_temp = weather_data["avg"]
        feels_temp = weather_data["feels"]
        weather_type = weather_data["weather"]


        if curr_temp == "failed" or avg_temp == "failed":
             return [self.__subjects[0], self.__failure_message]

        curr_temp_numeric = int(curr_temp)
        avg_temp_numeric = int(avg_temp)

        email_sub = ""

        if weather_type == "Clear Sky" or avg_temp_numeric + 5 == curr_temp_numeric:
            email_sub = self.__subjects[1]
        elif avg_temp_numeric - 5 == curr_temp_numeric:
            email_sub = self.__subjects[2]
        else:
            email_sub = self.__subjects[0]

        main_msg = city + " " + str(curr_temp) + " degrees, " + weather_type
        message = [email_sub, main_msg]


        return message



