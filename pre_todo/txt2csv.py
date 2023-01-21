# read txt and transfor to csv 

import csv

raw_csv_path = "./datasets/raw_data.csv"
raw_txt_path = "./datasets/YearPredictionMSD.txt"

csvFile = open(raw_csv_path,'w',newline='',encoding='utf-8')
writer = csv.writer(csvFile)
csvRow = []

f = open(raw_txt_path,'r',encoding='GB2312')
for line in f:
    csvRow = line.split(',')
    writer.writerow(csvRow)

f.close()
csvFile.close()