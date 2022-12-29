from owlready2 import *
import pandas as pd
import globals as gb
import math
from tabulate import tabulate
owlready2.JAVA_EXE = gb.JAVA_PATH

class OntoWesad:

    #def __init__(self):
        
    def compose_dataset(self):
        files = ["IBI_s2.csv","IBI_s3.csv","IBI_s4.csv","IBI_s5.csv","IBI_s6.csv","IBI_s7.csv","IBI_s8.csv","IBI_s9.csv","IBI_s10.csv","IBI_s11.csv","IBI_s13.csv","IBI_s14.csv","IBI_s15.csv","IBI_s16.csv","IBI_s17.csv"]
        #files = ["TESTE.CSV"]
        with open("C:\\OneDrive\\Estudos\\Mestrado\\Dissertation\\Code\\Data\\transformed_ds.csv",'w') as f:
            f.write("ts_min,duration,id,day,hour,hrv_mean,hrv_sd,stressIndex,locationId,stressorId,shared_time,classification\n")
        with open("C:\\OneDrive\\Estudos\\Mestrado\\Dissertation\\Code\\Data\\evaluation_ds.csv",'w') as f:
            f.write("id,ts_min,ts_max,hrv_mean,hrv_sd,stressIndex,locationId\n")
            
        for file in files:
            self.df_workers = pd.read_csv("C:\\OneDrive\\Estudos\\Mestrado\\Dissertation\\Code\\Data\\"+file, names=['hasId','hasTimestamp','sec', 'IBI', 'RR1-RR2', 'hasHRV','hasLocationId','hasStressIndex'],skiprows=1)        
            self.df_workers = self.df_workers.sort_values(by =['hasId','hasTimestamp'])
            id_curr = ts_min = ts_max = hrv_min = hrv_max = hrv_sd = sd_avg = sd_sum = hrv = stressIndex = 0
            ibi_mean = ibi_prev = ibi_curr = hrv_interval = ibi_counter = hrv_mean = 0
            hrv_list = prev_row = []
            
            for i,row in self.df_workers.iterrows():
                
                id_curr = int(getattr(row, 'hasId'))

                if (i == 0):
                    ts_min = int(row['hasTimestamp'])
                    ibi_curr = float(row['IBI'])                    
                    hrv_min = 0
                    hrv_max = 0
                    hrv_list = []  
                elif (int(getattr(row, 'hasId')) != int(getattr(prev_row, 'hasId')) and i > 1) or (int(getattr(row, 'hasId')) == int(getattr(prev_row, 'hasId')) and int(getattr(row, 'hasStressIndex')) != int(getattr(prev_row, 'hasStressIndex'))) or (int(getattr(row, 'hasId')) == int(getattr(prev_row, 'hasId')) and int(getattr(row, 'hasLocationId')) != int(getattr(prev_row, 'hasLocationId'))) or (int(getattr(row, 'hasId')) == int(getattr(prev_row, 'hasId')) and (int(getattr(row, 'hasTimestamp')) - ts_min) > 1800):
                    ts_max = int(prev_row['hasTimestamp'])
                    if len(hrv_list) > 0:
                        stressorId = 0
                        classif = 0
                        sd_avg = round(sum(hrv_list) / len(hrv_list),4)
                        for x in hrv_list:
                            sd_sum += (x - sd_avg) ** 2
                        hrv_sd = round(math.sqrt(sd_sum/len(hrv_list)),4)
                        if hrv_min != 0:
                            if int(getattr(prev_row, 'hasStressIndex')) >= 3:
                                stressIndex = 1
                            else:
                                stressIndex = 0
                            if int(prev_row['hasLocationId']) == 2:
                                stressorId = 17
                                classif = 1
                            elif int(prev_row['hasLocationId']) == 3:
                                stressorId = 16
                            hour = int((ts_min % 86400)/3600)
                            day = (int(ts_min / 86400)+4) % 7
                            with open("C:\\OneDrive\\Estudos\\Mestrado\\Dissertation\\Code\\Data\\transformed_ds.csv",'a') as f:
                                f.write(str(ts_min) + "," + str(ts_max - ts_min) + "," + str(int(prev_row['hasId'])) + "," + str(day) + "," + str(hour) + "," + str(sd_avg) + "," + str(hrv_sd) + "," + str(stressIndex) + "," + str(int(prev_row['hasLocationId'])) + "," + str(stressorId) + "," + str(ts_max - ts_min) + "," + str(classif) + "\n")
                            with open("C:\\OneDrive\\Estudos\\Mestrado\\Dissertation\\Code\\Data\\evaluation_ds.csv",'a') as f:
                                f.write(str(int(prev_row['hasId'])) + "," + str(ts_min) + "," + str(ts_max) + "," + str(sd_avg) + "," + str(hrv_sd) + "," + str(stressIndex) + "," + str(int(prev_row['hasLocationId'])) + "\n")
                    
                            ts_min = int(row['hasTimestamp'])  
                            ibi_curr = float(row['IBI'])
                            hrv_min = hrv_mean = 0
                            hrv_max = 0
                            hrv_list = []
                            hrv_interval = 0
                            hrv_sd = 0
                            sd_sum = 0
                    
                else:
                    ibi_mean += ((float(prev_row['IBI']) - float(row['IBI'])) ** 2)
                    #ver se vale a pena por segundo
                    c = 1
                    while int(row['hasTimestamp']) > int(prev_row['hasTimestamp'])+ c and i > 0:
                        ibi_mean += ((float(prev_row['IBI']) - ((float(prev_row['IBI'])+float(row['IBI']))/2)) ** 2)
                        ibi_counter += 1
                        hrv_interval += ((float(prev_row['IBI'])+float(row['IBI']))/2)
                        c += 1
                    hrv_interval += float(row['IBI'])
                    #self.hr = int(round(60/ibi_curr,0))
                    ibi_counter += 1
                    hrv = round(math.sqrt(ibi_mean/ibi_counter),4)
                    if hrv_interval > 150:
                        hrv_interval -= 150
                        hrv_list.append(hrv)
                        ibi_mean = ibi_counter = 0
                        if hrv_min > hrv or hrv_min == 0:
                            hrv_min = hrv
                        if  hrv_max < hrv or hrv_max == 0:
                            hrv_max = hrv
                prev_row = row

    def compose_envdataset(self):
        df_env = pd.read_csv("C:\\OneDrive\\Estudos\\Mestrado\\Dissertation\\Code\\python\\olds\\environment.csv", names=['timestamp','locationId','temperature', 'humidity', 'noise', 'light'],skiprows=1)        
        df_env = df_env.sort_values(by =['locationId','timestamp'])
        with open("C:\\OneDrive\\Estudos\\Mestrado\\Dissertation\\Code\\Data\\evaluation_envds.csv",'w') as f:
            f.write("locationId,ts_min,ts_max,temperature,humidity,noise,light\n")
        for i,row in df_env.iterrows():
            if (i == 0):
                ts_min = int(row['timestamp'])
                temp = int(row['temperature'])                    
                hum = int(row['humidity'])
                noise = int(row['noise'])
                light = int(row['light']) 
            elif (int(getattr(row, 'locationId')) != int(getattr(prev_row, 'locationId')) and i > 1) or (int(getattr(row, 'locationId')) == int(getattr(prev_row, 'locationId')) and int(getattr(row, 'temperature')) != int(getattr(prev_row, 'temperature'))) or (int(getattr(row, 'locationId')) == int(getattr(prev_row, 'locationId')) and int(getattr(row, 'humidity')) != int(getattr(prev_row, 'humidity'))) or (int(getattr(row, 'locationId')) == int(getattr(prev_row, 'locationId')) and int(getattr(row, 'noise')) != int(getattr(prev_row, 'noise'))) or (int(getattr(row, 'locationId')) == int(getattr(prev_row, 'locationId')) and int(getattr(row, 'light')) != int(getattr(prev_row, 'light'))) or (int(getattr(row, 'locationId')) == int(getattr(prev_row, 'locationId')) and (int(getattr(row, 'timestamp')) - ts_min) > 28800):
                ts_max = int(prev_row['timestamp'])
                temp = int(prev_row['temperature'])                    
                hum = int(prev_row['humidity'])
                noise = int(prev_row['noise'])
                light = int(prev_row['light']) 
                with open("C:\\OneDrive\\Estudos\\Mestrado\\Dissertation\\Code\\Data\\evaluation_envds.csv",'a') as f:
                    f.write(str(int(prev_row['locationId'])) + "," + str(ts_min) + "," + str(ts_max) + "," + str(temp) + "," + str(hum) + "," + str(noise) + "," + str(light) + "\n")
                ts_min = int(row['timestamp'])  
                temp = int(row['temperature'])                    
                hum = int(row['humidity'])
                noise = int(row['noise'])
                light = int(row['light']) 
            prev_row = row    
    
    def create_ontology(self):
        onto = get_ontology("file://onto.owl").load()
        df = pd.read_csv("C:\\OneDrive\\Estudos\\Mestrado\\Dissertation\\Code\\Data\\evaluation_ds.csv", names=['id','ts_min','ts_max','hrv_mean','hrv_sd','stressIndex','locationId'],skiprows=1)        
        df_env = pd.read_csv("C:\\OneDrive\\Estudos\\Mestrado\\Dissertation\\Code\\Data\\evaluation_envds.csv", names=['locationId','ts_min','ts_max','temperature','humidity','noise','light'],skiprows=1)        
 
        with onto:
            id1 = onto.Identity("Worker1", namespace = onto, hasId = [1], hasWorkplaceId = [6])
            id2 = onto.Identity("Worker2", namespace = onto, hasId = [2], hasWorkplaceId = [6])
            id3 = onto.Identity("Worker3", namespace = onto, hasId = [3], hasWorkplaceId = [6])
            id4 = onto.Identity("Worker4", namespace = onto, hasId = [4], hasWorkplaceId = [6])
            id5 = onto.Identity("Worker5", namespace = onto, hasId = [5], hasWorkplaceId = [6])
            id6 = onto.Identity("Worker6", namespace = onto, hasId = [6], hasWorkplaceId = [6])
            id7 = onto.Identity("Worker7", namespace = onto, hasId = [7], hasWorkplaceId = [6])
            id8 = onto.Identity("Worker8", namespace = onto, hasId = [8], hasWorkplaceId = [6])
            id9 = onto.Identity("Worker9", namespace = onto, hasId = [9], hasWorkplaceId = [6])
            id10 = onto.Identity("Worker10", namespace = onto, hasId = [10], hasWorkplaceId = [6])
            id11 = onto.Identity("Worker11", namespace = onto, hasId = [11], hasWorkplaceId = [6])
            id12 = onto.Identity("Worker12", namespace = onto, hasId = [12], hasWorkplaceId = [6])
            id13 = onto.Identity("Worker13", namespace = onto, hasId = [13], hasWorkplaceId = [6])
            id14 = onto.Identity("Worker14", namespace = onto, hasId = [14], hasWorkplaceId = [6])           
            id15 = onto.Identity("Worker15", namespace = onto, hasId = [15], hasWorkplaceId = [6])
            id16 = onto.Identity("Television", namespace = onto, hasId = [16])            
            id17 = onto.Identity("TSST", namespace = onto, hasId = [17])            
            
            loc1 = onto.Location("BaselineRoom", namespace = onto, hasLocationId = [1])
            loc2 = onto.Location("StressRoom", namespace = onto, hasLocationId = [2])
            loc3 = onto.Location("AmusementRoom", namespace = onto, hasLocationId = [3])
            loc4 = onto.Location("RelaxingRoom", namespace = onto, hasLocationId = [4])
            loc5 = onto.Location("RecoveryRoom", namespace = onto, hasLocationId = [5])
            
            ################
            
            for i,row in df.iterrows():
                if i > 0:
                    individualName = "Context" + str(i)
                    worker = onto.Worker(individualName, namespace = onto, hasId = [int(row['id'])], hasTsMin = [int(row['ts_min'])], hasTsMax = [int(row['ts_max'])], hasHRV = [float(row['hrv_mean'])], hasHRVsd = [float(row['hrv_sd'])], hasStressIndex = [int(row['stressIndex'])], hasLocationId = [int(row['locationId'])])
                if int(row['locationId']) == 2:
                    individualName = "ObjContext" + str(i)
                    object = onto.Object(individualName, namespace = onto, hasId = [17], hasTsMin = [int(row['ts_min'])], hasTsMax = [int(row['ts_max'])], hasLocationId = [int(row['locationId'])])
                elif int(row['locationId']) == 3:
                    individualName = "ObjContext" + str(i)
                    object = onto.Object(individualName, namespace = onto, hasId = [16], hasTsMin = [int(row['ts_min'])], hasTsMax = [int(row['ts_max'])], hasLocationId = [int(row['locationId'])])
            for i,row in df_env.iterrows():
                individualName = "EnvContext" + str(i)
                if i > 0:
                    env = onto.Workplace(individualName, namespace = onto, hasLocationId = [int(row['locationId'])], hasTsMin = [int(row['ts_min'])], hasTsMax = [int(row['ts_max'])], hasCelsius = [int(row['temperature'])], hasHumPercent = [int(row['humidity'])], hasDecibels = [int(row['noise'])],hasLux = [int(row['light'])])
            onto.save(file = "OntokaireEvaluation.owl")