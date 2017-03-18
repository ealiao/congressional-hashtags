# Erica Liao
# Iterate through all tweets + create csv of hashtags w/ their frequencies

import csv
import re

with open('output/tweets_05to10_2016.csv', 'rU') as f:
	reader = csv.reader(f)
	tweets_list = list(reader)

f.close

all_moc = []

def is_moc_in(handle):
	for i, congressmember in enumerate(all_moc):
		if (congressmember[0] == handle):
			return i
	return -1


for tweet in tweets_list:
	if tweet:
		# check if moc is already in list
		index = is_moc_in(tweet[0])
		# if yes add 1 to count, potentially update dates
		# < -- earlier dates are "lower"
		if (index != -1):
			all_moc[index][3] = all_moc[index][3] + 1 # frequency

			if (tweet[2] < all_moc[index][1]):
				all_moc[index][1] = tweet[2] # earliest tweet
			if (tweet[2] > all_moc[index][2]):
				all_moc[index][2] = tweet[2] # latest tweet

		# if no, add to list, add dates
		else:
			moc = [tweet[0], tweet[2], tweet[2], 1]
			all_moc.append(moc)

with open('output/congress_114_timeline.csv', 'w') as output:
	writer = csv.writer(output)
	writer.writerows(all_moc)