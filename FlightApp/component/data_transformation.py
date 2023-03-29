from FlightApp.exception import FlightException
from FlightApp.logger import logging
from FlightApp.entity import artifact_entity,config_entity
from FlightApp import utility
import pandas as pd
import numpy as np
import os,sys,warnings
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder
from sklearn.compose import make_column_transformer

warnings.filterwarnings('ignore')

class DataTransformation: 

    def __init__(self,data_transformation_config:config_entity.DataTransformationhConfig,data_validation_artifact:artifact_entity.DataValidationArtifact):
        try: 
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact

        except Exception as e:
            raise FlightException(e,sys)

    @classmethod
    def split_route(cls,spliter,df):
        try:
            
            logging.info("Getting the splited routes from route feature")
            df['Route'] = df['Route'].apply(lambda x: x.split(spliter))
            
            for i in range(6):
                if i == 0:
                    df['Source_Route'] = '0'    
                else:
                    df[f'Route_{i}'] = '0'
            for i in range(len(df["Route"])):
                for j in range(len(df['Route'].iloc[i])):
                    if j == 0:
                        df['Source_Route'].iloc[i] = df['Route'].iloc[i][j]
                    else:
                        df[f'Route_{j}'].iloc[i] = df['Route'].iloc[i][j]
            
            df.drop('Route',axis=1,inplace=True)
            return df

        except Exception as e:
            raise FlightException(e,sys)

    @classmethod
    def data_extraction_transformation(cls,df:pd.DataFrame)->pd.DataFrame:
        try:
            logging.info("Starting the Data extraction from data set")
            '''Read Note book for beter understand of General data transformation '''
            df['Date_of_Journey'] = pd.to_datetime(df['Date_of_Journey'])
            df['day_name'] = df['Date_of_Journey'].dt.day_name()
            df['day'] = df['Date_of_Journey'].dt.day
            df['month'] = df['Date_of_Journey'].dt.month
            df['quarter'] = df['Date_of_Journey'].dt.quarter
            df = df.drop("Date_of_Journey",axis=1)
            df['Destination'].replace("New Delhi","Delhi",inplace=True)
            spliter = df['Route'][0].split()[1]
            df = DataTransformation.split_route(spliter,df)
            df['Dep_Time'] = pd.to_datetime(df['Dep_Time'])
            df['Dep_Time_Hr'] = df['Dep_Time'].dt.hour
            df['Dep_Time_Min'] = df['Dep_Time'].dt.minute
            df.drop('Dep_Time',axis=1,inplace=True)
            df['Arrival_Time_'] = pd.to_datetime(df['Arrival_Time'].apply(lambda x: x.split()[0]))
            df['Arrival_Time_Hr'] = df['Arrival_Time_'].dt.hour
            df['Arrival_Time_Min'] = df['Arrival_Time_'].dt.minute
            df.drop(['Arrival_Time','Arrival_Time_'],axis=1,inplace=True)
            df['Duration'] = df['Duration'].apply(lambda x:x.replace('m','').replace('h',''))
            df['Duration'] = [(int(i[0])*60)+int(i[1]) if len(i)>1 else (int(i[0])*60) for i in df['Duration'].apply(lambda x:x.split()) ]
            df['Total_Stops'] = df['Total_Stops'].replace("non-stop","0")
            df['Total_Stops'] = df['Total_Stops'].apply(lambda x: x.split()[0])
            df['Total_Stops'] = df['Total_Stops'].astype(int)
            df.drop("Additional_Info",axis=1,inplace=True)
            logging.info("Completed the general data extraction and returning the dataset with extracted data")
            return df

        except Exception as e:
            raise FlightException(e,sys)

    @classmethod
    def get_transformer_pipeline(cls):
        try:
            ordinal_encod = make_column_transformer((OrdinalEncoder(), ['Airline',
                                                                        'day_name',
                                                                        'Source',
                                                                        'Destination',
                                                                        'Source_Route',
                                                                        'Route_1',
                                                                        'Route_2',
                                                                        'Route_3',
                                                                        'Route_4',
                                                                        'Route_5']),
                                                    remainder='passthrough'
                                                    )
            transformation_pipeline = Pipeline(
                steps={
                    ("ORDINAL_ENCODER",ordinal_encod)
                     })

        
            return transformation_pipeline


        except Exception as e:
            raise FlightException(e,sys)

    def inicate_data_transformation(self):
        try:
            logging.info("Starting the data transformation")
            logging.info("Lodding the data sets for the data transformation")
            train_df = pd.read_csv(self.data_validation_artifact.good_dataset_train_path)
            test_df = pd.read_csv(self.data_validation_artifact.good_dataset_test_path)
            train_df.dropna(inplace=True)
            train_df.drop_duplicates(inplace=True)
            test_df.dropna(inplace=True)
            test_df.drop_duplicates(inplace=True)
            logging.info("Deviding the datasets into the target and feature dataset")
            x_train = train_df.drop('Price',axis=1)
            y_train = train_df['Price']
            x_test = test_df.drop('Price',axis=1)
            y_test = test_df['Price']
            logging.info("Performing the general data extraction")
            x_train = DataTransformation.data_extraction_transformation(x_train)
            x_test = DataTransformation.data_extraction_transformation(x_test)
            logging.info("Loading the transformer to transform the dataset")
            transformer = DataTransformation.get_transformer_pipeline()
            logging.info("Fitting the transformer into the train dataset")
            transformer.fit(x_train)
            logging.info("Transforming the datasets with the transformer")
            x_train_arr = transformer.transform(x_train)
            x_test_arr = transformer.transform(x_test)
            logging.info("Converting the target feature into the array")
            y_train_arr = np.array(y_train)
            y_test_arr = np.array(y_test)
            logging.info("Saving the features and targets extracted from the datasets in the NPZ formates")
            utility.save_array(x_train_arr,self.data_transformation_config.x_train_df_transformed)
            utility.save_array(x_test_arr,self.data_transformation_config.x_test_df_transformed)
            utility.save_array(y_train_arr,self.data_transformation_config.y_train_df_transformed)
            utility.save_array(y_test_arr,self.data_transformation_config.y_test_df_transformed)
            logging.info("Saving the transformer for future use")
            utility.save_module(transformer,self.data_transformation_config.transformation_object)
            logging.info("Preparing the Artifact")
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transformer_object_path=self.data_transformation_config.transformation_object,
                x_train_df_transformed_path=self.data_transformation_config.x_train_df_transformed,
                x_test_df_transformed_path=self.data_transformation_config.x_test_df_transformed,
                y_train_df_transformed_path=self.data_transformation_config.y_train_df_transformed,
                y_test_df_transformed_path=self.data_transformation_config.y_test_df_transformed
            )
            logging.info("Completed the data transformationss")
            return data_transformation_artifact


        except Exception as e:
            raise FlightException(e,sys)