# Erica Liao
# Based off code by github/yanofsky & Darren M. Stevenson 

import tweepy
import json
import csv
import time

#Twitter API credentials / Erica
consumer_key = "7b09eN08wijLD02bPG6A2tKTX"
consumer_secret = "LAM67XkZEnmNtwxQcAcKLH7P1HWUYyPfWX3wbUjwBtfQqC9EzX"
access_key = "1938504912-8mBGuypIUxzakzY7w4fcLsZmmDm68caFInINZFc"
access_secret = "DFTWLnTvxMqbQDv9JIb9eTkqUGF9B3a44F6Ncmdy6fJLZ"

# list of twitter handles
with open('congress_114_twitter.csv', 'rU') as f:
	reader = csv.reader(f)
	usernames_list = list(reader)

# prevent program from failing if there are no urls in the text of the tweet
# needed because if no urls in tweet text, API returns empty list for entities['urls']
def get_urls(tweet):
	try:
		expanded = tweet.entities['urls'][0]['expanded_url'].encode('utf-8')
	except:
		expanded = None
	return expanded
	

def get_all_tweets(current_username):

	#Twitter only allows access to a users most recent 3200 tweets with this method

	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	#initialize a list to hold all the tweepy Tweets
	alltweets = []	

	#make initial request for most recent tweets (180 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = current_username,count=200)		
	
	#save most recent tweets
	alltweets.extend(new_tweets)

	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1

	#keep grabbing tweets until there are no tweets left to grab	
	while len(new_tweets) > 0:
		print ("getting tweets before")
		print (oldest)
	
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = current_username,count=200,max_id=oldest)
	
		#save most recent tweets
		alltweets.extend(new_tweets)
	
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
	
		print ("... %s tweets downloaded so far" % len(alltweets))
		
		print ('sleeping now...')
		time.sleep(5) #turn this on when running full list, as you get 300 api.friends_ids requests every 15 min
		
	# output data from Twitter API to a few files
	
	# tweepy api is returning "a list of status objects"
	# serialize that list of objects (full contents from the API)
	# and write this to a file for later analysis

	#create a json file of all API data, to use for further analysis later on
	json_str = [json.dumps(tweet._json) for tweet in alltweets]
	with open('output/tweets_full_json/%s.json' % current_username, 'a+') as f:
		for item in json_str:
			f.write(item+'\n')

	f.close
	print ("sleeping now...")
	time.sleep(5) #turn this on when running full list, as you get 300 api.friends_ids requests every 15 min

	#now we focus in on saving just a few fields rather than all the data returned by the API
	
	#transform the tweepy tweets into a 2D array that will populate the csv in file 4
	outtweets = [[current_username, tweet.id_str, tweet.created_at, tweet.text.encode('utf-8'), get_urls(tweet)] for tweet in alltweets]

	#write the csv, which contains only a few of the fields fields from the complete API data
	with open('output/tweets_output.csv', 'a+') as f_csv:
		writer = csv.writer(f_csv)
		writer.writerows(outtweets)


#now that we defined some stuff above, this loop iterates through the list of usernames and completes the API request, storing the data, for each user name	
for list in usernames_list:
	current_username = list[0]
	print ('\n'+'\n'+'currently gathering tweets for: %s' % current_username)
	get_all_tweets(current_username)
