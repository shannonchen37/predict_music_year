# delete the attributes above 12

import csv
import os

addtitle_csv_path = "./datasets/addtitle.csv"
delcol_csv_path = "./datasets/data.csv"

# set the index of columes
cols_to_remove = []
for i in range(13,91):
    cols_to_remove.append(i) # Column indexes to be removed (starts at 0)

cols_to_remove = sorted(cols_to_remove, reverse=True) # Reverse so we remove from the end first
row_count = 0 # Current amount of rows processed

with open(addtitle_csv_path, "r") as source:
    reader = csv.reader(source)
    with open(delcol_csv_path, "w", newline='') as result:
        writer = csv.writer(result)
        for row in reader:
            row_count += 1
            print('\r{0}'.format(row_count), end='') # Print rows processed
            for col_index in cols_to_remove:
                del row[col_index]
            writer.writerow(row)

# remove addtitle csv
cmd = "rm -rf " + addtitle_csv_path
os.system(cmd)