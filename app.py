from flask import Flask,request, render_template,jsonify
from FlightApp.pipeline import traning_pipeline,prediction_pipeline
from FlightApp.logger import logging
from FlightApp.exception import FlightException
import sys
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    try: 
        return render_template("home.html") 

    except Exception as e:
        raise FlightException(e,sys)


@app.route('/traning')
def train_model():
    try:
        
        traning_pipeline.start_traning_pipeline()
        return render_template("home.html")

    except Exception as e:
        raise FlightException(e,sys)

@app.route("/prediction",methods=['GET','POST'])
def prediction():
    try:
        if request.method == 'POST':
            input = {}
            input["Airline"] = request.form["Airline"]
            input["Date_of_Journey"] = request.form["Date_of_Journey"]
            input["Source"] = request.form["Source"]
            input["Destination"] = request.form["Destination"]
            input["Route"] = request.form["Route"]
            input["Dep_Time"] = request.form["Dep_Time"]
            input["Arrival_Time"] = request.form["Arrival_Time"]
            input["Duration"] = request.form["Duration"]
            input["Total_Stops"] = request.form["Total_Stops"]
            input["Additional_Info"] = request.form["Additional_Info"]
            


            output = prediction_pipeline.prediction(data=input)
            return render_template("home.html",output = output)

    except Exception as e:
        raise FlightException(e,sys)


if __name__ == "__main__":
    app.run(debug=True)
