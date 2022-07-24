import joblib
import numpy as np
from flask import Flask, render_template, request
from sklearn.linear_model import LinearRegression
import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pickle

from sklearn.preprocessing import LabelEncoder



app = Flask(__name__, static_folder="templates")

filename = 'finalized_model.sav'
le = LabelEncoder()
#data = pd.read_csv('ObesityDataSet_raw_and_data_sinthetic.csv')#读取数据
#data['NObeyesdad'] = le.fit_transform(data['NObeyesdad'])
filename1 = 'min_max_scalar.sav'
filename2 = 'label_encoder.sav'
scaler = preprocessing.MinMaxScaler()
@app.route("/",methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        height = request.form.get('height')
        weight = request.form.get('weight')
        age = request.form.get('age')
        gender = request.form.get('gender')
        selCity= request.form.get('selCity')
        calorie = request.form.get('eat')
        meals = request.form.get('meals')
        smoke = request.form.get('smoke')
        calories = request.form.get('calories')
        alcohol = request.form.get('alcohol')
        transport = request.form.get('transport')
        MinMaxScalerFile = pickle.load(open(filename1, 'rb'))
        test = MinMaxScalerFile.transform([[height, weight, age]])
        list_2 = [float(x) for item in test for x in item]
        height = list_2[0]
        weight = list_2[1]
        age = list_2[2]
        row = [gender,age,height,weight,selCity, calorie, meals, smoke, calories, alcohol, transport]
        ls = np.array(row, dtype=np.float64)
        load_model = pickle.load(open(filename, 'rb'))
        load_model1 = pickle.load(open(filename2,'rb'))
        result = load_model.predict([ls])
        bmi1 = load_model1.inverse_transform([result][0])
        #bmi1 = le.inverse_transform([(result[0].astype(int))])
        bmi =''.join(str(i) for i in bmi1)

        if((result[0].astype(int)) ==0):
            detail = 'Insufficient_Weight'
        if((result[0].astype(int)) ==1):
            detail = 'Normal_Weight'
        if ((result[0].astype(int)) == 2):
            detail = 'Obesity_Type_I'
        if ((result[0].astype(int)) == 3):
            detail = 'Obesity_Type_II'
        if ((result[0].astype(int)) == 4):
            detail = 'Obesity_Type_III'
        if ((result[0].astype(int)) == 5):
            detail = 'Overweight_Level_I'
        if ((result[0].astype(int)) == 6):
            detail = 'Overweight_Level_II'



        return render_template('home.html',  health = bmi,detail = detail)

    
    else:
        return render_template('home.html')
    
 
if __name__ == '__main__':
   app.run(debug = True)


