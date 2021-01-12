import pandas as pd
import numpy as np

df = pd.DataFrame({'Countries':['Spain','England','France', 'Germany'],
                    'Language': ['spanish', 'English', 'french','german']})

def f(x):
    return True if x[0].isupper() else False

print(df.Language.map(f))