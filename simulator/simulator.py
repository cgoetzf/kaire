import simpy
import simulator_env as e
import simulator_person as p
import random as rnd
from datetime import datetime
import pandas as pd
import globals as gb
import numpy as np

class Simulator:
    
    @property
    def days(self):
        return self._days
        
    @days.setter
    def days(self,days):
        self._days = days

    @property
    def seconds(self):
        return self._seconds
        
    @seconds.setter
    def seconds(self,seconds):
        self._seconds = seconds
        
    @property
    def init_time(self):
        return self._init_time
        
    @init_time.setter
    def init_time(self,init_time):
        self._init_time = init_time
        
    def __init__(self):
        self._init_time = pd.Timestamp.now()
        self._seconds = 24 * 60 * 60
        self._days = 1   

    def env(self):
        #criando ambiente de simulação
 
        #inicializando arquivos
        with open(gb.WORKERS_FILE,'w') as f:
                        f.write("id,timestamp,hrv,stressIndex,locationId\n")

        with open(gb.ENV_FILE,'w') as f:
                        f.write("locationId,timestamp,temperature,humidity,noise,light\n")
        
        with open(gb.DATASET_PATH+"line_ds.csv",'w') as f:
            f.write("id,stress,timestamp,hr,rmssd,sdrr,rr\n") 
            
        self._env = simpy.Environment()
        self._industry = e.Industry(self._env, self._init_time)

        worker1 = p.Person(self._env,self._init_time,1,"Worker1",40,2)
        worker2 = p.Person(self._env,self._init_time,2,"Worker2",32,2)
        worker3 = p.Person(self._env,self._init_time,3,"Worker3",25,3)
        worker4 = p.Person(self._env,self._init_time,4,"Worker4",50,3)
        worker5 = p.Person(self._env,self._init_time,5,"Worker5",27,4)
        worker6 = p.Person(self._env,self._init_time,6,"Worker6",31,4)
        worker7 = p.Person(self._env,self._init_time,7,"Worker7",22,4)
        supervisor = p.Person(self._env,self._init_time,8,"Supervisor",42,6)

        self._env.process(e.component1_process(self._env,self._industry,worker1,supervisor))
        self._env.process(e.component1_process(self._env,self._industry,worker2,supervisor))
        self._env.process(e.component2_process(self._env,self._industry,worker3,supervisor))
        self._env.process(e.component2_process(self._env,self._industry,worker4,supervisor))
        self._env.process(e.assembly_process(self._env,self._industry,worker5,supervisor))
        self._env.process(e.assembly_process(self._env,self._industry,worker6,supervisor))
        self._env.process(e.assembly_process(self._env,self._industry,worker7,supervisor))
        self._env.process(e.supervision_process(self._env, self._industry,supervisor,[worker1,worker2,worker3,worker4,worker5,worker6,worker7]))

    def run(self):
        ts = self._init_time.timestamp()
        hour = int((ts % 86400)/3600)
        day = (int(ts / 86400)+4) % 7
        weekday = "error!"
        match day:
            case 0:
                weekday="Sunday"
            case 1:
                weekday="Monday"
            case 2:
                weekday="Tuesday"
            case 3:
                weekday="Wednesday"
            case 4:
                weekday="Thursday"
            case 5:
                weekday="Friday"
            case 6:
                weekday="Saturday"
            case _:
                weekday("Something's wrong!")
        print(f'----------------------------------')
        print(f'Starting simulation: '+ str(weekday))
        print(f'----------------------------------')
        

        simulation_duration = self._seconds * self._days
        self._env.run(until = simulation_duration)


        print(f'----------------------------------')
        print(f'Simulation result')
        print(f'----------------------------------')
        print('Stock level: {0} components 1 and {1} components 2.'.format(self._industry.componenet1_stock.level, self._industry.componenet2_stock.level))
        print(f'Finished products: %d' % self._industry.dispatch.level)
        print(f'----------------------------------')
        print(f'Simulation finished!')
        print(f'----------------------------------')

    def reset_files(self):
        with open(gb.DATASET_PATH+"reasoner_ds.csv",'w') as f:
            f.write("id,stress,locationId,activity,timestamp,duration,day,hour,hrv_mean,hrv_sd,stressorId,shared_time,env_cond,cond\n")
        with open(gb.DATASET_PATH+"group_ds.csv",'w') as f:
            f.write("locationId,timestamp,day,hour,id,stress,shared_time\n") 
            
    def remove_duplicates(self):

        print(f'Removing duplicates! \n')

        df = pd.read_csv(gb.DATASET_PATH+"reasoner_ds.csv", names=['id','stress','locationId','activity','timestamp','duration','day','hour','hrv_mean','hrv_sd','stressorId','shared_time','env_cond','cond'],skiprows=1)         
        df = df.drop_duplicates()
        df.to_csv(gb.DATASET_PATH+"reasoner_ds.csv", index=False)
   
    def data_prediction(self):
        print(f'Creating dataset for classification! \n')
        df = pd.read_csv(gb.DATASET_PATH+"reasoner_ds.csv", names=['id','stress','locationId','activity','timestamp','duration','day','hour','hrv_mean','hrv_sd','stressorId','shared_time','env_cond','cond'],skiprows=1)         
        
        df.insert(13,"classification", " ")
        for i,row in df.iterrows():
            if int(row['stress']) == 1:
                if int(row['stressorId']) == 8:
                   df._set_value(i,'classification',1)
                else:
                    df._set_value(i,'classification',0)
            else:
                df._set_value(i,'classification',0)
                
        df = df.drop(columns=['timestamp','hrv_mean','hrv_sd','cond'])

        df = df.groupby(['id','stress','locationId','activity','day','hour','stressorId','env_cond'])['shared_time'].mean().reset_index()
        print("#")
        print(df)
        print("#")
        df = df.drop_duplicates()
        
        #df['duration']=np.floor(df.duration).astype(int)
        df['shared_time']=np.floor(df.shared_time).astype(int)
        df.to_csv(gb.DATASET_PATH+"prediction_ds.csv", index=False)
        
    def data_training(self):
        print(f'Creating dataset for training! \n')
        df = pd.read_csv(gb.DATASET_PATH+"reasoner_ds.csv", names=['id','stress','locationId','activity','timestamp','duration','day','hour','hrv_mean','hrv_sd','stressorId','shared_time','env_cond','cond'],skiprows=1)        
        df.insert(13,"classification", " ")
        for i,row in df.iterrows():
            if int(row['stress']) == 1:
                if int(row['stressorId']) == 8:
                   df._set_value(i,'classification',1)
                else:
                    df._set_value(i,'classification',0)
            else:
                df._set_value(i,'classification',0)
        df.to_csv(gb.DATASET_PATH+"training_ds.csv", index=False)