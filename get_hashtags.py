# Erica Liao
# Extract hashtags

import csv
import re

with open('output/tweets.csv', 'rU') as f:
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


with open('output/tweets_hashtags.csv', 'w') as output:
	writer = csv.writer(output)
	writer.writerows(all_tweets)
