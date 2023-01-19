from FlightApp.exception import FlightException
from FlightApp.logger import logging
from FlightApp.ModelResolver import ModelResolver
from FlightApp.entity import config_entity,artifact_entity
from FlightApp import utility
import os,sys


class ModelPusher:
    def __init__(self,model_pusher_config:config_entity.ModelPusherConfig,model_evaluation_artifact:artifact_entity.ModelEvaluationArtifact):
        try:
            self.model_pusher_config = model_pusher_config
            self.model_evaluation_artifact = model_evaluation_artifact

        except Exception as e:
            raise FlightException(e,sys)

    
    def inicated_model_pusher(self):
        try:
            logging.info("Starting the model pusher")
            logging.info("Loading the transformer nad model objects")
            transformer = utility.load_module(self.model_evaluation_artifact.transformer_path)
            model = utility.load_module(self.model_evaluation_artifact.model_path)
            logging.info("Saving the model into the artifact directory")
            utility.save_module(module=model,path=self.model_pusher_config.model_path)
            utility.save_module(module=transformer,path=self.model_pusher_config.transformer_path)
            logging.info("Lodding the latest directory paths")
            transformer_path = ModelResolver().get_latest_saved_transformation_dir()
            model_path = ModelResolver().get_latest_save_model_dir()
            logging.info("Saving the model and transformer object into latest directory")
            utility.save_module(module=model,path=model_path)
            utility.save_module(module=transformer,path=transformer_path)
            logging.info("Preparing the artifact")
            model_pusher_artifact = artifact_entity.ModelPusherArtifact(pusher_dir=self.model_pusher_config.model_pusher,saved_model_dir=ModelResolver().get_latest_dir())
            logging.info("Complecting the model pusher")
            return model_pusher_artifact

        except Exception as e:
            raise FlightException(e,sys)