import pandas as pd
import numpy as np
from tabulate import tabulate

class Advisor:
    def __init__(self):
        return None
        
    def generate_data(self):
        return None
        
    def data_prediction(self):
        print(f'Creating dataset for classification! \n')
        df = pd.read_csv(gb.DATASET_PATH+"reasoner_ds.csv", names=['id','stress','locationId','activity','timestamp','duration','day','hour','hrv_mean','hrv_sd','stressorId','shared_time','env_cond'],skiprows=1)         
        df = df.drop(columns=['timestamp','hrv_mean','hrv_sd'])
        df = df.groupby(['id','stress','locationId','activity','day','hour','stressorId','env_cond']).mean().reset_index()
        df = df.drop_duplicates()
        df['duration']=np.floor(df.duration).astype(int)
        df['shared_time']=np.floor(df.shared_time).astype(int)
        df.to_csv(gb.DATASET_PATH+"prediction_ds.csv", index=False)
        
    def notification(self):
        print("##### Notifications #####")
        print("\n")
        print("Worker 6 may be stressed in the Supervisor's Room at the Friday meeting around 2:00 pm. In the analyzed context there are possibilities of stressors as follows: Supervisor 75.35%, worker 5 34.45%, worker 7 12.14%.")
        print("\n")
        
    def prediction(self):
        print("##### Advisor prediction results #####")
        print("\n")
        df = pd.read_csv("advisor.txt", names=['id','stressorId','location','day','hour','activity','env_cond','probability'],skiprows=1)  
        print(tabulate(df,headers=['id','stressorId','location','day','hour','activity','env_cond','probability'],tablefmt='github',showindex=False))
        print("\n")