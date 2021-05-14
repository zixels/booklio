# Gets userScreenName of a batch of users using their ID

# Imports
from __future__ import print_function 
import os
import argparse
import io # to deal with unicode problem in python 2
import datetime
import codecs, json, time, tweepy
from itertools import islice

# api credentials
user_screen_name = "AminSarafraz"
consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_TOKEN_SECRET")

if __name__ == '__main__':
	batch_size = 95 # must be less than 100 (twitter limit)

	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--filename", required=True, help = "the filename of user_ids")
	args = ap.parse_args()
	
	# oAuth for twitter API
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	
	# Read user_ids file and get the followers information using their ids 
	n = 1;
	print('Extracting user info (', batch_size,  ' ids at a time):')
	with open(args.filename, 'r') as in_file:
		while True:
			user_ids = list(islice(in_file, batch_size))
			if not user_ids:
				break
	
			for user_id in user_ids:
				print(n, user_id)
				n +=1
	
			for i in xrange(0, len(user_ids), batch_size):
				users = api.lookup_users(user_ids=user_ids[i:i+n])	
				for user in users:
					print(user.id, user.screen_name)
	
			time.sleep(60)