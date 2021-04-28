import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from scipy.stats import linregress, spearmanr
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler

#########################################################################################################################
#                                                Visual Exploration                                                     #
#          Exploration to further understand the distribution of the Outcome of Stop and search  and the correlations   #
#########################################################################################################################

fig_path = os.path.join(os.getcwd(), 'visuals')
df = pd.read_csv(r'data\filtered_merged_data_2019.csv')
data = df.copy()

# drops unnecessary data , all variables in part of policing operation are False, dropped.
data.drop(['Unnamed: 0', 'Date', 'Part of a policing operation', 'Policing operation',
           'Latitude', 'Longitude', 'postcode'], axis=1, inplace=True)

data.isnull().sum()
data.dropna(inplace=True)  # Drops missing values

data.rename(columns={'Modelled_Household_median_income_estimates_2012/13': 'median income',
                     'Unemployment_rate_(2015)': 'unemployment rate'}, inplace=True)  # renames columns for ease of use

# encode Outcome variable
le = LabelEncoder()
data['Outcome'] = le.fit_transform(data['Outcome'])
groups = data.groupby('Borough')  # groups by borough

# creates a list of lists containing borough, median income, unemployment rate, n of arrests and total stops.
grouped = [[brgh, len(ds),
            ds['median income'].unique()[0],
            len(ds[ds['Outcome'] == 1]),
            ds['unemployment rate'].unique()[0]]
           for brgh, ds in groups]


new_df = pd.DataFrame(grouped, columns=['borough', 'stops', 'median income',
                                        'arrests', 'unemployment'])  # Creates dataframe
correlation_matrix = new_df.corr()
# Stops and median income negative pearson correlation -0.44
# stops and unemployment positive pearson correlation 0.39
# arrests and median income -0.43
# arrests and unemployment 0.35


def correlation_pval():
    '''
        Plots a heatmap with the pearson coeeficient correlation
        prints the variables of interest and their corresponding
        correlation to number of arrests , it also prints the
        p values for this correlations
        --------------------------------------------------------
        returns a list of tuples containing (variable, p value)
        --------------------------------------------------------
        '''
    sns.heatmap(correlation_matrix, annot=True, cmap='Blues', vmin=-1, vmax=1)
    plt.title('Correlation Heatmap')
    plt.savefig(r'visuals/Correlation heatmap.png')
    plt.show()
    llista = ['median income', 'unemployment']
    output = 'arrests'
    vals = []
    for x in llista:
        corr, p = stats.pearsonr(new_df[x], new_df[output])
        print(f'{x} has correlation {corr} with {output} p_val = {p}')
        vals.append((x, p))
    return vals


p_vals = correlation_pval()

print(p_vals)
##########visualize relationships########################


def line_int(df, var1, var2):
    '''
       ---------------------------------------------
       Calculates a linear least-squares regression
       between two variables, plots the best line
       between this variables returns the p-value
       null hyptohesis being the slope is zero.
       ---------------------------------------------
        df = dataset containing variables
        var1 = first variable for linregress
        var2 = second variable for linregress
       ---------------------------------------------
         '''
    sns.set_palette('Blues_r')
    line = linregress(df[var1], df[var2])
    plt.plot(df[var1], df[var2], 'o', label='data')
    plt.plot(df[var1], line.intercept + line.slope * df[var1],
             'r', label='fitted line')

    title = f'correlation between {var1} and {var2}'
    plt.xlabel(var1)
    plt.ylabel(var2)
    plt.title(title)
    plt.savefig(os.path.join(fig_path, title))
    plt.show()
    return line.pvalue


for x in ['stops', 'median income', 'unemployment']:
    p_val = line_int(new_df, 'arrests', x)
    print(f'{x} pvalue = {p_val:.3f}')


# object of search frequency

def plot_object_search(data, type, save=False):
    '''
       --------------------------------------------------------
       Plot the frequency of reasons for search, expects
       the outcome variable to be label encoded
       --------------------------------------------------------
       data = data to be plotted
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
    perc = visual_data['Object of search'].value_counts() / len(data) * 100
    fig = perc.sort_values(ascending=False).plot.bar()
    fig.set_title(title)
    fig.set_ylabel('Percentage of total stop and search occurences')
    plt.xticks(rotation=65)
    if save:
        plt.savefig(os.path.join('visuals', title), bbox_inches='tight')
    print('-' * 50)
    plt.show()
    print('-' * 50)
    print(perc.apply(lambda x: round(x, 2)))
    print('-' * 50)


test1 = data[data['Outcome'] == 0]
test2 = data[data['Outcome'] == 1]

plot_object_search(test1, 'dismissed cases', save=True)
plot_object_search(test2, 'Arrest cases', save=True)


def percentage_arrest(val):
    for group in data[val].unique():
        stop = data[data[val] == group]
        no_arrest = len(stop[stop['Outcome'] == 0])
        arrest = len(stop[stop['Outcome'] == 1])
        print(f'group {group} \n')
        print(
            f'Total population of group {len(stop)} | {len(stop)/len(data)*100:.2f}%')
        print('-' * 60)
        print(f'percentage of arrest: {(arrest/len(stop))*100:.2f}%')
        print(
            f'percentage of no further action: {no_arrest/len(stop)*100:.2f}%')
        print('-' * 60)


def plot_unique_outcome(val):
    '''
    ------------------------------------------
    For  variable inputted it plots
    a graph showing the Outcome distribution per
    unique value in the selected variable.
    prints a pseudo-report on each group of unique
    value with the amount of samples per group
    total percentage , and percentage of arrest
    and no further action per group.
    --------------------------------------------
        val = Unique variable to be checked
    --------------------------------------------
    '''
    path = r'visuals\frequencies'
    print('-' * 20, val, '-' * 20)
    sns.set_palette('Set1')
    sns.histplot(x=val, data=data, hue='Outcome', multiple='stack')
    plt.title(val)
    plt.xticks(rotation=90)
    plt.legend(title='Outcome', labels=['Arrest', 'No further action'])
    plt.savefig(os.path.join(path, f'{val} frequency and outcome.png'))
    plt.show()
    print('-' * 60)
    percentage_arrest(val)


for x in [n for n in data.columns if n not in ['Outcome', 'labels']]:
    plot_unique_outcome(x)
