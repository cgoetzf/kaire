import pandas as pd
import numpy as np
from tabulate import tabulate
import globals as gb
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
        df = pd.read_csv(url, names=['location_id','timestamp','day','hour','id','stress','shared_time'],skiprows=1)
        df = df.sort_values(by =['location_id','timestamp','day','hour','id'])
        max_shared_time = 0
        #for i,r in df.iterrows():
            #max_shared_time = df.groupby(['location_id','timestamp','day','hour'], sort=False)['shared_time'].max()
            #df_gsi = df[(df["locationId"] == r['locationId']) & (df["hour"] == r['hour'])& (df["day"] == r['day'])]
        dfi = df.drop(columns=['id','stress','shared_time'])        
        dfi = dfi.drop_duplicates()
        dfi.insert(4,"classification", " ")
        print(dfi)
        df_gsi = df[(df["location_id"] == 2) & (df["timestamp"] == 1620000000) & (df["hour"] == 8)& (df["day"] == 1)]
        #print(df_gsi)
        for i,r in dfi.iterrows():
            
            df_gsi = df[(df["location_id"] == r["location_id"]) & (df["timestamp"] == r["timestamp"]) & (df["day"] == r["day"]) & (df["hour"] == r["hour"])]
            df_gsi = df_gsi.groupby(['location_id','timestamp','day','hour','id','stress']).agg({'shared_time':'sum'}).reset_index()
            #print(df_gsi)            
            max_shared_time = df_gsi.max()[6]
            #print(max_shared_time)
            dividend = 0
            #print(df_gsi)
            for index,row in df_gsi.iterrows():
                if max_shared_time > 0:
                    dividend += (float(row['stress']) * float(row['shared_time']))/max_shared_time
                else:
                    dividend = 0
                #divisor += float(row['shared_time'])
            gsi = round(dividend / df_gsi.shape[0],4)
            dfi._set_value(i,'classification',gsi)
            
            #print(df_gsi.shape[0])
            #df = df.merge(df_gsi, how='left', indicator=True)
            #df = pd.concat([df, df_gsi]).drop_duplicates(keep=False)
            #print("Location: " + str(r['location_id']) + " - Hour:" + str(r['hour']) + " - GSI: " + str(gsi))
            #print('The workgroup located at {0} on {1},{2}h presented a Group Stress Index equal to {3}.'.format(gb.SECTORS[r['location_id']],gb.WEEKDAYS[r['day']],r['hour'],gsi))
        
        dfi = dfi.sort_values(by=['classification','location_id','timestamp','day','hour'])
        print(tabulate(dfi,headers='keys',tablefmt='psql',showindex=False))
        dfi = dfi.sort_values(by=['location_id','timestamp','day','hour'])
        gsi_calc = dfi.drop(columns=['location_id','timestamp','day','hour'])
        gsi_calc = np.ravel(gsi_calc).reshape(1, -1)
        # load dataset into Pandas DataFrame
        gsi_true = pd.read_csv("C:\\_Workspace\\Kaire\\python\\ds\\group_ds_sim.csv", names=['location_id','timestamp','day','hour','classification'],skiprows=1)
        gsi_true = gsi_true.sort_values(by=['location_id','timestamp','day','hour'])        
        gsi_true = gsi_true.drop(columns=['location_id','timestamp','day','hour'])
        gsi_true = np.ravel(gsi_true).reshape(1, -1)
        print(gsi_calc.shape)       
        print(gsi_true.shape)     
        print(gsi_calc)
        print(gsi_true)
        
        from sklearn.metrics.pairwise import cosine_similarity
        print("Sim: " + str(cosine_similarity(gsi_calc , gsi_true)))

    def show_gsi(self):
        print("\n")    
        print("##### Workgroup classification results #####")
        print("\n")
        df = pd.read_csv("group.txt", names=['locationId','date','day','hour','gsi'],skiprows=1)  
        print(tabulate(df,headers=['locationId','date','day','hour','gsi'],tablefmt='github',showindex=False))
        print("\n")