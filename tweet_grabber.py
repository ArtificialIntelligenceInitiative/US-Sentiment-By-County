import tweepy
import json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

import requests

# put twitter credentials below
consumer_key = 'TelkaEC2GUWR0IJogWxkrpZKy'
consumer_secret = 'ENYYJseZJ1IY0wqXUSnEj0i2L0Xz3v2c6MRvPEzY6hnrt3ZEEj'
access_token = '1620837440-0p8voswXhMYGO8upThRqeGwzUuh3TI9sPnQkZim'
access_secret = 'obvlWiW1Tvkdl1JYyA6hbIrJ96yvq1OS2hILRHs3R0HHy'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


def clean_coordinates(tweet):
    print('test')
    print(tweet["coordinates"])
    longitude, latitude = (tweet["coordinates"]["coordinates"])  # extract coordinates from dictionary
    return str(latitude), str(longitude)

class MyListener(StreamListener):
    def on_data(self, data):
        try:
            # Grabs all new tweets with coordinates enabled and prints the tweet info to a .json file.
            json_data = json.loads(data)
            text = str(json_data['text'])

            a = requests.post("http://www.datasciencetoolkit.org/text2sentiment", data="{'data':" + text + "}")
            #a = 'not'
            print(text, "SENTIMENT: " + a.text)

            if json_data['coordinates']:
                latitude, longitude = clean_coordinates(json_data)
                print(latitude, longitude)
                r = requests.get("http://www.datasciencetoolkit.org/coordinates2politics/"+latitude+"%2c"+longitude)
                print(r.text)

        except BaseException as e:
            #print("Error on_data: %s" % str(e))
            pass

    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#Trump','Trump', "#Hillary", "Hillary" "Bernie"])

