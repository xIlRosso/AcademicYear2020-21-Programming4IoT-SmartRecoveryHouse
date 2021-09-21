from MyMQTT import *
from Curves import *
from mqtt_methods.mqtt_methods import Subscribers
import json, requests, time, os

class myPublisher():
    def __init__(self, clientID, topic, broker, port, msg):
        self.client = MyMQTT(clientID, broker, port, self)
        self.name = clientID
        self.topic = topic
        self.status = None
        self.__message = msg

    def start(self):
        self.client.start()

    def stop(self):
        self.client.stop()

    def publish(self, value):
        message = self.__message
        message["e"][0]["v"] = value
        message["e"][0]["t"] = str(time.time())
        self.client.myPublish(self.topic, message)

if __name__ == '__main__':
    

    with open("Patient Sensors - Simulation/catalog_mqtt_settings.json","r") as json_in:
        setsCatalog = json.load(json_in)

    S=Subscribers(setsCatalog["ID"], setsCatalog["topic"], setsCatalog["broker"], setsCatalog["port"])
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

    r = requests.get(catalog_address+"/sensors/patient")

    conf = r.json()

    i=0

    alarmValues = {
        "normal" : "",
        "higher" : "",
        "lower" : "",
    }    

    while i<1000:
        f = requests.get(catalog_address+"/sensors/bodydevices_list") # get the list of houses
        devs = f.json()

        sim_t = []
        sim_w = []
        sim_hr = []
        for sensors in devs:
            
            for sensor in sensors:
                r = requests.get(catalog_address+"/sensors/sim_values/"+sensor["patientID"])
                conf_sim = r.json()

                if sensor["e"][0]["n"]=="temperature":
                    sim_t = Simulation(sensor["simThresholds"]["temperatureLow"],sensor["simThresholds"]["temperatureHigh"])
                    for sim in conf_sim:
                        if sim["sensorName"] == "temperature":
                            if sim["typeSim"] == "r":
                                c = sim["statusSim"]
                                sim_t.Norm_Temp(c)
                            elif sim["typeSim"] == "l":
                                sim_t.Low_Temp()
                            elif sim["typeSim"] == "h":
                                sim_t.High_Temp()
                elif sensor["e"][0]["n"]=="weight":
                    sim_w = Simulation(sensor["simThresholds"]["weightLow"],sensor["simThresholds"]["weightHigh"])
                    for sim in conf_sim:
                        if sim["sensorName"] == "weight":
                            if sim["typeSim"] == "r":
                                sim_w.Norm_Weig()
                            elif sim["typeSim"] == "l":
                                sim_w.Low_Weig()    
                            elif sim["typeSim"] =="h":
                                sim_w.High_Weig()
                elif sensor["e"][0]["n"]=="heartrate":
                    sim_hr = Simulation(sensor["simThresholds"]["heartrateLow"],sensor["simThresholds"]["heartrateHigh"])            
                    for sim in conf_sim:
                        if sim["sensorName"] == "heartrate":                    
                            if sim["typeSim"] == "r":
                                sim_hr.Rest_HR()
                            elif sim["typeSim"] == "l":
                                c = sim["statusSim"]
                                sim_hr.Low_HR(c)    
                            elif sim["typeSim"] == "h":
                                c = sim["statusSim"]
                                sim_hr.High_HR(c)

                myPubl = myPublisher("SRH_body"+sensor["e"][0]["n"]+str(i), sensor["topic"], conf["broker"], conf["port"],sensor)    
                myPubl.start()
               

                if sensor["e"][0]["n"]=="temperature":
                    if sensor["timesVisited"]==len(sim_t.sf)-1:
                        sensor["timesVisited"]=0
                    myPubl.publish(sim_t.sf[sensor["timesVisited"]])
                    sensor["e"][0]["v"]=sim_t.sf[sensor["timesVisited"]]
                    sensor["timesVisited"]+=1
                    if sim_t.sf[sensor["timesVisited"]] > sensor["alarmThresholds"]["temperatureHigh"]:
                        alarmValues["higher"] = sensor["e"][0]["n"]
                    elif sim_t.sf[sensor["timesVisited"]] < sensor["alarmThresholds"]["temperatureLow"]:
                        alarmValues["lower"] = sensor["e"][0]["n"]
                    else:
                        alarmValues["normal"] = sensor["e"][0]["n"]
                    
                    
                elif sensor["e"][0]["n"]=="weight":
                    if sensor["timesVisited"]==len(sim_w.sf)-1:
                        sensor["timesVisited"]=0
                    myPubl.publish(sim_w.sf[sensor["timesVisited"]])
                    sensor["e"][0]["v"]=sim_w.sf[sensor["timesVisited"]]
                    sensor["timesVisited"]+=1
                    if sim_w.sf[sensor["timesVisited"]] > sensor["alarmThresholds"]["weightHigh"]:
                        alarmValues["higher"] = sensor["e"][0]["n"]
                    elif sim_w.sf[sensor["timesVisited"]] < sensor["alarmThresholds"]["weightLow"]:
                        alarmValues["lower"] = sensor["e"][0]["n"]
                    else:
                        alarmValues["normal"] = sensor["e"][0]["n"]         
                    

                elif sensor["e"][0]["n"]=="heartrate":
                    if sensor["timesVisited"]==len(sim_hr.sf)-1:
                        sensor["timesVisited"]=0
                    myPubl.publish(sim_hr.sf[sensor["timesVisited"]])
                    sensor["e"][0]["v"]=sim_hr.sf[sensor["timesVisited"]]
                    sensor["timesVisited"]+=1
                    if sim_hr.sf[sensor["timesVisited"]] > sensor["alarmThresholds"]["heartrateHigh"]:
                        alarmValues["higher"] = sensor["e"][0]["n"]
                    elif sim_hr.sf[sensor["timesVisited"]] < sensor["alarmThresholds"]["heartrateLow"]:
                        alarmValues["lower"] = sensor["e"][0]["n"]
                    else:
                        alarmValues["normal"] = sensor["e"][0]["n"] 
                    

                time.sleep(20)

                #do a put request to update the timesVisited value
                times_dict = {
                    "timesVisited" : sensor["timesVisited"]
                }

                requests.put(catalog_address + "/sensors/updateTimeVisited/"+sensor["patientID"]+"/"+sensor["e"][0]["n"], json = times_dict)

                requests.put(catalog_address + "/sensors/alarm_patient/"+sensor["patientID"]+"/"+sensor["e"][0]["n"], json = alarmValues)

                requests.post(catalog_address + "/updateSens/body/" + sensor["patientID"], json=sensor)

                myPubl.stop()    
                print("Computing and publishing the next body sensor")


        time.sleep(1)

"""for i,j,m in zip(sim_t.sf, sim_w.sf, sim_hr.sf):

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
    myPubl_HR.stop() """