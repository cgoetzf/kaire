import random as rnd
import math
import globals as gb

class Person:

    def __init__(self, env, init_time, id, name, age, locationId):
        self.init_time = init_time
        self.timestamp = int(round(self.init_time.timestamp()))
        self.timestamp_init = int(round(self.init_time.timestamp()))
        self.id = id
        self.name = name
        self.age = age
        self.steps = 0
        self.locationId = locationId        
        self.stressIndex = 0
        self.rmssd = rnd.randrange(42,50)
        self.sdrr = rnd.randrange(42,50)
        self.rr = rnd.randrange(42,50)
        self.ibi_std = rnd.randrange(650,700)/1000
        self.ibi_min = gb.IBI_MIN_NORMAL
        self.ibi_max = gb.IBI_MAX_NORMAL
        self.hr = round(60/self.ibi_std,2)
        self.data_collection = env.process(self.data_collection(env))
        self.heart_rate_variance = env.process(self.heart_rate_variance(env))
        
    def data_collection(self, env):
        yield env.timeout(300)
        while True:
            
            ts = env.now + self.timestamp_init
            hour = int((ts % 86400)/3600)
            day = (int(ts / 86400)+4) % 7
            if (hour >=8 and hour <=18) and (day > 0 and day < 6):
                with open(gb.WORKERS_FILE,'a') as f:
                    f.write(str(self.id) + "," + str(env.now + self.timestamp_init) + "," + str(self.rmssd) + "," + str(self.stressIndex) + "," + str(self.locationId) + "\n")                  
                if self.id == 1:
                    with open(gb.DATASET_PATH+"line_ds.csv",'a') as f:
                        f.write(str(self.id) + "," + str(self.stressIndex) + "," + str(env.now + self.timestamp_init) + "," + str(self.hr) + "," + str(self.rmssd) + "," + str(self.sdrr) + "," + str(self.rr) + "\n")                  
            if (hour >=7 and hour <=19) and (day > 0 and day < 6):
                yield env.timeout(300)
            else:
                yield env.timeout(3600)
    
    def ibi_stress(self):
        self.ibi_min = gb.IBI_MIN_STRESS
        self.ibi_max = gb.IBI_MAX_STRESS
    
    def ibi_normal(self):
        self.ibi_min = gb.IBI_MIN_NORMAL
        self.ibi_max = gb.IBI_MAX_NORMAL
        
    def heart_rate_variance(self, env):
        while True:
            remainder = counter = t = ibi_prev = ibi_curr = ibi_mean = 0
            while t < 300:
                if remainder > 0:
                    t += remainder
                    remainder = 0
                if ibi_curr == 0:
                    ibi_curr = self.ibi_std
                else:
                    ibi_curr = rnd.randrange(self.ibi_min,self.ibi_max)/1000
                    ibi_mean += ((ibi_prev - ibi_curr) ** 2) 
                t += ibi_curr
                self.hr = int(round(60/ibi_curr,0))
                self.rr = ibi_curr
                ibi_prev = ibi_curr
                counter += 1
            self.rmssd = round(math.sqrt(ibi_mean/counter),3)
            self.sdrr = ibi_mean
            remainder = counter - 300
            ts = env.now + self.timestamp_init
            day = (int(ts / 86400)+4) % 7
            hour = int((ts % 86400)/3600)
            if (hour >=7 and hour <=19) and (day > 0 and day < 6):
                yield env.timeout(1)
            else:
                yield env.timeout(3600)
                
    def walk(self, destiny):
        step = 0.82
        total_steps = 0
        walking_time = 0
        avg_distance = 0
        if self.locationId == 2:
            if destiny == 1:
                avg_distance = 14.5
            elif destiny == 3:
                avg_distance = 18.7
        elif self.locationId == 3:
            if destiny == 2:
                avg_distance = 18.7
            elif destiny == 4:
                avg_distance = 20.75
        elif self.locationId == 4:
            if destiny == 3:
                avg_distance = 20.75
            elif destiny == 5:
                avg_distance = 22.5
        elif self.locationId == 5:
            if destiny == 4:
                avg_distance = 22.5
            elif destiny == 6:
                avg_distance = 21.25
        elif self.locationId == 6:
            if destiny == 5:
                avg_distance = 21.25
        else:
            avg_distance = 0
        total_steps = int(avg_distance / step)
        self.steps += total_steps
        walking_time = int(rnd.gauss((total_steps * 10), 0.2))
        self.locationId = 0
        self.locationId = destiny
        return walking_time
