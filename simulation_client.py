from PredictiveMigration import PredictiveMigrationClient
import pandas as pd
import numpy as np

n_clients = 100
test_case = 10
sample_file = "simulationp1.csv"
model_file = "PredictiveMigration.pkl"
serveraddr = ("localhost", 19724)

c = []
sim_src = []
for i in range(n_clients):
    sim_src.append(pd.read_csv(sample_file).drop(columns=['Unnamed: 0',"maint"]).sample(n=test_case))
    c.append(PredictiveMigrationClient(i, model_file,serveraddr))

date_case = pd.date_range(start="2020-01-01", periods=test_case, freq="1D")


def clients_send(test_case):
    for i in range(test_case):
        for c_num  in range(n_clients):
            c[c_num].simulate(str(date_case[i]),[sim_src[c_num].iloc[i]])

clients_send(test_case)