from FlightApp.pipeline import traning_pipeline
from FlightApp.logger import logging
from FlightApp.exception import FlightException
import os,sys

if __name__=="__main__":
    try:
        logging.info(f"Starting the traning pipeline")
        traning_pipeline.start_traning_pipeline()

    except Exception as e:
        raise FlightException(e,sys)
