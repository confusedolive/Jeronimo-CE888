from sklearn.cluster       import  KMeans
from sklearn.preprocessing import  StandardScaler
from sklearn.preprocessing import LabelEncoder
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import dowhy

fig_path = os.path.join(os.getcwd(), 'visuals')
df = pd.read_csv(r'data\filtered_merged_data_2019.csv')
data =  df.copy()
data
#drops unnecessary data , all variables in part of policing operation are False.
data.drop(['Unnamed: 0', 'Date', 'Part of a policing operation', 'Policing operation',
           'Latitude', 'Longitude','postcode'], axis=1, inplace=True)

#renames columns for ease of use
data.rename(columns={'Modelled_Household_median_income_estimates_2012/13': 'median income',
                     'Unemployment_rate_(2015)': 'unemployment rate'}, inplace=True)

data.dropna(inplace=True)

data_k = data.iloc[:,-2:].copy()

standard = StandardScaler()
transform = data_k.copy()
data_standard = standard.fit_transform(transform)

#elbow chart to find number of clusters

def elbowing():
    wcss = []
    for i in range(1, 11):
        kmean = KMeans(n_clusters=i)
        kmean.fit(data_standard)
        wcss.append(kmean.inertia_)

    plt.plot(range(1, 11), wcss, marker='o', linestyle='-')
    plt.show()

elbowing()
# n clusters = (3 or 4 unpreceise elbow chart)
kmean = KMeans(n_clusters=3)
kmean.fit(data_standard)
# create vbariable called labels
data_k['labels'] = kmean.labels_
data_k.dropna(inplace=True)

sns.scatterplot(x=data_k['median income'],
                y=data_k['unemployment rate'],
                hue=data_k['labels'])
plt.title('K neighbours clustered SES')

plt.savefig(os.path.join(fig_path, 'scatter_test_kmeans'))
print(data_k)
data['SES groups'] = kmean.labels_
