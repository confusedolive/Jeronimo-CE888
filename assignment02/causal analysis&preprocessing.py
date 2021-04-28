import os

import dowhy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pygraphviz
import seaborn as sns
from IPython.display import Image, display
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler

#########################################################################################################################
#                                              Causal analysis                                                          #
#            Preprocessing the availabel data to be able to construct a dowhy causal model with                         #
#########################################################################################################################

fig_path = os.path.join(os.getcwd(), 'visuals')
df = pd.read_csv(r'data\filtered_merged_data_2019.csv')
data = df.copy()
borough_info = pd.read_csv(r'data\london-borough-profiles.csv')

# pick relevant information to obtain from borough dataset
crimeinfo = borough_info[['Area_name',
                          'Crime_rates_per_thousand_population_2014/15']]


def obtain_borough_info(borough_info, column, main_data):
    '''From general borough info dataset adds the columns of interest to dataset of interest'''
    for col in column:
        borough_info_dict = {
            borough: info for borough, info
            in zip(borough_info['Area_name'].values,
                   borough_info[col].values)
        }

        main_data[col] = [
            borough_info_dict[borough] for
            borough in main_data['Borough'].values
        ]


def pipeline_preprocessing():
    # add crime rates per thousand , replace nan values in the borough city of london
    obtain_borough_info(
        crimeinfo, ['Crime_rates_per_thousand_population_2014/15'], data)

    '''Converts variable to type float , first replaces . value with np.nan
    then calculates the mean  and replaces those nan values with the mean'''

    mask = data['Crime_rates_per_thousand_population_2014/15'] == '.'
    data[mask] = data[mask].replace(['.'], [np.nan])
    data['Crime_rates_per_thousand_population_2014/15'] = \
        data['Crime_rates_per_thousand_population_2014/15'].astype(float)
    mean_rates = data['Crime_rates_per_thousand_population_2014/15'].mean()
    data[mask] = data[mask].replace([np.nan], [mean_rates])
    # renames columns for ease of use

    data.rename(
        columns={'Modelled_Household_median_income_estimates_2012/13': 'median income',
                 'Unemployment_rate_(2015)': 'unemployment rate',
                 'Crime_rates_per_thousand_population_2014/15': 'Crime rates per thousand',
                 'Self-defined ethnicity': 'ethnicity'}, inplace=True)

    # Change variable type to float64 from object type
    '''Converts Date variable to timedelta type out
       of which the hours at which the stop and search happend
       are extracted into a new variable named Hour, utilizing cut
       hour is converted into a categorical variable containing 4 bins
       Early morning, morning, afternoon and night '''
    data['Date'] = pd.to_datetime(data['Date'])
    data['Hour'] = data['Date'].dt.hour
    data['Hour'] = pd.cut(
        data['Hour'], bins=4,
        labels=['Early monring', 'Morning', 'Afternoon', 'Night'])

    # drops unnecessary data , all variables in part of policing operation are False.
    data.drop(
        ['Unnamed: 0', 'Date', 'Part of a policing operation',
         'Policing operation', 'Latitude', 'Officer-defined ethnicity',
         'Longitude', 'postcode'], axis=1, inplace=True)

    # drop missing values
    # data.dropna(inplace=True)

    le = LabelEncoder()  # label encoder instance
    data['Outcome'] = le.fit_transform(
        data['Outcome'])  # transform outcome to 0,1

    print('''Preprocessing finished: Added Crime rates per thousand, Added hour of crime,
    Dropped unnecessary columns, dropped missing values and labelencoded outcome''')
    return le  # return labelencoder object to reverse transform if needed the encoded outcome


le = pipeline_preprocessing()


# elbow chart to find number of clusters
def elbowing():
    # plots elbow plot to find optimal neighbours for kmeans
    wcss = []
    for i in range(1, 11):
        kmean = KMeans(n_clusters=i)
        kmean.fit(data_standard)
        wcss.append(kmean.inertia_)

    plt.plot(range(1, 11), wcss, marker='o', linestyle='-')
    plt.show()


elbowing()
# n clusters = (3 or 4 unprecise elbow chart)

def create_clusters(clusters=2):
    '''Essentially divide the median income variable into
    two groups low-medium an high average income, as dowhy
    deals with boolean as treament'''
    # copy of the data used to create the cluesters
    # unemployment rate and median income
    data_k = data[['median income', 'unemployment rate']].copy()

    # standarize data
    standard = StandardScaler()
    transform = data_k['median income'].copy()
    data_standard = standard.fit_transform(transform.values.reshape(-1, 1))
    kmean = KMeans(n_clusters=clusters, random_state=42)
    kmean.fit(data_standard)
    # create vbariable called labels
    data_k['labels'] = kmean.labels_

    # plot and save the clusters created
    sns.scatterplot(x=data_k['median income'],
                    y=data_k['unemployment rate'],
                    hue=data_k['labels'], palette='Set1')
    plt.title('K neighbours clustered SES')
    plt.savefig(os.path.join(fig_path, 'scatter_test_kmeans'))
    plt.show()
    return kmean.labels_


def replace_values(val, back_val=False, old_vals=None):
    '''Encodes categorical variables by simply replacing the unique
    values by a number in the form of range(n-1) n being the amount
    of unique values in the variable, returns a list containing the original
    values, if back_val is set to True and old_vals is fed the list containing
    the original unique values it will de-encode the variable'''

    to_replace = [x for x in df1[val].unique()]
    if back_val:
        df1[val] = df1[val].replace(to_replace, old_vals)
        print(f'Variable {val} has been returned back the original values')
    else:
        new = [x for x in range(len(df1[val].unique()))]
        df1[val] = df1[val].replace(to_replace, new)
        print(f'Categorical variable {val} have been econded correctly')
        return to_replace


df1 = data.copy()  # dataset for causal analysis
# Encode all categorical variables
to_replace_var = [x for x in df1.columns if df1[x].dtype == object]
replaced_vals = []  # list of lists containing the original values
for x in to_replace_var:
    test = replace_values(x)
    replaced_vals.append(test)

# test de encoding works correctly
# for x, y in zip(to_replace_var, replaced_vals):
#     test = replace_values(x,back_val=True, old_vals=y)

# rename variables for pygraphviz to understand them
df1.rename(columns={'Age range': 'Age_range', 'Object of search': 'Object_of_search',
                    'median income': 'median_income', 'unemployment rate': 'unemployment_rate',
                    'Crime rates per thousand': 'Crime_rates_per_thousand',
                    'SES groups': 'income_groups'}, inplace=True)

#Drop redundant variables
df1.drop(columns=['median_income', 'Legislation',
         'Type', 'Borough'], inplace=True)

# replacing "treatment" variable to boolean values False if income is below average and True if it is above
df1['income_groups'] = df1['income_groups'].replace([0, 1], [False, True])
to_standard = df1['Crime_rates_per_thousand']

# defines causal graph to be given to the dowhy model object
causual_graph = '''digraph {
ethnicity[label="Ethnic origin"];
Age_range[label="Age range"];
Gender[label="Gender"];
Hour[label="Time of stop"];
Object_of_search[label="Reason for stop"];
Outcome[label="Outcome of Stop and search"];
unemployment_rate[label="Unemployment"];
Crime_rates_per_thousand[label="crime rate"];
income_groups[label="average income"];
U[label="Unobserved Confounders"];
U->income_groups; U->Outcome; U->Object_of_search;
ethnicity->Outcome;
Age_range->Outcome;
Hour->Outcome;
Crime_rates_per_thousand->Outcome;
unemployment_rate->Crime_rates_per_thousand; unemployment_rate->income_groups;
Object_of_search->Outcome;
income_groups->Outcome; income_groups->Crime_rates_per_thousand; income_groups->Object_of_search
}'''

#Create dowhy causal model , treatment is income groups , outcome is the Outcome of stop and search
model = dowhy.CausalModel(data=df1, graph=causual_graph.replace(
    "\n", " "), treatment="income_groups", outcome="Outcome")

model.view_model()#saves image of model as causal_model.png
display(Image(filename="causal_model.png"))# visualize graphical causation model

identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)#identify effect
print(identified_estimand)#print estiamnde

#estimate the effect of treatment in the outcome , effect = income average
estimate = model.estimate_effect(identified_estimand,
                                 method_name='backdoor1.propensity_score_matching',
                                 target_units='att', method_params={'max_iter': 1000})

help(model.estimate_effect)
print(estimate)

#refute utilizing placebo treatment , estimand should approximate 0 if correct
refutation = model.refute_estimate(identified_estimand, estimate, method_name="placebo_treatment_refuter",
                                   placebo_type="permute", num_simulations=10)
print(refutation)
