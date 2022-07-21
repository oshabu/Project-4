from flask import Flask, render_template, request
import pandas as pd
from sklearn.linear_model import LinearRegression
import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pickle


app = Flask(__name__)
app = Flask(__name__, static_folder="templates")

filename = 'finalized_model.sav'
filename_le = 'label_encoder.sav'
filename_minmax ='min_max_scalar.sav'

def calculate_bmi(Height,Weight,Age,Gender,family_history_with_overweight,FAVC,CAEC,SMOKE,
         SCC,CALC,MTRANS,Height,Weight,Age):
    
    column_names = ['Gender','family_history_with_overweight','FAVC','CAEC','SMOKE','SCC','CALC','MTRANS','Height','Weight','Age']
    dict_all_loaded = pickle.load(file)
    file.close()

    df = pd.DataFrame(columns=column_names)
    df.loc[0] = [Gender,family_history_with_overweight,FAVC,CAEC,SMOKE,SCC,CALC,MTRANS]

    for col in df.columns:
        df.replace(dict_all_loaded[col], inplace=True)

    
    MinMaxScalerFile = pickle.load(open(filename_minmax, 'rb'))
    height_weight = MinMaxScalerFile.transform([[Height,Weight,Age]]) 
    Height = height_weight[0][0]
    Weight = height_weight[0][1]
    Age = height_weight[0][2]

    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.predict([[Gender,family_history_with_overweight,FAVC,CAEC,SMOKE,SCC,CALC,MTRANS,Height,Weight,Age]])

    return result[0]


@app.route("/",methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        gender = request.form['gender']
        height = request.form['height']
        weight = request.form['weight']
        
        bmi = calculate_bmi(gender,height,weight)

        return render_template('home.html',  result = bmi)
    
    else:
        return render_template('home.html')
    
 
if __name__ == '__main__':
   app.run(debug = True)


