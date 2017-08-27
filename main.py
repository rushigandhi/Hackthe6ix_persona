import tweepy
import config
from textblob import TextBlob

consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_token_secret = config.access_token_secret

def get_all_tweets(screen_name):

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    alltweets = []

    new_tweets = api.user_timeline(screen_name = screen_name,count=200)

    alltweets.extend(new_tweets)

    oldest = alltweets[-1].id - 1

    while len(new_tweets) > 0:
        print("getting tweets before %s    " % (oldest))

        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

        alltweets.extend(new_tweets)

        oldest = alltweets[-1].id - 1

        print ("...%s tweets downloaded so far" % (len(alltweets)))


    for tweet in alltweets:
        print(tweet.text)
        analysis = TextBlob(tweet.text)
        print(analysis.sentiment)



if __name__ == '__main__':
    print("What is your Twitter id?")
    username = raw_input()
    print("Hello " + username + " we will help you fix your Twitter! Please press enter!")
    get_all_tweets(username)
