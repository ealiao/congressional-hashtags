# Erica Liao
# Iterate through all tweets + create csv of hashtags w/ their frequencies

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

all_hashtags = []

# check if a hashtag is already in the array
def is_hashtag_in(hashtag_string):
	for i, hashtag in enumerate(all_hashtags):
		if (hashtag_string == hashtag[0]):
			return i
	return -1

def is_moc_in(handle, index):
	for i, congressmember in enumerate(all_hashtags[index][1]):
		if (handle == congressmember[0]):
			return i
	return -1


for tweet in all_tweets:
	if tweet:
		if tweet[4]:
			for i, hashtag in enumerate(tweet[4]):
				hashtag_string = tweet[4][i]
				
				# check if already in library
				index = is_hashtag_in(hashtag_string)
				if (index != -1):
					#check if member of congress is already in list
					moc_index = is_moc_in(tweet[0], index)

					# if yes add 1 to count
					# if no add to list
					if (moc_index != -1):
						all_hashtags[index][1][moc_index][1] = all_hashtags[index][1][moc_index][1] + 1
					else:
						moc = [tweet[0], 1]
						all_hashtags[index][1].append(moc)

				# if hashtag is not in library
				else:
					moc = [tweet[0], 1]	
					hashtag = [hashtag_string, [moc]]
					all_hashtags.append(hashtag)

with open('output/hashtags.csv', 'w') as output:
	writer = csv.writer(output)
	writer.writerows(all_hashtags)