import os
import pymongo
import tweepy
import time
import struct

user_screen_name = "TheBooklio"
consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_TOKEN_SECRET")

# Connection to Mongo DB
try:
    client=pymongo.MongoClient()
    print "Connected to MongoDB successfully!!!"
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e 

db = client.twitter_results #  MongoDB database
posts = db.posts #  Collection in the database where search data will be inserted

# Get search data from Twitter and ingest in MongoDB
query ='books'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

search = []
for tweets in tweepy.Cursor(api.search, q=query).pages(2):
    search.extend(tweets)
#    time.sleep(60)
#    for tweet in tweets:
#       print tweet.text.encode('utf-8')
#       time.sleep(1)

#print search[0].text.encode('utf-8')

# loop through search and insert dictionary into mongoDB
for tweet in search:
    # Empty dictionary for storing tweet related data
    data ={}
    data['first'] = 1;
    data['second'] = 'second';
    #data['created_at'] = tweet.created_at
    #data['coordinates'] = tweet.coordinates
    #data['entities'] = tweet.entities
    #data['favorite_count'] = tweet.favorite_count
    #data['favorited'] = tweet.favorited
    #data['geo'] = tweet.geo
    #data['id'] = tweet.id
    #data['id_str'] = tweet.id_str
    #data['lang'] = tweet.lang
    #data['place'] = tweet.place
    #data['retweet_count'] = tweet.retweet_count
    #data['retweeted'] = tweet.retweeted
    #data['source'] = tweet.source
    #data['text'] = tweet.text
    #data['truncated'] = tweet.truncated
    #data['user'] = tweet.user
    # Insert process
    posts.insert(data)

client.close()
print "Connection to MongoDB was closed successfully!"
