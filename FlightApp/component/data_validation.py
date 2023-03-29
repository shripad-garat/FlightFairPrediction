from FlightApp.logger import logging
from FlightApp.exception import FlightException
from FlightApp.entity import artifact_entity,config_entity
import pandas as pd 
from FlightApp import utility
import os,sys


class DataValidation:

    def __init__(self,data_validation_config:config_entity.DataValidationnConfig,data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_status = {"train_df":True,"test_df":True}

        except Exception as e:
            raise FlightException(e,sys)


    def drop_missing_values_columns(self,dataset:pd.DataFrame):
        try:
            logging.info("Finding the columns with null valuse higher than threshold ")
            for col in dataset.columns:
                if dataset[col].isnull().sum() > dataset.shape[0]*self.data_validation_config.missing_threshold:
                    logging.info(f"Dropin the column {col}")
                    dataset.drop(col,inplace=True)
            logging.info(f"Completed the check for missing value columns for {dataset}")
            return dataset

        except Exception as e:
            raise FlightException(e,sys)

    
    def is_required_feature_avalable(self,current_dataset):
        try:
            logging.info("Checking for Features/columns required in the dataset is present or not?")
            validation_checks = {
                'required_feature':True,
                'missing_column': [],
            }
            based_column = self.base_df.columns
            current_column = current_dataset.columns
            for col in based_column:
                if col not in current_column:
                    logging.info("Failed In passing the validation")
                    validation_checks['required_feature'] = False
                    validation_checks['missing_column'].append(col)
                    self.validation_status[str(current_dataset)] = False


            logging.info(f"Completed the validation check for {current_dataset}")
            return validation_checks
        except Exception as e:
            raise FlightException(e,sys)



    def initated_data_validation(self):
        try:
            logging.info("Initalizing the the data validation")
            logging.info("Creating the status call")
            train_report_status = {}
            test_report_status = {}
            report = {}
            logging.info("Importing the based dataset for comapring the given dataset \nAlso importing the train and test dataset ")
            base_df = pd.read_excel(self.data_validation_config.based_data_path)
            train_df = pd.read_csv(self.data_ingestion_artifact.train_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_path)
            logging.info("Checking for missing values if its exicute the threshold")
            self.base_df = self.drop_missing_values_columns(base_df)
            train_df = self.drop_missing_values_columns(train_df)
            test_df = self.drop_missing_values_columns(test_df)
            logging.info("Checking if the required features/cloumns are present in the datasets")
            train_report_status['Is_required_features_avalable'] = self.is_required_feature_avalable(train_df)
            test_report_status['Is_required_features_avalable'] = self.is_required_feature_avalable(test_df)
            logging.info("Saving the datasets")
            if self.validation_status['train_df']==False:
                logging.info("Saving the dataset into bad dataset dir as its fails the validation")
                utility.save_data_to_csv(train_df,self.data_validation_config.bad_train_path)
            else:
                logging.info("Saving the dataset into the good dataset dir")
                utility.save_data_to_csv(train_df,self.data_validation_config.good_train_path)
            
            if self.validation_status['test_df']==False:
                logging.info("Saving the dataset into bad dataset dir as its fails the validation")
                utility.save_data_to_csv(train_df,self.data_validation_config.bad_test_path)
            else:
                logging.info("Saving the dataset into the good dataset dir")
                utility.save_data_to_csv(train_df,self.data_validation_config.good_test_path)
            logging.info("Writting thw report into the yaml file")
            report['train_df_report'] = train_report_status
            report['test_df_report'] = test_report_status
            utility.write_yaml_report(report,self.data_validation_config.report_path)
            logging.info("Preparing the artifacts for data validation")
            data_validation_artifact = artifact_entity.DataValidationArtifact(
                report_path=self.data_validation_config.report_path,
                good_dataset_train_path=self.data_validation_config.good_train_path,
                good_dataset_test_path=self.data_validation_config.good_test_path,
                bad_dataset_train_path=self.data_validation_config.bad_train_path,
                bad_dataset_test_path=self.data_validation_config.bad_test_path
            )
            logging.info("Completing the data validation")
            return data_validation_artifact




        except Exception as e:
            raise FlightException(e,sys)