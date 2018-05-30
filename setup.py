from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
import sqlite3, json, time
from textblob import TextBlob
from unidecode import unidecode
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# analyzer = SentimentIntensityAnalyzer()

conn = sqlite3.connect('twitter.db')
c = conn.cursor()

def create_table():
    try:
        c.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)")
        c.execute("CREATE INDEX fast_unix ON sentiment(unix)")
        c.execute("CREATE INDEX fast_tweet ON sentiment(tweet)")
        c.execute("CREATE INDEX fast_sentiment ON sentiment(sentiment)")
        conn.commit()
    except Exception as e:
        print(str(e))
create_table()

# consumer key and secret, access token and secret
ckey = 'CFJJc39JJXpQU0MADIjhUqomh'
csecret = 'S0Y7KPsdHzSwzkDenKYylgQnugboRq9SM8wonLwLIrAs2QsGwB'
atoken = '735219118278856704-XBWf86guWNRc5gjOVou7JODbTdhdm9u'
asecret = '9gRu2Uc1ze7TjTIKuBG09ioguLHi5dnO479vNGqe2UAa8'

class listener(StreamListener):
    def on_data(self, data):
        try:
            data = json.loads(data)
            tweet = unidecode(data['text'])
            time_ms = data['timestamp_ms']


            analysis = TextBlob(tweet)
            sentiment = analysis.sentiment.polarity

            # vs = analyzer.polarity_scores(tweet)
            # sentiment = vs['compound']

    
            print(time_ms, tweet, sentiment)
            c.execute("INSERT INTO sentiment (unix, tweet, sentiment) VALUES (?, ?, ?)", (time_ms, tweet, sentiment))
            conn.commit()
        except KeyError as e:
            print(str(e))
        return(True)
    
    def on_error(self, status):
        print(status)


while True:

    try:
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        twitterStream = Stream(auth, listener())
        twitterStream.filter(track=["a","e","i","o","u"])
    except Exception as e:
        print(str(e))
        time.sleep(5)