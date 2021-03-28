import pandas as pd
from scipy.stats import linregress, spearmanr
import numpy as np
import matplotlib.pyplot as plt
import os

fig_path = os.path.join(os.getcwd(), 'visuals')
df = pd.read_csv(r'data\filtered_merged_data_2019.csv')
data =  df.copy()

#drops unnecessary data for the visualization
data.drop(['Unnamed: 0', 'Date', 'Part of a policing operation', 'Policing operation',
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

def line_int(var1 , var2):
    line = linregress(new_df[var1], new_df[var2])
    plt.plot(new_df[var1], new_df[var2], 'o', label='data')
    plt.plot(new_df[var1], line.intercept + line.slope*new_df[var1],
                                            'r', label='fitted line')

    title = f'relationship between {var1} and {var2}'
    plt.xlabel(var1)
    plt.ylabel(var2)
    plt.title(title)
    plt.savefig(os.path.join(fig_path, title))
    plt.show()
    return line.pvalue

for x in ['stops','median income', 'unemployment']:
    line_int('arrests', x )
