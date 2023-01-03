from datetime import date, datetime, timedelta
import pandas as pd
import numpy
import random
import sys

sys.path.insert(0, 'model')
sys.path.insert(1, 'simulator')
import globals as gb
import prediction as p
import ontology as o
import simulator as s
import ontology_wesad as w
import advisor as a
import stressor_identifier as si

def __init__():
    ini = int(pd.Timestamp.now().timestamp())
    print(ini)
    #simulation()
    simulator = s.Simulator()
    simulator.data_training()
    simulator.data_prediction()
    simulator.data_gsi_sim()
    prediction()
    #test()
    identifier = si.StressorIdentifier()
    identifier.calculate_gsi()
    end = int(pd.Timestamp.now().timestamp())
    total = end - ini
    print("\nRuntime: " + str(total) + "seconds or " + str(int(total/60)) + " minutes! \n")


def test():
    z = p.Predictor()
    z.line_graph_feat()
    
def simulation():
    simulator = s.Simulator()
    simulator.reset_files()          
    for d in range(3):
        simulator.init_time = pd.Timestamp(datetime(2022, d+1, 1))
        simulator.env()
        simulator.run()
        onto = o.OntoKaire()
        onto.init_dataset()
        onto.compose_dataset()
        onto.compose_envdataset()
        onto.create_ontology()
       # o.OntoKaire().reasoner()
    simulator.remove_duplicates()
    simulator.data_training()
    simulator.data_prediction()


def prediction():
    z = p.Predictor()
    #z.line_graph()
    #print("#### Non Standardized Identification\n")
    #z.init_dataset()
    #z.reduce_dimension()
    ##z.loocv_predict()
    #z.split_dataset(0.3)
    #z.svm_predict()
    #z.rf_predict()
    #z.show_metrics()
    #z.show_graph_nonstd()
    #
    #print("#### Standardized Identification\n")
    #z.init_dataset()
    #z.standardize()
    #z.reduce_dimension()
    #z.split_dataset(0.3)
    #z.svm_predict()
    #z.rf_predict()
    #z.show_metrics()
    #z.show_graph_std()
    #
    #z.show_confusion_matrix()
    #z.show_probability()

    print("#### Non Standardized Prediction\n")
    z.init_dataset_prediction()
    z.reduce_dimension()
    #z.loocv_predict()
    z.split_dataset(0.3)
    z.svm_predict()
    z.rf_predict()
    z.show_metrics()
    z.show_graph_nonstd()
    
    print("#### Standardized Prediction\n")
    z.init_dataset_prediction()
    z.standardize()
    z.reduce_dimension()
    z.split_dataset(0.3)
    z.svm_predict()
    z.rf_predict()
    z.show_metrics()
    z.show_graph_std()
    z.show_confusion_matrix()
    #advisor = a.Advisor()
    #advisor.prediction()
    #advisor.notification()
    #identifier = si.StressorIdentifier()
    #identifier.classification()
    #identifier.notification()
    #identifier.show_gsi()
    

def create_envds_wesad():    
    with open("C:\\OneDrive\\Estudos\\Mestrado\\Dissertation\\Code\\Data\\evaluation_envds.csv",'w') as f:
        f.write("locationId,ts_min,ts_max,temperature,humidity,noise,light\n")
    arr_days = []
    arr_days.append(pd.Timestamp(datetime(2017, 5, 22)))
    arr_days.append(pd.Timestamp(datetime(2017, 5, 24)))
    arr_days.append(pd.Timestamp(datetime(2017, 6, 13)))
    arr_days.append(pd.Timestamp(datetime(2017, 6, 14)))
    arr_days.append(pd.Timestamp(datetime(2017, 7, 6)))
    arr_days.append(pd.Timestamp(datetime(2017, 7, 10)))
    arr_days.append(pd.Timestamp(datetime(2017, 7, 11)))
    arr_days.append(pd.Timestamp(datetime(2017, 7, 25)))
    arr_days.append(pd.Timestamp(datetime(2017, 8, 8)))
    arr_days.append(pd.Timestamp(datetime(2017, 8, 9)))
    arr_days.append(pd.Timestamp(datetime(2017, 8, 10)))
    arr_days.append(pd.Timestamp(datetime(2017, 8, 11)))
    
    
    for d in arr_days:
        for y in range(5):
            ts_min = int(d.timestamp()) + (3600*(7))
            ts_max = int(d.timestamp()) + (3600*(19)) - 1
            print(str(ts_min) + " - " + str(ts_max))
            temp = random.randrange(20,25)
            hum = random.randrange(40,65)
            noise = random.randrange(60,100)
            light = random.randrange(100,200)
            with open("C:\\OneDrive\\Estudos\\Mestrado\\Dissertation\\Code\\Data\\evaluation_envds.csv",'a') as f:
                f.write(str(int(y+1)) + "," + str(ts_min) + "," + str(ts_max) + "," + str(temp) + "," + str(hum) + "," + str(noise) + "," + str(light) + "\n")
                    
        print("Done")     

def ontology_wesad():
    wesad = w.OntoWesad()
    wesad.compose_dataset()
    wesad.compose_envdataset()
    wesad.create_ontology()
    
__init__()