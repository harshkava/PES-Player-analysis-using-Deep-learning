# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 20:45:41 2018

@author: Harsh Kava
"""

import pandas as pd
from keras.models import *
from keras.layers import *
from sklearn.preprocessing import MinMaxScaler


#importing Data
train_data = pd.read_csv('Train_data.csv')
test_data = pd.read_csv('Test_data.csv')


#selecting columns for model
subset = ['Overall Rating','Height', 'Weight','Age']

train_data = train_data[subset]
test_data = test_data[subset]


##preprocessing the data
scaler = MinMaxScaler(feature_range=(0,1))

scaled_training = scaler.fit_transform(train_data)
scaled_testing = scaler.transform(test_data)

print("Note: overall rating values were scaled by multiplying by {:.10f} and adding {:.6f}".format(scaler.scale_[3], scaler.min_[3]))
#print(scaler.inverse_transform(scaled_training))

# Create new pandas DataFrame objects from the scaled data which is a numpy array
scaled_training_df = pd.DataFrame(scaled_training, columns=train_data.columns.values)
scaled_testing_df = pd.DataFrame(scaled_testing, columns=test_data.columns.values)


X = scaled_training_df.drop('Overall Rating', axis =1).values
Y = scaled_training_df['Overall Rating'].values


#building the model
model = Sequential()
model.add(Dense(30, input_dim = 3,activation= 'relu'))
model.add(Dense(150, activation= 'relu'))
model.add(Dense(50, activation= 'relu'))
model.add(Dense(1, activation= 'linear'))
model.compile(loss = 'mse', optimizer='adam')


#training the model
model.fit(
        X,
        Y,
        epochs=50,
        shuffle=True,
        verbose=2)

#Evaluating the model against Test Data
X_test = scaled_testing_df.drop('Overall Rating', axis =1).values
Y_test = scaled_testing_df['Overall Rating'].values

test_error_rate= model.evaluate(X_test,Y_test, verbose =2)
print(test_error_rate*100, ' Percent')
 

#Prediction of Data against new Values
pred_X= pd.read_csv('evaluate_data_expected.csv')
pred_X = pred_X[['Height', 'Weight','Age']]

pred_X 
 
#converting prediction into actual values  
prediction = model.predict(pred_X)
prediction = prediction -0.500000
prediction = prediction / 0.0333333333


print(prediction)
