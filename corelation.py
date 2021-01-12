import pandas as pd
def average_influenza_doses():
    data = pd.read_csv(r'NISPUF17.csv')
    df = data[['P_NUMFLU', 'CBF_01']].dropna()
    breastfed = df[df['CBF_01']==1]
    not_breastfed = df[df['CBF_01']==2]
    
    return (breastfed['P_NUMFLU'].sum()/len(breastfed['P_NUMFLU']),
            not_breastfed['P_NUMFLU'].sum()/len(breastfed['P_NUMFLU']))
    raise NotImplementedError()
print(average_influenza_doses())