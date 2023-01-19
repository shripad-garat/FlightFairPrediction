import pandas as pd
import pymongo 
import json
import os 

mongo_url = "mongodb+srv://host:0pQPoWnWMSlypR0N@cluster0.alpnhdp.mongodb.net/?retryWrites=true&w=majority"
app_name = "FlightPrice_Predection"
collection = "FlightData"
mongo_clint = pymongo.MongoClient(mongo_url)

def dump_data():
    try:
        dump_data = pd.read_excel("Data_Train.xlsx")
        print(f" Rows and columns=: {dump_data.shape}")
        dump_data.reset_index(drop="True",inplace=True)
        json_records = list(json.loads(dump_data.T.to_json()).values())
        mongo_clint[app_name][collection].insert_many(json_records)
    except Exception as e:
        raise e

dump_data()