# gets user ids of twitter followings (friends) of a specific account (user_screen_name) and
# saves them in a csv file user_screen_name+'_followers_twitter_ids.csv'

# Imports
import os
import codecs
import time
import tweepy

# Inputs
user_screen_name = "AminSarafraz"
consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_TOKEN_SECRET")

# oAuth for twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Get user ids for the followings (friends) of a user
user_ids = []
total_number_user_ids = 0
for page in tweepy.Cursor(api.friends_ids, screen_name=user_screen_name).pages():
    user_ids.extend(page)
    with codecs.open(user_screen_name + '_followings_twitter_ids.csv', encoding='utf-8', mode='a+') as text_file:
        for user_id in user_ids:
            text_file.write(u'{} \n'.format(user_id))

    total_number_user_ids += len(user_ids)
    print("Total number of user ids extracted from the followings (friends) of", user_screen_name, ":",
          total_number_user_ids)
    user_ids = []

    time.sleep(61)  # To avoid exceeding Twitter API rate limit (15 GETS every 15 minutes)
