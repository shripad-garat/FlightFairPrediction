import pymongo
import os 
from dataclasses import dataclass
from dotenv import load_dotenv
print("Loding the env enviroment and reading .env file")
load_dotenv()

@dataclass
class EnvironmentVariable:
    mongo_db_url:str = os.getenv("MONGO_DB_URL")
    database = os.getenv("DATABASE")
    collection = os.getenv('COLLECTION')

env_var = EnvironmentVariable()
print(env_var.mongo_db_url)
mongo_clint = pymongo.MongoClient(env_var.mongo_db_url)
