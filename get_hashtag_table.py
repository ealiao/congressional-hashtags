# Erica Liao
# For my thesis on how members of congress use hashtags,
# and what this may indicate about party coordination,
# lobbying efforts, and activism.
#
# Here, I am creating a table where rows = each MOC,
# columns are each hashtag, and I am listing how often
# each member of congress uses each hashtag.

import csv
import re

# this file has tweets w/ the format of
# twitter handle, tweet id, date & time, tweet text
with open('output/tweets_05to10_2016.csv', 'rU') as f:
	reader = csv.reader(f)
	tweets_list = list(reader)
f.close

# this file is a list of all hashtags that have been used
# in tweets from the above file (previously extracted in python)
with open('output/hashtags_final.csv', 'rU') as f:
	reader = csv.reader(f)
	hashtag_list = list(reader)
f.close

# this file is a list of the twitter handles of all members of congress
with open('output/congress_114.csv', 'rU') as f:
	reader = csv.reader(f)
	moc_list = list(reader)
f.close

### setting up table /////////////
# 514 membes of congress w/ twitter accounts,
# 7636 hashtags being studied
table = []
new = []
for i in range (0, 514):
    for j in range (0, 7636):
        new.append(0)
    table.append(new)
    new = []
### //////////////////////////////

### create dictionary where key = hashtag, value = hashtag's column index
hashtags = {}
index = 1

for hashtag in hashtag_list:
	if hashtag:
		hashtags[hashtag[0]] = index
		table[0][index] = hashtag[0]
		index = index + 1
### /////////////////////////////////////////////////////////////////////

### create dictionary where key = MOC twitter handle, value = MOC's row
mocs = {}
index = 1

for moc in moc_list:
	if moc:
		mocs[moc[0]] = index;
		table[index][0] = moc[0]
		index = index + 1
### /////////////////////////////////////////////////////////////////////

### get hashtags in tweet list //////////////////////////////////////////
# extracting all hashtags used in a tweet, appending as a list to the tweet
all_tweets = []
for tweet in tweets_list:
	if tweet:
		tweet_text = tweet[3]
		tweet_hashtags = re.findall(r'#\w*', tweet_text)
		tweet[4] = tweet_hashtags
		all_tweets.append(tweet)
### /////////////////////////////////////////////////////////////////////


# iterate through all tweets
for tweet in all_tweets:
	if tweet:
		if tweet[4]:
			# iterate through all hashtags in tweet (if they exist)
			for i, hashtag in enumerate(tweet[4]):
				# because #BLM and #blm have the same meaning,
				# all hashtags standardized to all lowercase
				hashtag_string = tweet[4][i].lower()

				if hashtag_string in hashtags:
					# get hashtag's index from dict,
					# get member of congress' index from dict
					hashtag_index = hashtags[hashtag_string]
					moc_index = mocs[tweet[0]]

					# if there's already a value, increment up
					# otherwise, give value of 1
					if table[moc_index][hashtag_index]:
						table[moc_index][hashtag_index] = table[moc_index][hashtag_index] + 1
					else:
						table[moc_index][hashtag_index] = 1

# write out table to csv file
with open('output/mocs_and_hashtag_counts.csv', 'w') as output:
	writer = csv.writer(output)
	writer.writerows(table)