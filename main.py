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

        print("...%s tweets downloaded so far" % (len(alltweets)))

    totalPolwo0 = 0
    totalTweetswo0 = 0
    totalPolw0 = 0

    for i in range (len(alltweets)):
        print(alltweets[i].text)
        analysis = TextBlob(alltweets[i].text)

    for tweet in alltweets:
        print(tweet.text)
        analysis = TextBlob(tweet.text)
        print(analysis.sentiment)

        if analysis.sentiment.polarity != 0:
            totalTweetswo0 += 1
            totalPolwo0 += analysis.sentiment.polarity
        totalPolw0 += analysis.sentiment.polarity

    meanPolw0 = totalPolw0/len(alltweets)
    meanPolwo0 = totalPolwo0/totalTweetswo0

    if meanPolwo0 >= 0.5:
        print("Your Twitter is great and the mean polarity w/o 0s is " + str(meanPolwo0) + ". Keep up the good work!" )

    elif meanPolwo0 <= -0.5:
        print("Your Twitter is negative and the mean polarity is w/o 0s " + str(meanPolwo0) + ". Please make some changes!" )
    elif -0.5 < meanPolwo0 < 0.5:
        print ("Your Twitter is neutral and the mean polarity is w/o 0s " + str(meanPolwo0) + ".")

    if meanPolw0 >= 0.5:
        print("Your Twitter is great and the mean polarity with 0s is " + str(meanPolw0) + ". Keep up the good work!" )

    elif meanPolw0 <= -0.5:
        print("Your Twitter is negative and the mean polarity is with 0s " + str(meanPolw0) + ". Please make some changes!" )
    elif -0.5 < meanPolw0 < 0.5:
        print ("Your Twitter is neutral and the mean polarity is with 0s " + str(meanPolw0) + ".")


if __name__ == '__main__':
    print("What is your Twitter id?")
    username = raw_input()
    print("Hello " + username + " we will help you fix your Twitter! Please press enter!")
    get_all_tweets(username)
