import pandas  as pd
import numpy   as np
import seaborn as sns
import pickle  as pkl
import os

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model    import  LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
import sklearn

print(sklearn.__version__)
model_dir = os.path.join(os.getcwd(), 'models')

if not os.path.exists(model_dir):
    os.mkdir(model_dir)

path = r'C:\Users\jeron\OneDrive\Desktop\lab10\Lab10\data\heart.csv'
data = pd.read_csv(path)

data.head()
data.isnull().sum()
print(data['cp'].max(), data['cp'].min())
X = data.iloc[:,:3].copy()
y = data.iloc[:,-1].copy()

features = ['age', 'sex','cp']
output = 'target'

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y)
##################logistic regression #######################################

lr = LogisticRegression()
params = {'C': [0.001, 0.01, 0.1, 1, 10, 100]}
cv_grid_lr = GridSearchCV(estimator= lr, param_grid=params, refit=True)
cv_grid_lr.fit(X_train, y_train)

cv_grid_lr.score(X_test, y_test)
pkl_file = os.path.join(model_dir,'logistic_pkl_model.pkl')

with open(pkl_file, 'wb') as file:
    pkl.dump(cv_grid_lr, file)

##############random forest#######################
rf = RandomForestClassifier()
params = {'n_estimators':[100, 200, 500], 'max_depth':[4,5,6]}
cv_grid = GridSearchCV(estimator=rf, param_grid=params, cv=5, refit=True)
cv_grid.fit(X_train,y_train)


cv_grid.score(X_test, y_test)

pkl_random = os.path.join(model_dir,'rf_pkl_model.pkl')

with open(pkl_random, 'wb') as file:
    pkl.dump(cv_grid, file)
#################SVC###################

svc = SVC()
params = {'C': [0.001, 0.01, 0.1, 1, 10],
          'gamma': [0.001, 0.01, 0.1, 1]}

cv_grid_svc = GridSearchCV(estimator=svc, param_grid=params, cv=5, refit=True)

cv_grid_svc.fit(X_train,  y_train)
cv_grid_svc.score(X_test, y_test)

pkl_svc = os.path.join(model_dir,'svc_pkl_model.pkl')

with open(pkl_svc, 'wb') as f:
    pkl.dump(cv_grid_svc, f)
