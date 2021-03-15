from PredictiveMigration import PredictiveMigrationServer
import pandas as pd
import numpy as np

n_clients = 1000
serveraddr = ("localhost", 19724)

s = PredictiveMigrationServer(serveraddr[1])
s.simulate(n_clients, 60)