from FlightApp.entity import config_entity
from FlightApp.component.data_ingestion import DataIngestion
from FlightApp.component.data_validation import DataValidation
from FlightApp.component.data_transformation import DataTransformation
from FlightApp.component.model_traning import ModelTraning
from FlightApp.component.model_evaluation import ModelEvaluation
from FlightApp.component.model_pusher import ModelPusher
from FlightApp.logger import logging
from FlightApp.exception import FlightException
import os,sys

def start_traning_pipeline():
    try:
        traning_pipeline_config = config_entity.traning_pipeline_config()
        data_ingestion_config = config_entity.DataIngestionConfig(traning_pipeline_config=traning_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initated_data_ingestion()
        data_validation_config = config_entity.DataValidationnConfig(traning_pipeline_config=traning_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact = data_validation.initated_data_validation()
        data_transformation_config = config_entity.DataTransformationhConfig(traning_pipeline_config=traning_pipeline_config)
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config,data_validation_artifact=data_validation_artifact)
        data_transformation_artifact = data_transformation.inicate_data_transformation()
        model_traning_config = config_entity.ModelTraningConfig(traning_pipeline_config=traning_pipeline_config)
        model_traning = ModelTraning(data_transformation_artifact=data_transformation_artifact,model_traning_config=model_traning_config)
        model_traning_artifact = model_traning.initated_model_traning()
        model_evaluation_config = config_entity.ModelEvaluationConfig(traning_pipeline_config=traning_pipeline_config)
        model_evaluation = ModelEvaluation(data_validation_artifact=data_validation_artifact,data_transformation_artifact=data_transformation_artifact,model_evaluation_config=model_evaluation_config,model_tranining_artifact=model_traning_artifact)
        model_evaluation_artifact = model_evaluation.inicated_model_evaluation()
        model_pusher_config = config_entity.ModelPusherConfig(traning_pipeline_config=traning_pipeline_config)
        model_pusher = ModelPusher(model_pusher_config=model_pusher_config,model_evaluation_artifact=model_evaluation_artifact)
        model_pusher_artifact = model_pusher.inicated_model_pusher()
        print(model_pusher_artifact)
        

    except Exception as e:
        raise FlightException(e,sys)