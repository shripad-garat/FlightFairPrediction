from FlightApp.exception import FlightException
from FlightApp.logger import logging
from FlightApp.entity import artifact_entity,config_entity
from FlightApp import utility
import os,sys
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score



class ModelTraning:

    def __init__(self,data_transformation_artifact:artifact_entity.DataTransformationArtifact,model_traning_config:config_entity.ModelTraningConfig):
        try:
            self.model_traning_config = model_traning_config
            self.data_transformation_artifact = data_transformation_artifact


        except Exception as e:
            raise FlightException(e,sys)

    def model_selection(self,x,y):
        try:
            
            model = RandomForestRegressor()
            
            model.fit(x,y)

            return model

        except Exception as e:
            raise FlightException(e,sys)



    def initated_model_traning(self):
        try:
            logging.info(f"Starting the model training")
            logging.info(F"Loading the features and target array to train the model")
            x_train = utility.load_array(self.data_transformation_artifact.x_train_df_transformed_path)
            x_test = utility.load_array(self.data_transformation_artifact.x_test_df_transformed_path)
            y_train = utility.load_array(self.data_transformation_artifact.y_train_df_transformed_path)
            y_test = utility.load_array(self.data_transformation_artifact.y_test_df_transformed_path)
            logging.info(f"Traning and loading the model with train features and target label")
            model = self.model_selection(x_train,y_train)
            logging.info(f"Evaulating the model on test dataset")
            y_pred = model.predict(x_train)
            train_score = r2_score(y_true=y_train,y_pred=y_pred)
            logging.info(f"Traning score for model: {train_score}")
            y_pred = model.predict(x_test)
            test_score = r2_score(y_true=y_test,y_pred=y_pred)
            logging.info(f"Test score for model: {test_score}")
            logging.info(f"Checking if the model performing well than expected score({self.model_traning_config.expected_score})")
            if test_score<self.model_traning_config.expected_score:
                raise Exception(f"The model test score({test_score}) is less than expeced score({self.model_traning_config.expected_score})")
            logging.info(f"Getting the deffrence between the train and test score")            
            deffrence = train_score - test_score
            logging.info(f"Checking if the model is overfitting or not")
            if deffrence>self.model_traning_config.overfiting_threshold:
                raise Exception(f"The model is overfitting and having the defrence of {deffrence}")
            logging.info("Saving the model")
            utility.save_module(model,self.model_traning_config.saved_model_path)
            logging.info("Preparing he artifact")
            model_traning_artifact = artifact_entity.ModelTraningArtifact(train_model_path=self.model_traning_config.saved_model_path)
            logging.info("Completing the model traning")
            return model_traning_artifact

        except Exception as e:
            raise FlightException(e,sys)