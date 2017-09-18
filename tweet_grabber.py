import tweepy
import json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

import requests

# put twitter credentials below
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


def clean_coordinates(tweet):

    longitude, latitude = (tweet["coordinates"]["coordinates"])  # extract coordinates from dictionary
    return str(latitude), str(longitude)


def clean_place(tweet):
    longitude, latitude = (tweet["place"]["bounding_box"]["coordinates"][0][0])
    print(str(latitude), str(longitude))
    return str(latitude), str(longitude)

class MyListener(StreamListener):
    def on_data(self, data):
        try:
            # Grabs all new tweets with coordinates enabled and prints the tweet info to a .json file.
            json_data = json.loads(data)
            text = str(json_data['text'])

            a = requests.post("http://www.datasciencetoolkit.org/text2sentiment", data="{'data':" + text + "}")
            #a = 'not'
            #print(text, "SENTIMENT: " + a.text , json_data['place'])

            r = 0

            if json_data['coordinates']:
                latitude, longitude = clean_coordinates(json_data)
                r = requests.get("http://www.datasciencetoolkit.org/coordinates2politics/"+latitude+"%2c"+longitude)

            elif json_data['place']:
                latitude, longitude = clean_place(json_data)
                r = requests.get("http://www.datasciencetoolkit.org/coordinates2politics/"+latitude+"%2c"+longitude)

            if r:
                r = json.loads(r.text)


                for dict in r[0]['politics']:
                    if dict['type'] == 'admin6':
                        code = dict['code']
                        code = code.replace('_', '')
                        if len(code) == 5:
                            print(json_data['text'], "SENTIMENT: " + a.text, "COUNTY CODE: " + code)


            #print("SOMETHING FUCKED UP")

        except BaseException as e:
            #print("Error on_data: %s" % str(e))
            pass

    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#Trump','Trump', "#Hillary", "Hillary" "Bernie"])

