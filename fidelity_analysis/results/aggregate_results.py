# Aggregate fidelity results to a single CSV file
import os
import numpy as np
import pandas as pd
from glob import iglob

pd.set_option('precision', 3)

def read_df_rec(path, fn_regex=r'*results.csv'):

    dfs = []

    for f in iglob(os.path.join(path, '**', fn_regex), recursive=True):
        print(f)
        df = pd.read_csv(f)
        print(df.head())
        zone = f.split('_')[1]
        
        df['Class'] = zone
        
        if 'clpx' in f:
            domain = 'CLPX'
            df['Swath'] = domain
        elif 'hv' in f:
            domain = 'HV'
            df['Swath'] = domain
        

        dfs.append(df)

    
    all_recs = pd.concat(dfs)
    
    #del all_recs['nrmse_arr']

    all_recs['Winters'] = all_recs.iloc[:, 0]
    all_recs['Winters'] = all_recs['Winters'].apply(lambda x: x[-4:] + ' v. ' + x[0:4] if int(x[0:4]) > int(x[-4:]) else x)
    del all_recs['Unnamed: 0']
    
    print(all_recs.head())
    print(len(all_recs))

    return all_recs

agg = read_df_rec('.')
agg.to_csv('all_fidelity_results.csv', index=False)

