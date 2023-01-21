import csv
import pandas as pd

def create_csv(csvpath):
    path = csvpath
    with open(path,'wb') as f:
        csv_write = csv.writer(f)
        csv_head = ['good','bad']
        csv_write.writerow(csv_head)

csvpath = "./final/datasets/title.csv"
create_csv(csvpath)