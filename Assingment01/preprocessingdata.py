import pandas as pd
import numpy as np
import seaborn as sns
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import re
from preprocessing import join_datasets,add_borough_df

def converter(x):
        pattern = r','
        converted = re.sub(pattern, '', x)
        return float(converted)

path = r'C:\Users\jeron\OneDrive\Desktop\university\CE888\police data\Borough2019-01.csv'
#path to first month datastet which all other datasets going to be concant to
dirpath = r'C:\Users\jeron\OneDrive\Desktop\university\CE888\police data\borough_data'
#path to directory with all other datsets
metro_data = r'C:\Users\jeron\OneDrive\Desktop\university\CE888\police data\london-borough-profiles.csv'
#path to london borough profiles

full_data = join_datasets(dirpath,path)
#merged datasets
policies = ['Police and Criminal Evidence Act 1984 (section 1)',
 'Misuse of Drugs Act 1971 (section 23)','Firearms Act 1968 (section 47)']
#policies of interst

outcomes = ['Arrest', 'A no further action disposal']
#outcomes of interest

stop_search = full_data[
                        ((full_data['Legislation'] == policies[0])|
                        (full_data['Legislation'] == policies[1])|
                        (full_data['Legislation'] == policies[2]))& 
                        ((full_data['Outcome'] == outcomes[0])|
                        (full_data['Outcome'] == outcomes[1]))
                        ].copy()    
#filtered datset with 3 legislations of interests and 2 outcomes : arrest or no further action
print(len(stop_search))
print(stop_search.columns)

lnd = pd.read_csv(r'C:\Users\jeron\OneDrive\Desktop\university\CE888\police data\london-borough-profiles.csv')
#london boroughs profiles
london_prof = lnd.copy()
interest = ['Code', 'Area_name',
'Unemployment_rate_(2015)','Modelled_Household_median_income_estimates_2012/13']
#columns of interest

london_prof = london_prof[interest]
london_prof = london_prof.replace('.', np.nan)
#turned missing values into nan
london_prof[interest[-1]] = london_prof[interest[-1]].apply(lambda x: converter(x[1:]))
#converted modeled household income into float
london_prof[interest[-2]] = london_prof[interest[-2]].apply(float)
#converted unemployment rate into float
full_copy = stop_search.copy()
#copy of merged and filtered datset
full_copy.set_index('Borough', inplace=True)
#changed index to borough in order to filter out boroughs that are not officially london boroughs
not_wanted_info = ['Outer London', 'London', 'England', 'United Kingdom', 'Inner London']
#info in borough dataset not needed
not_wanted_b = [x for x in london_prof['Area_name'].values if x not in not_wanted_info ]
#london boroughs wanted
ts = full_copy.T[not_wanted_b].copy()
#filtered merged data by boroughs wanted
complete_data = ts.T
#transposed to normal structure
del complete_data['Unnamed: 0.1']
del complete_data['Unnamed: 0']
#deleted residue columns
complete_data.reset_index(inplace=True)
#reset index to normal and borough to column
print(complete_data)

def obtain_borough_info(borough_info, column, main_data):
    for col in column:
        borough_info_dict = {
                        borough:info for borough,info 
                        in zip(borough_info['Area_name'].values, 
                        borough_info[col].values)
                        }
    
        main_data[col] = [
                            borough_info_dict[borough] for
                            borough in main_data['Borough'].values
                            ]
#obtain information of relevance about each borough form the borough info dataset

obtain_borough_info(london_prof, ['Modelled_Household_median_income_estimates_2012/13',
                            'Unemployment_rate_(2015)'],
                                complete_data )


complete_data['Unemployment_rate_(2015)'] = complete_data['Unemployment_rate_(2015)'].fillna(4.8)
# obtained the specific 2015 city of london unemployment 
#filled na 
print(complete_data)







