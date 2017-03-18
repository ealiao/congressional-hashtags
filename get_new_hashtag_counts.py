# Erica Liao
# Iterate through all tweets + create csv of hashtags w/ their frequencies

import csv
import re

with open('output/tweets_05to10_2016.csv', 'rU') as f:
	reader = csv.reader(f)
	tweets_list = list(reader)

f.close

all_tweets = []

for tweet in tweets_list:
	if tweet:
		tweet_text = tweet[3]
		tweet_hashtags = re.findall(r'#\w*', tweet_text)
		tweet[4] = tweet_hashtags
		all_tweets.append(tweet)

all_hashtags = {}

for tweet in all_tweets:
	if tweet:
		if tweet[4]:
			for i, hashtag in enumerate(tweet[4]):
				hashtag_string = tweet[4][i].lower()

				# check if already in library
				if hashtag_string in all_hashtags:
					# if yes add 1 to count
					all_hashtags[hashtag_string] = all_hashtags[hashtag_string] + 1

				# if hashtag is not in library
				else:
					all_hashtags[hashtag_string] = 1

hashtag_table = []

for (k,v) in all_hashtags.items():
	temp = [k, v]
	hashtag_table.append(temp)

with open('output/hashtags_new_count.csv', 'w') as output:
	writer = csv.writer(output)
	writer.writerows(hashtag_table)