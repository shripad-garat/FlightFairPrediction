from FlightApp.entity import config_entity,artifact_entity
from FlightApp.utility import get_data_
from FlightApp.logger import logging
from FlightApp.exception import FlightException
from sklearn.model_selection import train_test_split
import os,sys

class DataIngestion:

    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise FlightException(e,sys)


    def initated_data_ingestion(self):
        try:
            logging.info("Initate the dsata Ingestion")
            logging.info(f"Getting the data from Database in DataFrame format")
            self.df = get_data_(self.data_ingestion_config.Database,self.data_ingestion_config.Collection)
            logging.info(f"Dropping the NA and duplicate datapoints")
            self.df.dropna(inplace=True)
            self.df.drop_duplicates(inplace=True)
            logging.info("Getting the path for storing dataset into features and dataset dir")
            feature_store_path = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            dataset_path = os.path.dirname(self.data_ingestion_config.test_file_path)
            logging.info("Making the directory is not exist")
            os.makedirs(feature_store_path,exist_ok=True)
            os.makedirs(dataset_path,exist_ok=True)
            logging.info("Spliting the data into tarin and test dataset")
            self.train,self.test = train_test_split(self.df,test_size=self.data_ingestion_config.test_size,random_state=110)
            logging.info("Saving the Data in feature store and dataset dir")
            self.df.to_csv(self.data_ingestion_config.feature_store_file_path,index=False,header=True)
            self.train.to_csv(self.data_ingestion_config.train_file_path,index=False,header=True)
            self.test.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)
            logging.info("Preparing the data ingestion artifact")
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_path=self.data_ingestion_config.feature_store_file_path,
                train_path=self.data_ingestion_config.train_file_path,
                test_path=self.data_ingestion_config.test_file_path
            )
            logging.info("Completed the Data Ingestion")
            return data_ingestion_artifact




        except Exception as e:
            raise FlightException(e,sys)