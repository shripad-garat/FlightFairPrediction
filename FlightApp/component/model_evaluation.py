from FlightApp.exception import FlightException
from FlightApp.logger import logging
from FlightApp.ModelResolver import ModelResolver
from FlightApp.component.data_transformation import DataTransformation
from FlightApp.entity import artifact_entity,config_entity
from FlightApp import utility
from sklearn.metrics import r2_score
import os,sys
import pandas as pd


class ModelEvaluation:

    def __init__(self,data_validation_artifact:artifact_entity.DataValidationArtifact,data_transformation_artifact:artifact_entity.DataTransformationArtifact,model_tranining_artifact:artifact_entity.ModelTraningArtifact,model_evaluation_config:config_entity.ModelEvaluationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.model_traning_artifact = model_tranining_artifact
            self.model_evaluation_config = model_evaluation_config
            self.model_resolver = ModelResolver()

        except Exception as e:
            raise FlightException(e,sys)


    def inicated_model_evaluation(self):
        try:
            logging.info("Initalinzing the model evaluation")
            logging.info("Getting the latest model directory")
            latest_dir = self.model_resolver.get_latest_dir()
            logging.info("checking if model exist or not in the current directory")
            if latest_dir== None:
                return artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,impruve_accuracy=None,model_path=self.model_traning_artifact.train_model_path,transformer_path=self.data_transformation_artifact.transformer_object_path)
            logging.info("Geting the latest model and transformer object path")
            saved_transformer_path = self.model_resolver.get_latest_transformer_dir()
            saved_model_path = self.model_resolver.get_latest_model_dir()
            logging.info("Loading the latest model and transformer object")
            saved_transformer = utility.load_module(saved_transformer_path)
            saved_model = utility.load_module(saved_model_path)
            logging.info("Loading the current model and transformer object")
            current_transformer = utility.load_module(self.data_transformation_artifact.transformer_object_path)
            current_model = utility.load_module(self.model_traning_artifact.train_model_path)
            logging.info("LOading the test data")
            test_df = pd.read_csv(self.data_validation_artifact.good_dataset_test_path)
            x_test = test_df.drop("Price",axis=1)
            y_test = test_df['Price']
            logging.info("Making the general transformation in the data set")
            x_test = DataTransformation.data_extraction_transformation(x_test)
            logging.info("Transforming the dataset using the transformer objects")
            saved_x_test = saved_transformer.transform(x_test)
            current_x_test = current_transformer.transform(x_test)
            logging.info("Making the predection using model objects")
            saved_model_predect = saved_model.predict(saved_x_test)
            current_model_predect = current_model.predict(current_x_test)
            logging.info("Getting the R2 score of the models")
            saved_model_score = r2_score(y_true=y_test,y_pred=saved_model_predect)
            current_model_score = r2_score(y_true=y_test,y_pred=current_model_predect)
            logging.info("Comparing the scores of the models")
            if current_model_score<saved_model_score:
                logging.info("Current model dosent performing well than previous model")
                logging.info("Preparing the artifact")
                model_evaluation_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=False,impruve_accuracy=current_model_score,model_path=self.model_traning_artifact.train_model_path,transformer_path=self.data_transformation_artifact.transformer_object_path)
            else:
                logging.info("Preparing the artifact")
                model_evaluation_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,impruve_accuracy=current_model_score,model_path=self.model_traning_artifact.train_model_path,transformer_path=self.data_transformation_artifact.transformer_object_path)
            logging.info("completing the model evaluation")
            return model_evaluation_artifact



        except Exception as e:
            raise FlightException(e,sys)