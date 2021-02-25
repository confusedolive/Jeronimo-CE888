import pandas as pd
import numpy as np
import os
import shutil
import seaborn as sns
import matplotlib.pyplot as plt

def lat_long_to_txt(dirpath):
    ''' iterates through directory containing the datasets,
        extracts latitude and longitude from each dataset
        as a formated txt file named after the dataset'''
    #dirpath to be passed as an r'string' 
    #dirpath should contain path to directory containing datasets

    for dataset in os.listdir(dirpath):   
        stop_search = pd.read_csv(os.path.join(dirpath,dataset))
        df_1 = stop_search[['Latitude','Longitude']].copy()
        df_1.dropna(inplace=True)
        coordinates = list(zip(df_1['Latitude'].values, df_1['Longitude'].values))

    #text files containing coordinates 
    #will be named after its corresponding dataset
    
        with open(f'{dataset[:-4]}.txt', 'w') as f:
            for coordinate in coordinates:
                f.write(f'{coordinate[0]} {coordinate[1]}\n')
           
def add_postcode_df(text_path, dirpath):
    '''Adds postcodes as a new column named postcode to the datasets
    from  a directory containing all the txt files with the postcodes into a directory
    containing the corresponding csv files'''
    for dataset, text in zip(os.listdir(dirpath), os.listdir(text_path)):
        data_stop_search = pd.read_csv(os.path.join(dirpath,dataset))
        df_1 = data_stop_search.copy()
        df_1.dropna(subset=['Latitude', 'Longitude'],inplace=True)
        postcodes = []
        with open(os.path.join(text_path, text), 'r') as f:
            text = f.readlines()
            for postcd in text[1:]:
                postcodes.append(postcd.strip())
        df_1['postcodes'] = postcodes
        df_1.to_csv(f'{dataset[:-4]}postcodes.csv')

def add_borough_df(metro_data_path, borough_data_path):
    ''' adds the borough to each datset'''
    for metro_data, borough_data in zip(os.listdir(metro_data_path), os.listdir(borough_data_path)):
        metropo = pd.read_csv(os.path.join(metro_data_path, metro_data))
        borough = pd.read_csv(os.path.join(borough_data_path, borough_data))
        metropo['Borough'] = borough['District']
        metropo.to_csv(f'Borough{borough_data[:-4]}.csv')



# def month_column(data):
#     df= pd.read_csv(data)
#     df['month'] = df['Date'].apply(lambda x: num_to_month(int(x[5:7])))
#     return df

def join_datasets(dirpath, first_dataset):
    '''Concatenates all datasets using'''
    first = pd.read_csv(first_dataset)
    for dataset in os.listdir(dirpath):
        df = pd.read_csv(os.path.join(dirpath, dataset))
        first = pd.concat([first, df])
    return first







