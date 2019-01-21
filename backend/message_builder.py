'''
@file: message_builder.py
@author: Sukraat Ahluwalia

Class for building messages
'''

import json

class message_builder:
    '''
    Constructor

    Variables -
    __subjects          List of subjects based on weather conditions
    __failure_message   In case the requests to the weather API fail then
                        send a system down message as part of the email

    '''
    def __init__(self):
        self.__subjects = ["Enjoy a discount on us.",
                         "It's nice out! Enjoy a discount on us.",
                         "Not so nice out? That's okay, enjoy a discount on us.",
                          ]
        self.__failure_message = "Our system was down, enjoy a discount on us anyway"


    '''
    Method that constructs the subject and the message body for the email.
    
    @:param city        Name of the city
    @:param json_str    JSON representation of the city's weather
    
    @:return    A list containing the subject and the message body     
    '''
    def construct(self, city, json_str):
        weather_data = json.loads(json_str)
        curr_temp = weather_data["temp"]
        avg_temp = weather_data["avg"]
        weather_type = weather_data["weather"]

        # In case the API calls fail send the system down failure message
        # with the 'Enjoy a discount on us' Subject
        if curr_temp == "failed" or avg_temp == "failed":
             return [self.__subjects[0], self.__failure_message]

        # Casted to int rather than float to avoid the
        # approximations of floating point arithmetic in calculations
        curr_temp_numeric = int(curr_temp)
        avg_temp_numeric = int(avg_temp)

        email_sub = ""

        '''
        If the weather is Sunny or 5 degrees warmer -> 'It's nice out'
        If the weather is cooler by 5 degrees -> 'Not so nice out'
        else -> 'Enjoy a discount on us'
        '''
        if weather_type == "Clear Sky" or avg_temp_numeric + 5 == curr_temp_numeric:
            email_sub = self.__subjects[1]
        elif avg_temp_numeric - 5 == curr_temp_numeric:
            email_sub = self.__subjects[2]
        else:
            email_sub = self.__subjects[0]

        # Construct the message body and send
        main_msg = city + " " + str(curr_temp) + " degrees, " + weather_type
        message = [email_sub, main_msg]


        return message



