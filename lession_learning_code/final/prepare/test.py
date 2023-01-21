import csv
import pandas as pd

csv_path = './final/datasets/test.csv'

header_list = ['Year']
for i in range(1,91):
    header_list.append('arrt' + str(i))

with open(csv_path, 'w', newline='') as f:
    movies = csv.writer(f)
    movies.writerow(header_list)