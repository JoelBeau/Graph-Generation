import csv
import os
import pandas as pd
import numpy as np

data_file_path = './data/'

for file in os.listdir(data_file_path):
    if file is not "original.csv":
        df = pd.read_csv(data_file_path + file)


