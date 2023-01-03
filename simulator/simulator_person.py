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
        self.rr_std = rnd.randrange(650,700)
        self.rr_min = gb.RR_MIN_NORMAL
        self.rr_max = gb.RR_MAX_NORMAL
        self.hr = round(60/(self.rr_std/1000),2)
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
                    f.write(str(self.id) + "," + str(env.now + self.timestamp_init) + "," + str(self.hr) + "," + str(self.rmssd) + "," + str(self.sdrr) + "," + str(self.stressIndex) + "," + str(self.locationId) + "\n")                  
                if self.id == 1:
                    with open(gb.DATASET_PATH+"line_ds.csv",'a') as f:
                        f.write(str(self.id) + "," + str(self.stressIndex) + "," + str(env.now + self.timestamp_init) + "," + str(self.hr) + "," + str(self.rmssd) + "," + str(self.sdrr) + "," + str(self.rr) + "\n")                  
            if (hour >=7 and hour <=19) and (day > 0 and day < 6):
                yield env.timeout(300)
            else:
                yield env.timeout(3600)
    
    def rr_stress(self):
        self.rr_min = gb.RR_MIN_STRESS
        self.rr_max = gb.RR_MAX_STRESS
        self.stressIndex = 1
        
    def rr_normal(self):
        self.rr_min = gb.RR_MIN_NORMAL
        self.rr_max = gb.RR_MAX_NORMAL
        self.stressIndex = 0
        
    def heart_rate_variance(self, env):
        while True:
            remainder = counter = t = rr_prev = rr_curr = rr_mean = sd_mean = 0
            rr_list = []
            
            while t < 300:
                if remainder > 0:
                    t += remainder
                    remainder = 0
                if rr_curr == 0:
                    rr_curr = self.rr_std
                else:
                    rr_curr = rnd.randrange(self.rr_min,self.rr_max)
                    rr_mean += ((rr_prev - rr_curr) ** 2) 
                t += (rr_curr/1000)
                self.hr = int(round(60/(rr_curr/1000),0))
                self.rr = rr_curr
                rr_prev = rr_curr
                rr_list.append(rr_curr)
                counter += 1
            
            self.rmssd = round(math.sqrt(rr_mean/(len(rr_list)-1)),3)
            rr_mean = sum(rr_list) / len(rr_list)
            for rr in rr_list:
                sd_mean += ((rr - rr_mean) ** 2)
            self.sdrr = round(math.sqrt(sd_mean/len(rr_list)),3)
            remainder = counter - 300
            ts = env.now + self.timestamp_init
            day = (int(ts / 86400)+4) % 7
            hour = int((ts % 86400)/3600)
            if (self.id == 3 and self.locationId == 3 and (hour <= 9) and (day == 2 or day == 5)):
                self.rr_stress()
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
        self.locationId = destiny
        return walking_time
