# Imports
import os
import codecs
import json
import time
import tweepy
import pymongo
from itertools import islice

# Inputs
user_screen_name = "TheBooklio"
consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_TOKEN_SECRET")


file_name = "temp/booklio_followers_id.csv"
batch_size = 95 # must be less than 100 (twitter limit)

# Connection to Mongo DB
try:
	client = pymongo.MongoClient()
	print "Connected to MongoDB successfully!!!"
except pymongo.errors.ConnectionFailure, e:
	print "Could not connect to MongoDB: %s" % e 

db = client.booklio_family #  MongoDB database
user_bucket = db.twitter_bucket #  Collection in the database where user data will be inserted

# oAuth for twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Read user_ids file and get the followers information using their ids 
n = 1;
print 'Extracting user info and updating MongoDB documents (', batch_size,  ' ids at a time):'
with open(file_name, 'r') as in_file:
	while True:
		user_ids = list(islice(in_file, batch_size))
		if not user_ids:
			break

		for user_id in user_ids:
			print n, user_id
			n +=1

		for i in xrange(0, len(user_ids), batch_size):
			users = api.lookup_users(user_ids=user_ids[i:i+n])
			# Loop through each user and ingest its information in MongoDB

			for user in users:
				# Get the following_list if exists and append to it. Create new if it does not exist
				following_list = []
				returned_cursor = user_bucket.find({"id": user.id, "following_list": {"$exists": True}})
				for doc in returned_cursor:
					following_list = doc['following_list']

				if user_screen_name not in following_list:
					following_list.append(user_screen_name)

				user._json['following_list'] = following_list

				user_bucket.update({"id": user.id}, user._json, upsert=True) # inserts new document if it does not exist.

		time.sleep(60)

client.close() # Close connection to MongoDB
print "Connection to MongoDB was closed successfully!"