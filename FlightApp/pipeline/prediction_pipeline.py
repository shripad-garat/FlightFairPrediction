from FlightApp.ModelResolver import ModelResolver
from FlightApp.logger import logging
from FlightApp.exception import FlightException
from FlightApp import utility
from FlightApp.component.data_transformation import DataTransformation
import os,sys
import pandas as pd

based_data_path = os.path.join(os.getcwd(),"base_data","Data_Train.xlsx")
base_data = pd.read_excel(based_data_path)
base_column = base_data.columns
def prediction(data):
    try:
        data = pd.DataFrame(data=data,columns=base_column)
        base_transform_data = DataTransformation.data_extraction_transformation(data)
        transformer_path = ModelResolver.get_latest_transformer_dir()
        model_path = ModelResolver.get_latest_model_dir()
        model = utility.load_module(model_path)
        transformer = utility.load_module(transformer_path)
        transform_data = transformer.transform(base_transform_data)
        prediction_output = model.predict(transform_data)

        return prediction_output

    except Exception as e:
        raise FlightException(e,sys)