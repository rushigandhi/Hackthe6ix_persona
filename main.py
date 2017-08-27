import tweepy
import config
from textblob import TextBlob
from textblob import Word
import vulgar_terms
import enchant

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
        output = list()
        analysis = TextBlob(alltweets[i].text)
        words = alltweets[i].text.split()
        misspelled = list()
        vulgar = list()
        for x in range (len(words)):
            if words[x] in vulgar_terms.bad_words.keys():
                vulgar.append(words[x])

            spellword = words[x]
            if spellword.startswith("@") == False and spellword.endswith(",") == False and spellword.startswith("https://") == False and spellword.startswith("http://") == False and enchant.Dict("en_US").check(words[x])  == False:
                misspelled.append(words[x])
        # print(alltweets[i].id_str, alltweets[i].created_at, alltweets[i].text, analysis.sentiment, vulgar)

        if analysis.sentiment.polarity <= 0.2 and analysis.sentiment.subjectivity >= 0.5:
            if len(vulgar) != 0 and len(misspelled) != 0:
                output.append(str(alltweets[i].text) + " MISPELLED WORDS " + str(misspelled) + " and " + " BAD WORDS " + str(vulgar) + " and you are NEGATIVE AND SUBJECTIVE " + str(analysis.sentiment))
            elif len(vulgar) != 0:
                output.append(str(alltweets[i].text) + " BAD WORDS " + str(vulgar) + " and you are NEGATIVE AND SUBJECTIVE " + str(analysis.sentiment))
            elif len(misspelled) != 0:
                output.append(str(alltweets[i].text) + " MISPELLED WORDS " + str(misspelled) + " and you are NEGATIVE AND SUBJECTIVE " + str(analysis.sentiment))
            else:
                output.append(str(alltweets[i].text) + " you are NEGATIVE AND SUBJECTIVE " + str(analysis.sentiment))
        elif len(vulgar) != 0 and len(misspelled) != 0:
            output.append(str(alltweets[i].text) + " MISPELLED WORDS " + str(misspelled) + " and " + " BAD WORDS " + str(vulgar))
        elif len(vulgar) != 0:
            output.append(str(alltweets[i].text) + " BAD WORDS " + str(vulgar))
        elif len(misspelled) != 0:
            output.append(str(alltweets[i].text) + " MISPELLED WORDS " + str(misspelled))





if __name__ == '__main__':
    print("What is your Twitter id?")
    username = raw_input()
    print("Hello " + username + " we will help you fix your Twitter! Please press enter!")
    get_all_tweets(username)
