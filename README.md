# FlightFairPrediction
2.Architecture
                                                      																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																								
3.Architecture Description
3.1. Base Data-set 

	The base data-set is data-set we used for to determine the validation rules and also to train the base model of our project. The features in this data set will going to be same entire time with same rules and format.

3.2.Retraining Data-set

	In future if the model don’t do well we can retrain the model using this retraining data-set which we collect from the application.

3.3.Data Base

	The Data Base we are using in the project is MongoDB. Here the Training and base data set are stored.

3.4.Data Ingestion
	
	In Data Ingestion component it is used for the extracting the data from database and stored it in the artifact for the further use. Here we are going to extract, split and store data set in artifact with training and testing data set format.

3.5.Data Validation 

	In data validation component it is used for validating the data which we have extracted from the data base with our base dataset and the data description we receive from the  data base. If the validation pass then data will push to store in the good data artifact else it will pushed to bad data artifact. 

3.6.Data Transformation 

	In data transformation component it is used to transform the data set in to trainable dataset as we data come from the data base will going to be not in trainable format. Here we will do some EDA and feature engineering on the dataset and transfer it to required dataset format to train our model. Once the dataset get transfer the dataset will get save along with transformer object in the data transformation artifact.

3.7.Model Training 

	In Model training component it is used to train the model on the transferred dataset and it will give the score of the model on both train and test dataset. It will check on the overfiting and expected score. Once the check passes the model will get save into model training artifact.

3.8.Model evaluation

	In model evaluation component it is used to evaluate the train model with current present model and if the model do well on testing dataset than previous one then the train model will push to the model pusher component. 

3.9.Model Pusher 
		
	In model pusher component it is used to push the train model in to the saved model artifact for further used to predict the fair of the flight.

3.10.API 
	
	In the API, we are going to build the API for the entire project and then we will extracted the dataset from the user and then we will perform the prediction component to predict the fair of the flight.



