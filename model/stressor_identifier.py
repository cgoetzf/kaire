import pandas as pd
import numpy as np
from tabulate import tabulate

class StressorIdentifier:
    def __init__(self):
        return None
        
    def classification(self):
        print("\n")    
        print("##### Stressor identifier classification results #####")
        print("\n")
        df = pd.read_csv("notifications.txt", names=['id','stressorId','location','day','hour','shared_time','env_cond','probability'],skiprows=1)  
        print(tabulate(df,headers=['id','stressorId','location','day','hour','shared_time','env_cond','probability'],tablefmt='github',showindex=False))
        print("\n")
        
    def notification(self):
        print("##### Notifications #####")
        print("\n")
        print("Worker 1 experienced stress in the Supervisor Room on Monday around 10 am during 2100 seconds. No irregular conditions identified in the environment. Supervisor has an 85.60% probability of being the stressor in the analyzed context.")
        print("\n")
        
    def calculate_gsi(self):
        url = "C:\\_Workspace\\Kaire\\python\\ds\\group_ds.csv"
        # load dataset into Pandas DataFrame
        df = pd.read_csv(url, names=['id','stress','locationId','activity','timestamp','duration','day','hour','hrv_mean','hrv_sd','stressorId','shared_time','env_cond'],skiprows=1)
        df = df.sort_values(by =['locationId','day','hour','id'])
        df = df.drop(columns=['activity','timestamp','hrv_mean','hrv_sd','stressorId','env_cond'])
        dividend = divisor = 0
        dfi = df.drop(columns=['id','duration','shared_time','stress'])
        dfi = dfi.drop_duplicates()
        print(dfi)
        for i,r in dfi.iterrows():
            df_gsi = df[(df["locationId"] == r['locationId']) & (df["hour"] == r['hour'])& (df["day"] == r['day'])]
            print(df_gsi)
            df_gsi = df_gsi.groupby(['id','locationId','day','hour']).agg({'duration':'sum', 'shared_time':'sum','stress':'mean'}).reset_index()
            
            for index,row in df_gsi.iterrows():
                dividend += float(row['stress']) * float(row['shared_time'])
                divisor += float(row['shared_time'])
            gsi = round(dividend / divisor,4)
            #df = df.merge(df_gsi, how='left', indicator=True)
            #df = pd.concat([df, df_gsi]).drop_duplicates(keep=False)
            #print(gsi)
            
    def show_gsi(self):
        print("\n")    
        print("##### Workgroup classification results #####")
        print("\n")
        df = pd.read_csv("group.txt", names=['locationId','date','day','hour','gsi'],skiprows=1)  
        print(tabulate(df,headers=['locationId','date','day','hour','gsi'],tablefmt='github',showindex=False))
        print("\n")