from FlightApp import config
from FlightApp.exception import FlightException
from FlightApp.logger import logging
import os,sys
import yaml
import pandas as pd
import dill
import numpy as np


mongo_clint = config.mongo_clint

def get_data_(app,collection)->pd.DataFrame:
    try:
        
        
        raw_data = list(mongo_clint[app][collection].find())
        
        df = pd.DataFrame(raw_data)
        
        if '_id' in df.columns:

            df.drop('_id',axis=1,inplace=True)

        return df

    except Exception as e:
        raise FlightException(e,sys)


def save_data_to_csv(data:pd.DataFrame,path):
    try:

        base_dir = os.path.dirname(path)
        os.makedirs(base_dir,exist_ok=True)

        data.to_csv(path,header=True,index=False)

    except Exception as e:
        raise FlightException(e,sys)

def write_yaml_report(data,path):
    try:

        base_dir = os.path.dirname(path)
        os.makedirs(base_dir,exist_ok=True)

        with open(path,'w') as file:
            
            yaml.dump(data,file)

    except Exception as e:
        raise FlightException(e,sys)


def save_module(module,path):
    try:
        
        base_dir = os.path.dirname(path)
        os.makedirs(base_dir,exist_ok=True)

        with open(path,'wb') as file:
            dill.dump(module,file)

    except Exception as e:
        raise FlightException(e,sys)


def load_module(path):
    try:
        
        if not os.path.exists(path):
            raise Exception(f"File not found : {path}")
        with open(path,'rb') as file:
            return dill.load(file)

    except Exception as e:
        raise FlightException(e,sys)


def save_array(array,path):
    try:
        
        base_dir = os.path.dirname(path)
        os.makedirs(base_dir,exist_ok=True)

        with open(path ,'wb') as file:
            np.save(file,array)
            
    except Exception as e:
        raise FlightException(e,sys)


def load_array(path):
    try:
        with open(path,'rb') as file:
            return np.load(file,allow_pickle=True)

    except Exception as e:
        raise FlightException(e,sys)


def change_to_float(df):
    try:
        for col in df.columns:
            df[col] = df[col].astype(float)
        return df
    except  Exception as e:
        raise FlightException(e,sys)