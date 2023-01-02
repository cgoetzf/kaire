from owlready2 import *
import pandas as pd
import globals as gb
import math
from tabulate import tabulate
owlready2.JAVA_EXE = gb.JAVA_PATH

class OntoKaire:

    def __init__(self):
        self.static = True
               
    def init_dataset(self):
        if self.static:
            url_workers = gb.WORKERS_FILE
            url_env = gb.ENV_FILE
            self.df_workers = pd.read_csv(url_workers, names=['id','timestamp','hrv','stress_index','location_id'],skiprows=1)
            self.df_env = pd.read_csv(url_env, names=['location_id','timestamp','temperature', 'humidity', 'noise','light'],skiprows=1)
        else:
            from mysqlDb import mysqlConn
            conn = mysqlConn()
            self.df_workers = pd.read_sql('SELECT * FROM history', conn)
            self.df_env = pd.read_sql('SELECT * FROM history', conn)
        
    def compose_dataset(self):
        with open(gb.DATASET_PATH+"workers_ds.csv",'w') as f:
            f.write("id,ts_min,ts_max,hr,rmssd,sdrr,stress_index,location_id\n")
        url_workers = gb.WORKERS_FILE    
        self.df_workers = pd.read_csv(url_workers, names=['id','timestamp','hr','rmssd','sdrr','stress_index','location_id'],skiprows=1)
        self.df_workers = self.df_workers.sort_values(by =['id','timestamp','location_id','stress_index'])
        #print(tabulate(self.df_workers,headers='keys',tablefmt='psql',showindex=False))
        id_prev = id_curr = ts_min = ts_max = rmssd_mean = sdrr_mean = hr_mean = 0
        prev_row = []
        hr_list = []        
        rmssd_list = []
        sdrr_list = []
        
        for i,row in self.df_workers.iterrows():
            id_curr = int(row['id'])

            if (len(self.df_workers)-1) != i and i > 1:
                if (int(getattr(row, 'id')) != int(getattr(prev_row, 'id'))) or (int(getattr(row, 'id')) == int(getattr(prev_row, 'id')) and int(getattr(row, 'stress_index')) != int(getattr(prev_row, 'stress_index'))) or (int(getattr(row, 'id')) == int(getattr(prev_row, 'id')) and int(getattr(row, 'timestamp')) - ts_min > 1800):
                    ts_max = int(prev_row['timestamp'])
                    if ts_max == ts_min:
                        ts_max = int(row['timestamp']) -10
                    rmssd_mean = int(round(sum(rmssd_list) / len(rmssd_list),4))
                    sdrr_mean = int(round(sum(sdrr_list) / len(sdrr_list),4))
                    hr_mean = int(round(sum(hr_list) / len(hr_list),4))
                    
                    with open(gb.DATASET_PATH+"workers_ds.csv",'a') as f:
                        f.write(str(id_curr) + "," + str(ts_min) + "," + str(ts_max) + "," + str(hr_mean) + "," + str(rmssd_mean) + "," + str(sdrr_mean) + "," + str(int(row['stress_index'])) + "," + str(int(row['location_id'])) + "\n")
                    hr_list = []
                    sdrr_list = []
                    rmssd_list = []
                    
                if (int(getattr(row, 'id')) == int(getattr(prev_row, 'id'))):
                    hr_list.append(float(row['hr']))
                    rmssd_list.append(float(row['rmssd']))
                    sdrr_list.append(float(row['sdrr']))
                        
            if (i == 0) or (int(getattr(row, 'id')) != int(getattr(prev_row, 'id'))) or (int(getattr(row, 'id')) == int(getattr(prev_row, 'id')) and int(getattr(row, 'stress_index')) != int(getattr(prev_row, 'stress_index'))) or (int(getattr(row, 'id')) == int(getattr(prev_row, 'id')) and int(getattr(row, 'timestamp')) - ts_min > 1800):
                id_prev = id_curr
                ts_min = int(row['timestamp'])  
            prev_row = row
            
    def compose_envdataset(self):
        df_env = pd.read_csv(gb.ENV_FILE, names=['location_id','timestamp','temperature', 'humidity', 'noise', 'light'],skiprows=1)        
        df_env = df_env.sort_values(by =['location_id','timestamp'])
        with open(gb.DATASET_PATH+"environment_ds.csv",'w') as f:
            f.write("location_id,ts_min,ts_max,temperature,humidity,noise,light\n")
        for i,row in df_env.iterrows():
            if (i == 0):
                ts_min = int(row['timestamp'])
                temp = int(row['temperature'])                    
                hum = int(row['humidity'])
                noise = int(row['noise'])
                light = int(row['light']) 
            elif (int(getattr(row, 'location_id')) != int(getattr(prev_row, 'location_id')) and i > 1) or (int(getattr(row, 'location_id')) == int(getattr(prev_row, 'location_id')) and int(getattr(row, 'temperature')) != int(getattr(prev_row, 'temperature'))) or (int(getattr(row, 'location_id')) == int(getattr(prev_row, 'location_id')) and int(getattr(row, 'humidity')) != int(getattr(prev_row, 'humidity'))) or (int(getattr(row, 'location_id')) == int(getattr(prev_row, 'location_id')) and int(getattr(row, 'noise')) != int(getattr(prev_row, 'noise'))) or (int(getattr(row, 'location_id')) == int(getattr(prev_row, 'location_id')) and int(getattr(row, 'light')) != int(getattr(prev_row, 'light'))) or (int(getattr(row, 'location_id')) == int(getattr(prev_row, 'location_id')) and (int(getattr(row, 'timestamp')) - ts_min) > 28800):
                ts_max = int(prev_row['timestamp'])
                if ts_max == ts_min:
                    ts_max = int(row['timestamp']) -10
                temp = int(prev_row['temperature'])                    
                hum = int(prev_row['humidity'])
                noise = int(prev_row['noise'])
                light = int(prev_row['light']) 
                with open(gb.DATASET_PATH+"environment_ds.csv",'a') as f:
                    f.write(str(int(prev_row['location_id'])) + "," + str(ts_min) + "," + str(ts_max) + "," + str(temp) + "," + str(hum) + "," + str(noise) + "," + str(light) + "\n")
                ts_min = int(row['timestamp'])  
                temp = int(row['temperature'])                    
                hum = int(row['humidity'])
                noise = int(row['noise'])
                light = int(row['light']) 
            prev_row = row    
            
    def create_ontology(self):
        kaire_world = World()
        onto = kaire_world.get_ontology("file://model//onto.owl").load()
        df = pd.read_csv(gb.DATASET_PATH+"workers_ds.csv", names=['id','ts_min','ts_max','hr','rmssd','sdrr','stress_index','location_id'],skiprows=1)        
        df_env = pd.read_csv(gb.DATASET_PATH+"environment_ds.csv", names=['location_id','ts_min','ts_max','temperature','humidity','noise','light'],skiprows=1)        
 
        with onto:
            print(onto.search(is_a = onto.Context, type = onto.Context))
            id1 = onto.Identity("Worker1", namespace = onto, hasId = [1],hasWorkplaceId = [2])
            id2 = onto.Identity("Worker2", namespace = onto, hasId = [2],hasWorkplaceId = [2])
            id3 = onto.Identity("Worker3", namespace = onto, hasId = [3],hasWorkplaceId = [3])
            id4 = onto.Identity("Worker4", namespace = onto, hasId = [4],hasWorkplaceId = [3])
            id5 = onto.Identity("Worker5", namespace = onto, hasId = [5],hasWorkplaceId = [4])
            id6 = onto.Identity("Worker6", namespace = onto, hasId = [6],hasWorkplaceId = [4])
            id7 = onto.Identity("Worker7", namespace = onto, hasId = [7],hasWorkplaceId = [4])
            sup = onto.Identity("Supervisor", namespace = onto, hasId = [8],hasWorkplaceId = [5])
            
            loc1 = onto.Location("Warehouse", namespace = onto, hasLocationId = [1])
            loc2 = onto.Location("Sector1", namespace = onto, hasLocationId = [2])
            loc3 = onto.Location("Sector2", namespace = onto, hasLocationId = [3])
            loc4 = onto.Location("AssemblySector", namespace = onto, hasLocationId = [4])
            loc5 = onto.Location("FinalStock", namespace = onto, hasLocationId = [5])
            loc6 = onto.Location("SupervisorRoom", namespace = onto, hasLocationId = [6])
            
            for i,row in df.iterrows():
                individualName = "Context" + str(i)
                if i > 0:
                    worker = onto.Worker(individualName, namespace = onto, hasId = [int(row['id'])], hasTsMin = [int(row['ts_min'])], hasTsMax = [int(row['ts_max'])], hasHR = [float(row['hr'])], hasRMSSD = [float(row['rmssd'])], hasSDRR = [float(row['sdrr'])], hasStressIndex = [int(row['stress_index'])], hasLocationId = [int(row['location_id'])])
            
            for i,row in df_env.iterrows():
                individualName = "EnvContext" + str(i)
                if i > 0:
                    env = onto.Workplace(individualName, namespace = onto, hasLocationId = [int(row['location_id'])], hasTsMin = [int(row['ts_min'])], hasTsMax = [int(row['ts_max'])], hasCelsius = [int(row['temperature'])], hasHumPercent = [int(row['humidity'])], hasDecibels = [int(row['noise'])],hasLux = [int(row['light'])])
            onto_path.append("model/")
            onto.save(file = "model/OntokaireEvaluation_Sim.owl")
                
            self.create_rules()
            
            sync_reasoner_pellet(kaire_world,infer_property_values = True, infer_data_property_values = True, debug = 20)
            
            print('############### SPARQL ###############')
            arr = (list(kaire_world.sparql(gb.CQ7)))
            #print(tabulate(arr,headers=['id','stress','location_id','activity','timestamp','duration','day','hour','hr','rmssd','sdrr','stressor_id','shared_time','env_cond','cond'],tablefmt='github',showindex=False))

            for a in arr:
                with open(gb.DATASET_PATH+"reasoner_ds.csv",'a') as f:
                    f.write(str(a[0]) + "," + str(a[1]) + "," + str(a[2]) + "," + str(a[3]) + "," + str(a[4]) + "," + str(a[5]) + "," + str(a[6]) +  "," + str(a[7]) + "," + str(a[8]) + "," + str(a[9]) + "," + str(a[10]) + "," + str(a[11]).replace("None","0") + "," + str(a[12]).replace("None","0") + "," + str(a[13]).replace("None","0") + "," + str(a[14]).replace("None","0").replace("onto.","") + "\n")
            
            arr = (list(kaire_world.sparql(gb.CQ8)))
            #print(tabulate(arr,headers=['location_id','timestamp','day','hour','id','stress','shared_time'],tablefmt='github',showindex=False))
            for a in arr:
                with open(gb.DATASET_PATH+"group_ds.csv",'a') as f:
                    f.write(str(a[0]) + "," + str(a[1]) + "," + str(a[2]) + "," + str(a[3]) + "," + str(a[4]) + "," + str(a[5]) + "," + str(a[6]) + "\n")
        close_world(onto)
        
    def reasoner(self):
        onto = get_ontology("file://OntokaireEvaluation_Sim.owl").load()
        with onto:
            
            self.create_rules()
            
            sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True, debug = 20)
            prin(list(default_world.inconsistent_classes()))
            
            print('############### SPARQL ###############')
            arr = (list(default_world.sparql(gb.CQ7)))
            #print(tabulate(arr,headers=['id','stress','locationId','activity','timestamp','duration','day','hour','hrv_mean','hrv_sd','stressorId','shared_time','env_cond','cond'],tablefmt='github',showindex=False))

            for a in arr:
                with open(gb.DATASET_PATH+"reasoner_ds.csv",'a') as f:
                    f.write(str(a[0]) + "," + str(a[1]) + "," + str(a[2]) + "," + str(a[3]) + "," + str(a[4]) + "," + str(a[5]) + "," + str(a[6]) +  "," + str(a[7]) + "," + str(a[8]) + "," + str(a[9]) + "," + str(a[10]).replace("None","0") + "," + str(a[11]).replace("None","0") + "," + str(a[12]) + "," + str(a[13]).replace("None","0").replace("onto.","") + "\n")
            
            arr = (list(default_world.sparql(gb.CQ8)))
            #print(tabulate(arr,headers=['locationId','timestamp','day','hour','id','stress','shared_time'],tablefmt='github',showindex=False))
            for a in arr:
                with open(gb.DATASET_PATH+"group_ds.csv",'a') as f:
                    f.write(str(a[0]) + "," + str(a[1]) + "," + str(a[2]) + "," + str(a[3]) + "," + str(a[4]) + "," + str(a[5]) + "," + str(a[6]) + "\n")
        close_world(onto)
        
    def create_rules(self):
        #Rules for Worker
        R_StressedBy = Imp().set_as_rule("""Worker(?c), hasId(?c, ?x), hasId(?s, ?y), notEqual(?x, ?y), hasLocationId(?c, ?l), hasLocationId(?s, ?l), hasTsMin(?c, ?tscmin), hasTsMin(?s, ?tssmin), hasTsMax(?c, ?tscmax), hasTsMax(?s, ?tssmax), greaterThanOrEqual(?tssmax, ?tscmin), lessThanOrEqual(?tssmin, ?tscmax), greaterThan(?l, 0), targets(?s, ?z) -> stressedBy(?c, ?z)""")
        R_Normal = Imp().set_as_rule("""Worker(?c) , hasStressIndex(?c, ?s) , lessThan(?s, 1) -> feels(?c, Normal)""")
        R_Stressed = Imp().set_as_rule("""Worker(?c) , hasStressIndex(?c, ?s) , greaterThanOrEqual(?s, 1) -> feels(?c, Stressed)""")
        R_LocatedAt = Imp().set_as_rule("""Context(?c) , hasLocationId(?c, ?lid) , Location(?l) , hasLocationId(?l, ?lid) -> locatedAt(?c, ?l)""")
        R_PerformsTask = Imp().set_as_rule("""Context(?c) , hasLocationId(?c, ?x) , targetedBy(?i, ?c) , hasWorkplaceId(?i, ?y) , equal(?x, ?y) , greaterThan(?x, 0) -> performs(?c, WorkTask)""")
        R_PerformsMeeting = Imp().set_as_rule("""Context(?c) , hasLocationId(?c, ?x) , targetedBy(?i, ?c) , hasWorkplaceId(?i, ?y) , notEqual(?x, ?y) , greaterThan(?x, 0) -> performs(?c, Meeting)""")
        R_PerformsDisplacement = Imp().set_as_rule("""Context(?c) , hasLocationId(?c, 0) -> performs(?c, Displacement)""")
        R_Targets = Imp().set_as_rule("""Identity(?i) , hasId(?i, ?id) , Worker(?w) , hasId(?w, ?id) -> targets(?w, ?i)""")
        R_StressedByContext = Imp().set_as_rule("""Worker(?c), hasId(?c, ?x), hasId(?s, ?y), notEqual(?x, ?y), hasLocationId(?c, ?l), hasLocationId(?s, ?l), hasTsMin(?c, ?tscmin), hasTsMin(?s, ?tssmin), hasTsMax(?c, ?tscmax), hasTsMax(?s, ?tssmax), greaterThanOrEqual(?tssmax, ?tscmin), lessThanOrEqual(?tssmin, ?tscmax), greaterThan(?l, 0), targets(?s, ?z) -> stressedByContext(?c, ?s)""")
        R_EnvContext = Imp().set_as_rule("""Worker(?c), Workplace(?s), hasLocationId(?c, ?l), hasLocationId(?s, ?l), hasTsMin(?c, ?tscmin), hasTsMin(?s, ?tssmin), hasTsMax(?c, ?tscmax), hasTsMax(?s, ?tssmax), greaterThanOrEqual(?tssmax, ?tscmin), lessThanOrEqual(?tssmin, ?tscmax), greaterThan(?l, 0) -> hasEnvContext(?c, ?s)""")
        
        #Rules for time manipulation
        R_TsMinute = Imp().set_as_rule("""Context(?c) , hasTsMin(?c, ?ts) , mod(?m, ?ts, 60) , subtract(?h, ?ts, ?m) -> hasTsMinute(?c, ?h)""")
        R_TsDate = Imp().set_as_rule("""Context(?c), hasTsMin(?c, ?ts), mod(?m, ?ts, 864000), subtract(?h, ?ts, ?m) -> hasTsDate(?c, ?h)""")
        R_Ts5min = Imp().set_as_rule("""Context(?c), hasTsMin(?c, ?ts), mod(?m, ?ts, 300), subtract(?h, ?ts, ?m) -> hasTs5min(?c, ?h)""")
        R_Hour = Imp().set_as_rule("""Context(?c) , hasTsMin(?c, ?ts) , mod(?m, ?ts, 86400) , integerDivide(?h, ?m, 3600) -> hasHour(?c, ?h)""") 
        R_Weekday = Imp().set_as_rule("""Context(?c), hasTsMin(?c, ?ts), divide(?r, ?ts, 86400), floor(?f, ?r) , add(?a, ?f, 4) , mod(?d, ?a, 7) -> hasWeekday(?c, ?d)""")
        R_Duration = Imp().set_as_rule("""hasTsMax(?c, ?max), hasTsMin(?c, ?min), subtract(?d, ?max, ?min) -> hasDuration(?c, ?d)""")
        
        #Rules for Enviroment
        R_HighTemp = Imp().set_as_rule("""hasCelsius(?c, ?t) , greaterThan(?t, 26) -> hasCondition(?c, HighTemperature)""")
        R_LowTemp = Imp().set_as_rule("""hasCelsius(?c, ?t) , lessThan(?t, 22) -> hasCondition(?c, LowTemperature)""")
        R_HighLight = Imp().set_as_rule("""hasLux(?c, ?l) , greaterThan(?l, 500) -> hasCondition(?c, HighLight)""")
        R_LowLight = Imp().set_as_rule("""hasLux(?c, ?l) , lessThan(?l, 50) -> hasCondition(?c, LowLight)""")
        R_HighHum = Imp().set_as_rule("""hasHumPercent(?c, ?t) , greaterThan(?t, 60) -> hasCondition(?c, HighHumidity)""")
        R_LowHum = Imp().set_as_rule("""hasHumPercent(?c, ?t) , lessThan(?t, 40) -> hasCondition(?c, LowHumidity)""")
        R_HighNoise = Imp().set_as_rule("""hasDecibels(?c, ?t) , greaterThan(?t, 85) -> hasCondition(?c, HighNoise)""")
        R_IrregularCond = Imp().set_as_rule("""Context(?p) , hasNotification(?p, ?n) -> hasCondition(?p, Irregular)""")
        R_Irregular = Imp().set_as_rule("""hasCondition(?w, ?c) , Irregular(?c) -> Irregular(?w)""")
        R_StandardEnv = Imp().set_as_rule("""hasCelsius(?c, ?t) , greaterThanOrEqual(?t, 22) , lessThanOrEqual(?t, 26) , hasHumPercent(?c, ?h) , greaterThanOrEqual(?t, 40) , lessThanOrEqual(?h, 60) , hasDecibels(?c, ?t) , lessThanOrEqual(?t, 85) , hasLux(?c, ?l) , greaterThanOrEqual(?l, 50) , lessThanOrEqual(?l, 500) -> Standard(?c)""")    
