# add a title to the raw csv

import csv

raw_csv_path = "./datasets/raw_data.csv"
addtitle_csv_path = "./datasets/addtitle.csv"

# set title names
header_list = ['Year']
for i in range(1,91):
    header_list.append('attr' + str(i))

# read raw csv and insert title
with open(raw_csv_path, "r") as infile:
    reader = list(csv.reader(infile))
    reader.insert(0, header_list)

with open(addtitle_csv_path, "w") as outfile:
    writer = csv.writer(outfile)
    for line in reader:
        writer.writerow(line)