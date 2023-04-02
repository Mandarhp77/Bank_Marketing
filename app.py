from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import pandas as pd
import sklearn
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

file = 'Bank_model.pkl'
fileobj = open(file, "rb")
model = pickle.load(fileobj)

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

#standard_to = MinMaxScaler()
@app.route("/predict", methods=['POST'])
def predict():
    #Fuel_Type_Diesel=0
    if request.method == 'POST':
        
        Age = int(request.form['age'])


        Education=request.form['education']
        if(Education=='professional_course'):
            Education=10
        elif(Education=='university_degree'):
            Education=9
        elif(Education=='tertiary'):
            Education=8
        elif(Education=='secondary'):
            Education=7
        elif(Education=='high_school'):
            Education=6
        elif(Education=='basic_9y'):
            Education=5
        elif(Education=='basic_6y'):
            Education=4
        elif(Education=='primary'):
            Education=3
        elif(Education=='basic_4y'):
            Education=2
        elif(Education=='illiterate'):
            Education=1


        Duration=int(request.form['duration'])


        Campaign=int(request.form['campaign'])


        Jobs=request.form['job_Type']
        if(Jobs=='entrepreneur'):
            Jobs=11
        elif(Jobs=='self-employed'):
            Jobs=10
        elif(Jobs=='admin'):
            Jobs=9
        elif(Jobs=='management'):
            Jobs=8
        elif(Jobs=='services'):
            Jobs=7
        elif(Jobs=='technician'):
            Jobs=6
        elif(Jobs=='blue-collar'):
            Jobs=5
        elif(Jobs=='housemaid'):
            Jobs=4
        elif(Jobs=='retired'):
            Jobs=3
        elif(Jobs=='student'):
            Jobs=2
        elif(Jobs=='unemployed'):
            Jobs=1

        
        Maritals=request.form['marital_status']
        if(Maritals=='married'):
            Maritals=3
        elif(Maritals=='single'):
            Maritals=2
        elif(Maritals=='divorced'):
            Maritals=1
       

        default_yes=request.form['default']
        if(default_yes=='yes'):
            default_yes=1
        else:
            default_yes=0	


        housing_yes=request.form['housing']
        if(housing_yes=='yes'):
            housing_yes=1
        else:
            housing_yes=0

        
        loan_yes=request.form['loan']
        if(loan_yes=='yes'):
            loan_yes=1
        else:
            loan_yes=0


        contact_telephone = request.form['contact']
        if(contact_telephone =='telephone'):
            contact_telephone = 1
        else:
            contact_telephone = 0


        poutcome = request.form['poutcome']
        if(poutcome =='other'):
            poutcome_other = 1
        elif(poutcome =="success"):
            poutcome_success = 1
        else:
            poutcome_other, poutcome_success = 0,0


        quarter = request.form['month']
        if(quarter =='apr' or 'may' or 'jun'):
            quarter_q2 = 1
            quarter_q3 = 0
            quarter_q4 = 0
        elif(quarter =='jul' or 'aug' or 'sep'):
            quarter_q3 = 1
            quarter_q2 = 0
            quarter_q4 = 0
        elif(quarter =='oct' or 'nov' or 'dec'):
            quarter_q4 = 1
            quarter_q3 = 0
            quarter_q2 = 0
        else:
            quarter_q2, quarter_q3, quarter_q4 = 0,0,0

        
        scaler = MinMaxScaler()

        x = [[Age, Education, Duration, Campaign, Jobs, Maritals, default_yes, housing_yes, loan_yes, 
                                   contact_telephone, poutcome_other, poutcome_success, quarter_q2, quarter_q3, quarter_q4]]

        data = pd.DataFrame(scaler.fit_transform(x))

   
        prediction=model.predict(data)
        output=round(prediction[0],2)
        if output == 0:
            return render_template('prediction.html',prediction_text="Customer is not interested to buy long term deposit")
        elif output == 1:
            return render_template('prediction.html',prediction_text="Customer is interested to buy long term deposit")
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

