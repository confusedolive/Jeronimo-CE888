import pandas as pd
def proportion_of_education():
    pandas_file = pd.read_csv(r'NISPUF17.csv')
    diccion = {}
    lista = ["less than high school", "high school", "more than high school but not college", "college"]
    #for x,y in zip(lista, [1,2,3,4]):
        #diccion[x] =  (len(pandas_file[pandas_file['EDUC1'] == y]))/(len(pandas_file['EDUC1']))
    
    diccion = {x:len(pandas_file[pandas_file['EDUC1'] == y])/(len(pandas_file['EDUC1'])) 
              for (x,y) in zip(lista,[1,2,3,4])}
    
    return diccion

print(proportion_of_education())