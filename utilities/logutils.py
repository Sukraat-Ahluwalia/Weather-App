'''
@file: logutils.py
@author: Sukraat Ahluwalia

Class for using Python's logging functionality.
'''
import logging
from datetime import datetime as dt

'''
Class for logging messages for events in the application. Accepts a file name
and logging level for logging purposes. 
'''
class logutils:
    '''
    Constructor

    @:param     filename    File name to log messages to
    @:param     level       The logging level represented as an
                            integer value
    '''
    def __init__(self, filename, level):
        self.__level = level
        logging.basicConfig(level=level,filename=filename)

    '''
    Method to log the message to the file specified in the constructor
    
    @:param     message     Message to be logged
    
    The message is logged as date-time followed by the message passed
    '''
    def set_message(self, message):
        message = dt.now().strftime("%m-%d-%Y") + " " + message
        logging.log(self.__level, message)
