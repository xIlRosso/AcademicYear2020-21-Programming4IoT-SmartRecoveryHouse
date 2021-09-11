from Sens_Temp import *
from Sens_Weight import *
from Sens_HR_OS import *
from Curves import *
from mqtt_methods.mqtt_methods import Subscribers
import json
import requests
import time

if __name__ == '__main__':
    

    S=Subscribers("Beacon_Capture1234", 
    "programming_for_iot/aa2021/SmartRecoveryHouse/catalog_public_address",
    "broker.hivemq.com",
    1883, 0
    )
    i=0
    while i<10:
        S.start()
        time.sleep(4)
        S.stop()
        i+=2

    with open("Patient Sensors - Simulation/catalog_url.json") as json_in:
    # with open("catalog_url.json") as json_in: 
        dat=json.load(json_in)
        catalog_address=dat["url_catalog"]

    r = requests.get(catalog_address+"/sensor/patient")

    conf = r.json()

    r = requests.get(catalog_address+"/telegram_bot/simulation_values")

    conf_sim = r.json()
    # temperature
    
    broker = conf["broker"]
    port = conf["port"]
    msg_temp = conf["devicesList"][0]
    topic_temp = conf["Topics_List"][0]

    
    # "r - Normal [36.5 ; 37.5]"
    # "l - Low Temp [< 35]"
    # "h - High Temp [> 40]"


    sim_t = Simulation(36.5,37.5)

    if conf_sim["Temp_sim"] == "r":
        c = conf_sim["Temp_status"]
        sim_t.Norm_Temp(c)
    elif conf_sim["Temp_sim"] == "l":
        sim_t.Low_Temp()    
    elif conf_sim["Temp_sim"] == "h":
        sim_t.High_Temp()

    myPubl_temp = myPublisher_temp("SRH_SensTemp", topic_temp, broker, port, msg_temp)  


    # weight

    msg_weight = conf["devicesList"][2]
    topic_weight = conf["Topics_List"][2]
    
    # print("What case do you want to apply?")
    # print("r - Normal [62 ; 62.5]")
    # print("l - Low Weight [< 62]")
    # print("h - High Weight [> 62.5]\n")

    weight_patient = float(conf_sim["Weight"])

    sim_w = Simulation(weight_patient - 0.25,weight_patient + 0.25)

    if conf_sim["Weight_sim"] == "r":
        sim_w.Norm_Weig()
    elif conf_sim["Weight_sim"] == "l":
        sim_w.Low_Weig()    
    elif conf_sim["Weight_sim"] == "h":
        sim_w.High_Weig()

    myPubl_weight = myPublisher_weight("SRH_SensWeight", topic_weight, broker, port, msg_weight)    


    # heart rate

    msg_HR = conf["devicesList"][1]
    topic_HR = conf["Topics_List"][1]
    
    # print("What case do you want to apply?")
    # print("r - Rest [60 ; 75]")
    # print("l - Low Heart Rete [55 ; 75]")
    # print("h - High Heart Rate [60 ; 100]\n")

    sim_hr = Simulation(60,75)

    if conf_sim["HR_sim"] == "r":
        sim_hr.Rest_HR()
    elif conf_sim["HR_sim"] == "l":
        c = conf_sim["HR_status"]
        sim_hr.Low_HR(c)    
    elif conf_sim["HR_sim"] == "h":
        c = conf_sim["HR_status"]
        sim_hr.High_HR(c)



    # print("What case do you want to apply?")
    # print("r - Normal [95 ; 100]")
    # print("l - Low Oxygen [< 95]")
    # print("h - Extreme Low Oxygen [< 85]\n")


    sim_hr = Simulation(95,100)
    cmd = 'r'
    if cmd == "r":
        sim_hr.Norm_OS()
    elif cmd == "l":
        sim_hr.Low_OS()    
    elif cmd == "h":
        sim_hr.Dang_OS()

    y = sim_hr.sf

    myPubl_HR = myPublisher_HR("SRH_SensHR_OS", topic_HR, broker, port, msg_HR)


    # start publishers
        
    myPubl_temp.start()
    myPubl_weight.start()
    myPubl_HR.start()

    count = 0

    values = {
        "Temp" : 0,
        "HeartR" : 0,
        "Weight" : 0
    }     

    alarms = {
        "Temp" : 0,
        "HeartR" : 0,
        "Weight" : 0
    }        

    for i,j,m in zip(sim_t.sf, sim_w.sf, sim_hr.sf):

        myPubl_temp.publish(i)
        time.sleep(20)

        myPubl_weight.publish(j)
        time.sleep(20)

        myPubl_HR.publish(m,200)

        time.sleep(20)

        values["Temp"] = i
        values["HeartR"] = m
        values["Weight"] = j

        requests.post(catalog_address+"/last_patient_measurement", json=values)

        if i > 41.0:
            alarms["Temp"] = 1
        elif i < 34.7:
            alarms["Temp"] = 2
        else:
            alarms["Temp"] = 0

        if j > (weight_patient + 1.05):
            alarms["Weight"] = 1
        elif j < (weight_patient + 1.25):
            alarms["Weight"] = 2
        else:
            alarms["Weight"] = 0

        if m > 96.0:
            alarms["HeartR"] = 1
        elif m < 59.0:
            alarms["HeartR"] = 2  
        else:
            alarms["HeartR"] = 0       
        
        requests.post(catalog_address+"/alarm_patient", json=values)
        


    myPubl_temp.stop()
    myPubl_weight.stop()
    myPubl_HR.stop()