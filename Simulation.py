#!/usr/bin/env python
# coding: utf-8

# In[1]:


from PredictiveMigration import PredictiveMigrationServer, PredictiveMigrationClient
import pandas as pd
import numpy as np


# In[2]:


import _thread


# In[17]:


n_clients = 10
test_case = 100
sample_file = "simulation2.csv"
model_file = "PredictiveMigration.pkl"
serveraddr = ("localhost", 19723)


# In[18]:


s = PredictiveMigrationServer(serveraddr[1])

c = []
sim_src = []
for i in range(n_clients):
    sim_src.append(pd.read_csv(sample_file).drop(columns=['Unnamed: 0',"maint"]).sample(n=test_case))
    c.append(PredictiveMigrationClient(i, model_file,serveraddr))

date_case = pd.date_range(start="2020-01-01", periods=test_case, freq="1D")


# In[19]:


def clients_send(test_case):
    for i in range(test_case):
        for c_num  in range(n_clients):
            c[c_num].simulate(str(date_case[i]),[sim_src[c_num].iloc[i]])


# In[20]:


_thread.start_new_thread( s.simulate, (n_clients, 60) )
_thread.start_new_thread(clients_send, (test_case,))


# In[ ]:




