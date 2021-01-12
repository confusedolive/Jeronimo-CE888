import pandas as pd
import numpy as np
data = pd.read_csv('NISPUF17.csv')
print(data['P_NUMFLU'].unique())
print(data['CBF_01'].unique())

