import os,sys
from datetime import datetime
from FlightApp import config
from FlightApp.exception import FlightException
FILE_NAME = "Data.csv"
TRAIN_FILE_NAME = "Train.csv"
TEST_FILE_NAME = "Test.csv"
TRANSFORMATION_FILE_NAME = "transformer.pkl"
MODEL_FILE_NAME  = "model.pkl"

class traning_pipeline_config:
    
    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%d%m%y_%H%M%S')}")


        except Exception as e:
            raise FlightException(e,sys)



class DataIngestionConfig:

    def __init__(self,traning_pipeline_config:traning_pipeline_config):
        try:
            self.Database = config.env_var.database
            self.Collection = config.env_var.collection
            self.data_ingestion_dir = os.path.join(traning_pipeline_config.artifact_dir,"data_ingestion")
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir,"featurestore",FILE_NAME)
            self.train_file_path = os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)
            self.test_size = 0.3

        except Exception as e:
            raise FlightException(e,sys)




class DataValidationnConfig:

    def __init__(self,traning_pipeline_config:traning_pipeline_config):
        try:
            self.data_validation_dir = os.path.join(traning_pipeline_config.artifact_dir,"data_validation")
            self.based_data_path = os.path.join(os.getcwd(),"base_data","Data_Train.xlsx")
            self.report_path = os.path.join(self.data_validation_dir,'report','report.yaml')
            self.good_train_path = os.path.join(self.data_validation_dir,"good_dataset",TRAIN_FILE_NAME)
            self.good_test_path = os.path.join(self.data_validation_dir,"good_dataset",TEST_FILE_NAME)
            self.bad_train_path = os.path.join(self.data_validation_dir,"bad_dataset",TRAIN_FILE_NAME)
            self.bad_test_path = os.path.join(self.data_validation_dir,"bad_dataset",TEST_FILE_NAME)
            self.missing_threshold = 0.2
        
        except Exception as e:
            raise FlightException(e,sys)


class DataTransformationhConfig:

    def __init__(self,traning_pipeline_config:traning_pipeline_config):
        try:
            self.data_transformation_dir = os.path.join(traning_pipeline_config.artifact_dir,"data_transformation")
            self.transformation_object = os.path.join(self.data_transformation_dir,"transformation_object",TRANSFORMATION_FILE_NAME)
            self.x_train_df_transformed = os.path.join(self.data_transformation_dir,"transformed_data",TRAIN_FILE_NAME.replace('csv','npz'))
            self.x_test_df_transformed = os.path.join(self.data_transformation_dir,"transformed_data",TEST_FILE_NAME.replace('csv','npz'))
            self.y_train_df_transformed = os.path.join(self.data_transformation_dir,"transformed_data","y_train.npz")
            self.y_test_df_transformed = os.path.join(self.data_transformation_dir,"transformed_data","y_test.npz")
            
        except Exception as e:
            raise FlightException(e,sys)


class ModelTraningConfig:

    def __init__(self,traning_pipeline_config:traning_pipeline_config):
        try:
            self.model_traning_dir = os.path.join(traning_pipeline_config.artifact_dir,"model_traning")
            self.saved_model_path = os.path.join(self.model_traning_dir,MODEL_FILE_NAME)
            self.overfiting_threshold = 0.1
            self.expected_score = 0.8

        except Exception as e:
            raise FlightException(e,sys)


class ModelEvaluationConfig:

    def __init__(self,traning_pipeline_config:traning_pipeline_config):
        try:
            self.change_threshold = 0.01

        except Exception as e:
            raise FlightException(e,sys)


class ModelPusherConfig:

    def __init__(self,traning_pipeline_config:traning_pipeline_config):
        try:
            self.model_pusher = os.path.join(traning_pipeline_config.artifact_dir,"model_pusher")
            self.saved_model = os.path.join("Saved_Model")
            self.model_path = os.path.join(self.model_pusher,MODEL_FILE_NAME)
            self.transformer_path = os.path.join(self.model_pusher,TRANSFORMATION_FILE_NAME)
            
        except Exception as e:
            raise FlightException(e,sys)