import os
import pandas  as pd
import seaborn as sns
import numpy   as np

import matplotlib.pyplot as plt

from scipy.stats           import  linregress, spearmanr
from sklearn.cluster       import  KMeans
from sklearn.preprocessing import  StandardScaler
from sklearn.preprocessing import LabelEncoder

fig_path = os.path.join(os.getcwd(), 'visuals')
df = pd.read_csv(r'data\filtered_merged_data_2019.csv')
data =  df.copy()

#drops unnecessary data , all variables in part of policing operation are False.
data.drop(['Unnamed: 0', 'Date', 'Part of policing operation', 'Policing operation',
           'Latitude', 'Longitude','postcode'], axis=1, inplace=True)

#renames columns for ease of use
data.rename(columns={'Modelled_Household_median_income_estimates_2012/13': 'median income',
                     'Unemployment_rate_(2015)': 'unemployment rate'}, inplace=True)


#groups by borough
groups = data.groupby('Borough')

#creates a list of lists containing borough, median income, unemployment rate, n of arrests and total stops.
grouped = [[brgh, len(ds),
        ds['median income'].unique()[0],
        len(ds[ds['Outcome'] == 'Arrest']),
        ds['unemployment rate'].unique()[0]]
        for brgh, ds in groups]


new_df = pd.DataFrame(grouped, columns=['borough','stops','median income',
                                        'arrests','unemployment'])

##########visualize linear relationships########################
def line_int(df , var1 , var2):
    line = linregress(df[var1], df[var2])
    plt.plot(df[var1], df[var2], 'o', label='data')
    plt.plot(df[var1], line.intercept + line.slope*df[var1],
                                            'r', label='fitted line')

    title = f'correlation between {var1} and {var2}'
    plt.xlabel(var1)
    plt.ylabel(var2)
    plt.title(title)
    plt.savefig(os.path.join(fig_path, title))
    plt.show()
    return line.pvalue

for x in ['stops','median income', 'unemployment']:
    line_int(new_df,'arrests', x )


#################k means clusterign to find groups among unemployment and median household income###############
data_k = data.iloc[:,-2:].copy()

standard = StandardScaler()
transform = data_k.copy()
data_standard = standard.fit_transform(transform)

#elbow chart to find number of clusters
def elbowing():
    wcss = []
    for i in range(1,11):
        kmean = KMeans(n_clusters=i)
        kmean.fit(data_standard)
        wcss.append(kmean.inertia_)

    plt.plot(range(1,11), wcss, marker='o', linestyle='-')
    plt.show()

#n clusters = (3 or 4 unpreceise elbow chart)
kmean = KMeans(n_clusters=3)
kmean.fit(data_standard)
#create vbariable called labels
data_k['labels']=kmean.labels_
data_k.dropna(inplace=True)

sns.scatterplot(x=data_k['median income'],
                y=data_k['unemployment rate'],
                hue=data_k['labels'])
plt.title('K neighbours clustered SES')

plt.savefig(os.path.join(fig_path,'scatter_test_kmeans'))
print(data_k)
data['SES groups'] = kmean.labels_


le = LabelEncoder()
data['Outcome'] = le.fit_transform(data['Outcome'])
data['Outcome'].value_counts()
data.dropna(inplace=True)
print(data.isnull().sum())
data.nunique().plot.bar()
print(data['Part of a policing operation'].unique())
#object of search frequency


def plot_object_search(data, type, save=False):
    '''
       --------------------------------------------------------
       Plot the frequency of reasons for search
       --------------------------------------------------------
       data = data to be plotted in the form data['var']
       type = title /type of data being plotted
       save = if True saves the figure in the folder visuals
       --------------------------------------------------------
       '''

    visual_data = data.copy()

    def replace_test(x):
        '''replaces the long worded
           objects for search for shorter ones to
           make it easier to read in graph'''

        replace = {'Evidence of offences under the Act': 'Offence Evidence',
                   'Articles for use in criminal damage': 'criminal damage evidence'}

        if x in replace.keys():
            x = replace[x]
        return x

    visual_data['Object of search'] = visual_data['Object of search'].apply(
        lambda x: replace_test(x))

    title = f'Frequency of {type}'
    perc = visual_data['Object of search'].value_counts() / len(data)
    fig = perc.sort_values(ascending=False).plot.bar(
        y='Object of search', rot=70, color='lightcoral')
    fig.set_title(title)
    fig.set_ylabel('Percentage of total stop and search occurences')
    if save:
        plt.savefig(os.path.join('visuals',title), bbox_inches='tight')
    print('-'*50)
    plt.show()
    print('-'*50)
    print(perc)
    print('-'*50)

test1 = data[data['Outcome'] == 0]
test2 = data[data['Outcome'] == 1]

plot_object_search(test1, 'dismissed cases', save=True)
plot_object_search(test2, 'Arrest cases', save=True)
