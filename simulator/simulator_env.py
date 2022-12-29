import simpy
import random
from datetime import datetime
import pandas as pd
import globals as gb

#-------------------------------------------------

class Industry:
    def __init__(self, env, init_time):
        #time att
        self.init_time = init_time
        self.timestamp = int(round(self.init_time.timestamp()))
        self.timestamp_init = int(round(self.init_time.timestamp()))
        self.simulation_time = init_time
        self.weekday = init_time.weekday()
        
        #indutry att
        self.isOpened = False
        
        #temperature
        self.location1_temp = 24
        self.location2_temp = 24
        self.location3_temp = 24
        self.location4_temp = 24
        self.location5_temp = 24
        self.location6_temp = 24
        
        #humidity
        self.location1_hum = 50
        self.location2_hum = 50
        self.location3_hum = 50
        self.location4_hum = 50
        self.location5_hum = 50
        self.location6_hum = 50
        
        #noise
        self.location1_noise = 60
        self.location2_noise = 60
        self.location3_noise = 60
        self.location4_noise = 60
        self.location5_noise = 60
        self.location6_noise = 60
        
        #light
        self.location1_light = 100
        self.location2_light = 100
        self.location3_light = 100
        self.location4_light = 100
        self.location5_light = 100
        self.location6_light = 100
        
        self.operation_time = env.process(self.operation_time(env))
        self.data_collection = env.process(self.data_collection(env))
        self.temperature_variation = env.process(self.temperature_variation(env))
        
        self.feedstock_1 = simpy.Container(env, capacity = 4000, init = 4000)
        self.feedstock_2 = simpy.Container(env, capacity = 2000, init = 2000)
        self.componenet1_stock = simpy.Container(env, capacity = 4000, init = 0)
        self.componenet2_stock = simpy.Container(env, capacity = 2000, init = 0)
        self.dispatch = simpy.Container(env ,capacity = 1000, init = 0)

    def operation_time(self, env):
        yield env.timeout(0)
        while True:
            ts = self.init_time.timestamp() + env.now
            self.simulation_time = pd.Timestamp(ts, unit='s')
            self.weekday = self.simulation_time.weekday()
            if self.weekday < 5 and self.simulation_time.hour > 7 and self.simulation_time.hour < 19:
                self.isOpened = True
            else:
                self.isOpened = False
            yield env.timeout(300)
            #match self.weekday:
            #    case 0:
            #        print("It's Monday and opened!")
            #    case 1:
            #        print("It's Thuesday!")
            #    case 2:
            #        print("It's Wednesday!")
            #    case 3:
            #        print("It's Thursday!")
            #    case 4:
            #        print("It's Friday!")
            #    case 5:
            #        print("It's Saturday! Industry is closed!")
            #    case 6:
            #       print("It's Sunday! Go to the Mass!")
            #    case _:
            #        print("Something's wrong!")
            
            
    def data_collection(self, env):
        yield env.timeout(300)
        while True:
            ts = env.now + self.timestamp_init
            hour = int((ts % 86400)/3600)
            day = (int(ts / 86400)+4) % 7
            if (hour >=7 and hour <=19) and (day > 0 and day < 6):
                with open(gb.ENV_FILE,'a') as f:
                    self.timestamp = env.now + self.timestamp_init
                    f.write(str(1) + "," + str(env.now + self.timestamp_init) + "," + str(self.location1_temp) + "," + str(self.location1_hum) + "," + str(self.location1_noise) + "," + str(self.location1_light) + "\n")
                    f.write(str(2) + "," + str(env.now + self.timestamp_init) + "," + str(self.location2_temp) + "," + str(self.location2_hum) + "," + str(self.location2_noise) + "," + str(self.location2_light) + "\n")
                    f.write(str(3) + "," + str(env.now + self.timestamp_init) + "," + str(self.location3_temp) + "," + str(self.location3_hum) + "," + str(self.location3_noise) + "," + str(self.location3_light) + "\n")
                    f.write(str(4) + "," + str(env.now + self.timestamp_init) + "," + str(self.location4_temp) + "," + str(self.location4_hum) + "," + str(self.location4_noise) + "," + str(self.location4_light) + "\n")
                    f.write(str(5) + "," + str(env.now + self.timestamp_init) + "," + str(self.location5_temp) + "," + str(self.location5_hum) + "," + str(self.location5_noise) + "," + str(self.location5_light) + "\n")
                    f.write(str(6) + "," + str(env.now + self.timestamp_init) + "," + str(self.location6_temp) + "," + str(self.location6_hum) + "," + str(self.location6_noise) + "," + str(self.location6_light) + "\n")
            yield env.timeout(3600)

    def temperature_variation(self, env):
        yield env.timeout(300)
        while True:
            ts = env.now + self.timestamp_init
            hour = int((ts % 86400)/3600)
            day = (int(ts / 86400)+4) % 7
            if hour <= 14:
                self.location1_temp += random.randrange(0,1)
                self.location2_temp += random.randrange(0,1)
                self.location3_temp += random.randrange(0,1)
                self.location1_hum -= random.randrange(0,1)
                self.location2_hum -= random.randrange(0,1)
                self.location3_hum -= random.randrange(0,1)
            else:
                self.location1_temp -= random.randrange(0,1)
                self.location2_temp -= random.randrange(0,1)
                self.location3_temp -= random.randrange(0,1)
                self.location1_hum += random.randrange(0,1)
                self.location2_hum += random.randrange(0,1)
                self.location3_hum += random.randrange(0,1)
            yield env.timeout(3600)
            
#retirar yield do que não é processo
def quality_assurance(worker,supervisor):
    qa_level = 0.9
    while qa_level < 1:
        qa_level = 1.1
        qa_level = random.gauss(qa_level, 50)
        #supervisor.walk(supervisor.locationId,worker.locationId)
        if qa_level > 1:
            qa_level = 1.1
            worker.ibi_normal()
            worker.stressIndex = 0
            #env.timeout(1200)
        else:
            qa_level = 1.1
            worker.ibi_stress()
            worker.stressIndex = 1
            #env.timeout(1200)
    #supervisor.walk(supervisor.locationId,6)

def component1_process(env, industry, worker, supervisor):
    while True:

        if industry.isOpened:
            worker.walk(1)
            yield industry.feedstock_1.get(1)
            worker.walk(1)
            operation_time = max(random.gauss(1800, 300), 3000)
            industry.location2_noise += min(random.randrange(10,20),80)
            yield env.timeout(operation_time)
            industry.location2_noise -= min(random.randrange(10,20),70)
            quality_assurance(worker, supervisor)
            worker.walk(1)
            yield industry.componenet1_stock.put(1)
            worker.walk(2)
            #print(worker.name + ' made a componenet 1!')
        yield env.timeout(1800)    

def component2_process(env, industry, worker, supervisor):
    while True:
        if industry.isOpened:
            #print('Industry Working {0}'.format(industry.isOpened))
            worker.walk(1)
            yield industry.feedstock_2.get(1)
            worker.walk(3)
            operation_time = max(random.gauss(2500, 500),5000)
            industry.location3_noise +=  min(random.randrange(10,20),80)
            yield env.timeout(operation_time)
            industry.location3_noise -=  min(random.randrange(10,20),70)
            quality_assurance(worker, supervisor)
            worker.walk(1)
            yield industry.componenet2_stock.put(1)
            worker.walk(3)
            #print(worker.name + ' made a componenet 2!')
        yield env.timeout(2500)
        
def assembly_process(env, industry, worker,supervisor):
    while True:
        if industry.isOpened:
            worker.walk(1)
            yield industry.componenet2_stock.get(1)
            yield industry.componenet1_stock.get(2)
            worker.walk(4)
            operation_time = max(random.gauss(3600, 200), 6000)
            yield env.timeout(operation_time)
            quality_assurance(worker, supervisor)
            worker.walk(5)
            yield industry.dispatch.put(1)
            worker.walk(4)
            #print(worker.name + ' finished a product!')
        yield env.timeout(3600)
        
def supervision_process(env, industry, supervisor, workers):
    while True:
        ts = env.now + supervisor.timestamp_init
        hour = int((ts % 86400)/3600)
        day = (int(ts / 86400)+4) % 7
        if (day == 1 and hour == 10 ) or (day ==3 and hour == 14):
            workers[0].walk(6)
            workers[1].walk(6)
            workers[0].ibi_stress()
            workers[0].stressIndex = 1            
            if (day == 1 and hour == 10 ):
                workers[1].ibi_stress()
                workers[1].stressIndex = 1
            operation_time = random.randrange(1800, 3600)
            yield env.timeout(operation_time)
            workers[0].walk(2)
            workers[1].walk(2)
            workers[0].ibi_normal()
            workers[1].ibi_normal()
            workers[0].stressIndex = 0
            workers[1].stressIndex = 0
        if (day == 2 and hour == 10 ) or (day ==4 and hour == 14):
            workers[3].walk(6)
            workers[2].walk(6)
            operation_time = random.randrange(1800, 3600)
            yield env.timeout(operation_time)
            workers[3].walk(3)
            workers[2].walk(3)            
        if (day == 5 and hour == 15 ):
            workers[4].walk(6)
            workers[5].walk(6)
            workers[6].walk(6)
            workers[5].ibi_stress()
            workers[5].stressIndex = 1
            operation_time = random.randrange(1800, 3600)
            yield env.timeout(operation_time)
            workers[4].walk(3)
            workers[5].walk(3)
            workers[6].walk(3)
            workers[5].ibi_normal()
            workers[5].stressIndex = 0
        yield env.timeout(3600)