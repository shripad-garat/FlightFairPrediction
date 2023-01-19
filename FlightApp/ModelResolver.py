from FlightApp.exception import FlightException
from FlightApp.logger import logging
from FlightApp.entity import artifact_entity,config_entity
import os,sys

class ModelResolver:

    def __init__(self,model_registory="Saved_model",transformer_dir_name = "transformer",model_dir_name = "model"):
        try:
            self.model_registory = model_registory
            self.transformer_dir_name = transformer_dir_name
            self.model_dir_name = model_dir_name
            os.makedirs(self.model_registory,exist_ok=True)

        except Exception as e:
            raise FlightException(e,sys)


    def get_latest_dir(self):
        try:
            dir_name = os.listdir(self.model_registory)
            if len(dir_name)==0:
                return None
            dir_name = list(map(int,dir_name))
            latest_dir_name = max(dir_name)
            return os.path.join(self.model_registory,f"{latest_dir_name}")

        except Exception as e:
            raise FlightException(e,sys)

    
    def get_latest_model_dir(self):
        try:
            latest_dir_name = self.get_latest_dir()
            if latest_dir_name==None:
                raise Exception("Model not found in the given dir")
            return os.path.join(latest_dir_name,self.model_dir_name,config_entity.MODEL_FILE_NAME)
            
        except Exception as e:
            raise FlightException(e,sys)


    def get_latest_transformer_dir(self):
        try:
            latest_dir_name = self.get_latest_dir()
            if latest_dir_name==None:
                raise Exception(f"Transformer not found in the given dir")
            return os.path.join(latest_dir_name,self.transformer_dir_name,config_entity.TRANSFORMATION_FILE_NAME)

        except Exception as e:
            raise FlightException(e,sys)

    
    def get_latest_save_dir(self):
        try:
            latest_dir_name = self.get_latest_dir()
            if latest_dir_name==None:
                return os.path.join(self.model_registory,f"{0}")
            latest_dir_name = int(os.path.basename(latest_dir_name))
            return os.path.join(self.model_registory,f"{latest_dir_name+1}")

        except Exception as e:
            raise FlightException(e,sys)

    
    def get_latest_save_model_dir(self):
        try:
            latest_dir_name = self.get_latest_save_dir()
            return os.path.join(latest_dir_name,self.model_dir_name,config_entity.MODEL_FILE_NAME)

        except Exception as e:
            raise FlightException(e,sys)


    def get_latest_saved_transformation_dir(self):
        try:
            latest_dir_name = self.get_latest_save_dir()
            return os.path.join(latest_dir_name,self.transformer_dir_name,config_entity.TRANSFORMATION_FILE_NAME)

        except Exception as e:
            raise FlightException(e,sys)