#This is Heroku Deployment Lectre
from flask import Flask, request, render_template
import os
import pickle

print(os.getcwd())
path = os.getcwd()

with open('models/logistic_pkl_model.pkl', 'rb') as f:
    logistic = pickle.load(f)

with open('models/rf_pkl_model.pkl', 'rb') as f:
    randomforest = pickle.load(f)

with open('models/svc_pkl_model.pkl', 'rb') as f:
    svm_model = pickle.load(f)


def get_predictions(age, sex, cp, req_model):
    mylist = [age, sex, cp]
    mylist = [float(i) for i in mylist]
    vals = [mylist]

    if req_model == 'Logistic':
        #print(req_model)
        return logistic.predict(vals)[0]

    elif req_model == 'RandomForest':
        #print(req_model)
        return randomforest.predict(vals)[0]

    elif req_model == 'SVM':
        #print(req_model)
        return svm_model.predict(vals)[0]
    else:
        return "Cannot Predict"


app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/', methods=['POST', 'GET'])
def my_form_post():
    if request.method == 'POST':
        age =       request.form['age']
        sex =       request.form['sex']
        cp  =       request.form['cp']
        req_model = request.form['req_model']

        target = get_predictions(age, sex, cp,req_model)

        if target==1:
            sale_making = 'Patient has heart problems'
        else:
            sale_making = 'Patient has no heart problems'

        return render_template('home.html', target = target, sale_making = sale_making)
    else:
        return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
