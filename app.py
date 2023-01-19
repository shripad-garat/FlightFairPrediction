from flask import Flask,request, render_template,jsonify
from FlightApp.pipeline import traning_pipeline,prediction_pipeline
from FlightApp.logger import logging
from FlightApp.exception import FlightException
import os,sys
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    try: 
        return render_template("home.html")

    except Exception as e:
        raise FlightException(e,sys)


@app.route('/admin/traning',methods = ['POST'])
def train_model():
    try:
        if request.method == 'POST':
            status = request.json['Status']
            if status == True:
                traning_pipeline.start_traning_pipeline()

    except Exception as e:
        raise FlightException(e,sys)

@app.route("/prediction",methods=['POST'])
def prediction():
    try:
        if request.method == 'POST':
            data = request.json['data']
            data = pd.read_json(data)
            output = prediction_pipeline.prediction(data=data)
            return jsonify({'Flight Fare for your journey will be ':output})   

    except Exception as e:
        raise FlightException(e,sys)


app.run()

