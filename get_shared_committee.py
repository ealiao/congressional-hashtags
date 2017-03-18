# Erica Liao
# calculate how many committees MOCs share

import csv
import re

with open('output/mocs_and_comms.csv', 'rU') as f:
	reader = csv.reader(f)
	comms_list = list(reader)
f.close

### create dictionary where key = MOC bioguide id, value = MOC's row in mocs_and_comms
with open('output/congress_114_bioguideid.csv', 'rU') as f:
	reader = csv.reader(f)
	moc_list = list(reader)
f.close

mocs_dict = {}
index = 1

for moc in moc_list:
	mocs_dict[moc[0]] = index;
	index = index + 1
### ///////////////////////////////////////////////////////////////////////////////////

### setting up table /////////////
table = []
new = []
for i in range (0, 291600):
    for j in range (0, 3):
        new.append(0)
    table.append(new)
    new = []
### //////////////////////////////

### fill in table with pairs ////////////////////
count = 0

for moc1 in moc_list:
	for moc2 in moc_list:
		table[count][0] = moc1[0]
		table[count][1] = moc2[0]
		count = count + 1
### /////////////////////////////////////////////

### compare comms for all pairs (duplicates will be dealt with later in R)
for x, pair in enumerate(table):
	shared_comms = 0

	moc1 = table[x][0]
	moc2 = table[x][1]

	moc1_row = mocs_dict[moc1]
	moc2_row = mocs_dict[moc2]

	# 215 committees
	for comm in range (1, 216):

		# both in committee?
		if comms_list[moc1_row][comm] == "1" and comms_list[moc2_row][comm] == "1":
			shared_comms = shared_comms + 1
			print (shared_comms)

	table[x][2] = shared_comms


with open('output/mocs_and_shared_comms.csv', 'w') as output:
	writer = csv.writer(output)
	writer.writerows(table)
