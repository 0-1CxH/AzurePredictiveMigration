#!/usr/bin/env python
# coding: utf-8

# In[21]:


from datetime import datetime, timedelta
import socket
import json
import pickle


# In[137]:


class PredictiveMigrationClient(object):
    machineID = None
    datetime = None
    proba = None
    model = None
    serverAddr = None
    def __init__(self, macid,model_file, serveraddr):
        self.machineID = macid
        f = open(model_file,"rb")
        self.model = pickle.load(f)
        self.serverAddr = serveraddr
    def setTime(self, dt):
        self.datetime = dt
    def sendStatus(self):
        datadict = {'machineID':self.machineID, 'datetime':self.datetime ,"proba":self.proba}
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.connect(self.serverAddr)
        tcp_sock.send( json.dumps(datadict).encode() )
        tcp_sock.close()
        return datadict
    def calculateProba(self, ds):
        self.proba =  list(self.model.predict_proba(ds)[0])
    def simulate(self, dt, ds):
        self.setTime(dt)
        self.calculateProba(ds)
        dd = self.sendStatus()
        print("[Client",self.machineID,dd['datetime'],"] State=", dd['proba'])


# In[ ]:


class PredictiveMigrationServer(object):
    datetime = None
    serverPort = None
    stateDict = {}
    tcp_sock = None
    def __init__(self, serverport):
        self.serverPort = serverport
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_sock.bind(("", self.serverPort))
        self.tcp_sock.listen(128)
    def setTime(self, timestring):
        self.datetime = timestring
    def getStatus(self):
        incoming_sock, client_addr = self.tcp_sock.accept()
        recv_data = incoming_sock.recv(512)
        datadict = json.loads(recv_data)
        incoming_sock.close()
        return datadict
    def simulate_migrate(self):
        good_m = []
        bad_m = []
        for m in self.stateDict:
            if self.stateDict[m]["S"] == 1:
                bad_m.append(m)
            else:
                good_m.append(m)
        if len(bad_m) == 0:
            pass
        else:
            print("[SERVER", self.datetime, "]", "Migrate",bad_m," To ",good_m)
    def simulate(self, n_clients, simulationTime):
        start_time = datetime.now()
        while datetime.now() - start_time <= timedelta(seconds = simulationTime):
            for _ in range(n_clients):
                datadict = self.getStatus()
                self.setTime(datadict['datetime'])
                s_ = 0
                if datadict['proba'][1] > datadict['proba'][0]:
                    s_ =1 
                self.stateDict[datadict['machineID']] = {}
                self.stateDict[datadict['machineID']]['S'] = s_
                self.stateDict[datadict['machineID']]['P'] = datadict['proba'][s_]
            self.simulate_migrate()

