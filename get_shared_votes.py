# Erica Liao
# calculate how many times each pair of MOCs votes the same way on a bill
# discluding times when they did not vote on the bill
# table set up: (0) moc1 / (1) moc2 / (2) # shared voting behavior instances / (3) # possible shared voting behavior instances

import csv
import re

with open('output/mocs_and_votes.csv', 'rU') as f:
	reader = csv.reader(f)
	votes_list = list(reader)
f.close

### create dictionary where key = MOC bioguide id, value = MOC's row in mocs_and_votes
with open('output/congress_114_bioguideid.csv', 'rU') as f:
	reader = csv.reader(f)
	moc_list = list(reader)
f.close

mocs_dict = {}
index = 1

for moc in moc_list:
	mocs_dict[moc[0]] = index;
	index = index + 1
### ////////////////////////////////////////////////////////////////////////////////////

### setting up table /////////////
table = []
new = []
for i in range (0, 291600):
    for j in range (0, 4):
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

### compare votes for all pairs (duplicates will be dealt with later in R)
for x, pair in enumerate(table):
	shared_votes = 0
	possible_shared_votes = 0

	moc1 = table[x][0]
	moc2 = table[x][1]

	moc1_row = mocs_dict[moc1]
	moc2_row = mocs_dict[moc2]

	# 415 roll call votes
	for vote in range (1, 416):
		# did both of them vote?
		if votes_list[moc1_row][vote] != "-1" and votes_list[moc2_row][vote] != "-1":
			possible_shared_votes = possible_shared_votes + 1
			# did they vote the same way?
			if votes_list[moc1_row][vote] == votes_list[moc2_row][vote]:
				shared_votes = shared_votes + 1

	table[x][2] = shared_votes
	table[x][3] = possible_shared_votes

	# trying to catch errors
	if shared_votes > possible_shared_votes:
		print ("flag!")
		print (moc1)
		print (moc2)

with open('output/mocs_and_shared_votes.csv', 'w') as output:
	writer = csv.writer(output)
	writer.writerows(table)
