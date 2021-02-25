
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def unique_counts(data, column, outcome, data_value):
    '''returns dictionary containing unique value in df column and its counts'''
    unique, counts = np.unique(data[data[column] == outcome][data_value], return_counts=True)
    return  dict(zip(unique, counts))

df = pd.read_csv(r'C:\Users\jeron\OneDrive\Desktop\university\CE888\police data\Data used\filtered_merged_data_2019.csv')
test1 = unique_counts(df, 'Outcome', 'Arrest', 'Borough')
test2 = unique_counts(df, 'Outcome', 'A no further action disposal', 'Borough')
general_data = pd.DataFrame({'Borough': test1.keys(), 'Arrest': test1.values(), 'No further action': test2.values()})
general_data['Total'] = general_data['Arrest'] + general_data['No further action']

def obtain_borough_info(borough_info, column, main_data):
    '''From general borough info dataset adds the columns of interest to dataset of interest'''
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



bor = pd.read_csv(r'C:\Users\jeron\OneDrive\Desktop\university\CE888\police data\Data used\lodon_profiles.csv')
obtain_borough_info(bor, ['Modelled_Household_median_income_estimates_2012/13', 'Unemployment_rate_(2015)'], general_data)
mean_household = np.mean(general_data['Modelled_Household_median_income_estimates_2012/13'])

general_data['arrest%'] = (general_data['Arrest']/general_data['Total']*100)
print(general_data)


'''example lineplot of the generated dataset'''

sns.lineplot(data=general_data, x='Unemployment_rate_(2015)', y='arrest%')
plt.xlabel('Modelled household income')
plt.ylabel(r'arrest % of total stop-and-search')
plt.title(r'arrest % of total stop-and-search vs household income by London borough')
plt.show()