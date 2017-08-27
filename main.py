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

        output = list()

    for i in range (len(alltweets)):
        analysis = TextBlob(alltweets[i].text)
        words = alltweets[i].text.split()
        misspelled = ""
        vulgar = ""
        for x in range (len(words)):
            if words[x] in vulgar_terms.bad_words.keys():
                vulgar += words[x] + ", "

            spellword = words[x]
            if spellword.startswith("@") == False and spellword.endswith(",") == False and spellword.startswith("https://") == False and spellword.startswith("http://") == False and enchant.Dict("en_US").check(words[x])  == False:
                misspelled += words[x] + ", "

        misspelled = misspelled[:len(misspelled)-2]
        vulgar = vulgar[:len(vulgar) - 2]

        if analysis.sentiment.polarity <= -0.2 and analysis.sentiment.subjectivity >= 0.5:
            if len(vulgar) != 0 and len(misspelled) != 0:
                output.append(alltweets[i].id_str + "*" + alltweets[i].text + "*" + str(vulgar) + "*" + str(misspelled) + "*" + str(analysis.sentiment.polarity) + "*" + str(analysis.sentiment.subjectivity))
            elif len(vulgar) != 0:
                output.append(alltweets[i].id_str + "*" + alltweets[i].text + "*" + str(vulgar) + "*" + "N/A" + "*" + str(analysis.sentiment.polarity) + "*" + str(analysis.sentiment.subjectivity))
            elif len(misspelled) != 0:
                output.append(alltweets[i].id_str + "*" + alltweets[i].text + "*" + "N/A" + "*" + str(misspelled) + "*" + str(analysis.sentiment.polarity) + "*" + str(analysis.sentiment.subjectivity))
            else:
                output.append(alltweets[i].id_str + "*" + alltweets[i].text + "*" + "N/A" + "*" + "N/A" + "*" + str(analysis.sentiment.polarity) + "*" + str(analysis.sentiment.subjectivity))
        elif len(vulgar) != 0 and len(misspelled) != 0:
            output.append(alltweets[i].id_str + "*" + alltweets[i].text + "*" + str(vulgar) + "*" + str(misspelled) + "*" + "N/A" + "*" + "N/A")
        elif len(vulgar) != 0:
            output.append(alltweets[i].id_str + "*" + alltweets[i].text + "*" + str(vulgar) + "*" + "N/A" + "*" + "N/A" + "*" + "N/A")
        elif len(misspelled) != 0:
            output.append(alltweets[i].id_str + "*" + alltweets[i].text + "*" + "N/A" + "*" + str(misspelled) + "*" + "N/A" + "*" + "N/A")

    # for i in range(len(output)):
    #     print(output[i])

    return output
