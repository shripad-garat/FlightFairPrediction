from FlightApp.logger import logging
import os,sys

def error_message_details(error,error_details:sys):
    _,_,exc_tb = error_details.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    logging.error(error_message)
    return error_message
    

class FlightException(Exception):

    def __init__(self, error,error_details:sys):
        self.error_mesage = error_message_details(error=error,error_details=error_details)

    def __str__(self):
        return self.error_mesage
