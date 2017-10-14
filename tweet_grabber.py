import tweepy
import json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from textblob import TextBlob
from http.client import IncompleteRead # Python 3

import requests

# put twitter credentials below
consumer_key = 'TelkaEC2GUWR0IJogWxkrpZKy'
consumer_secret = 'ENYYJseZJ1IY0wqXUSnEj0i2L0Xz3v2c6MRvPEzY6hnrt3ZEEj'
access_token = '1620837440-0p8voswXhMYGO8upThRqeGwzUuh3TI9sPnQkZim'
access_secret = 'obvlWiW1Tvkdl1JYyA6hbIrJ96yvq1OS2hILRHs3R0HHy'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


def read_counties():
    dict = {}
    with open("counties.txt","r+") as c:
        for line in c:
            code = line.rstrip()
            dict[code] = (0, 0)

    return dict


def write_counties(counties):
    with open("mapvalues.txt", "w+") as f:
        f.write("id\trate\n")
        for key, val in counties.items():
            f.write(key+"\t"+str(val[0])+"\n")

def clean_coordinates(tweet):

    longitude, latitude = (tweet["coordinates"]["coordinates"])  # extract coordinates from dictionary
    return str(latitude), str(longitude)


def clean_place(tweet):
    longitude, latitude = (tweet["place"]["bounding_box"]["coordinates"][0][0])
    return str(latitude), str(longitude)

def get_coordinates(json_data):
    if json_data['coordinates']:
        latitude, longitude = clean_coordinates(json_data)
        r = requests.get("http://www.datasciencetoolkit.org/coordinates2politics/" + latitude + "%2c" + longitude)
        return json.loads(r.text)

    elif json_data['place']:
        latitude, longitude = clean_place(json_data)
        r = requests.get("http://www.datasciencetoolkit.org/coordinates2politics/" + latitude + "%2c" + longitude)
        return json.loads(r.text)

    else:
        return ""



class MyListener(StreamListener):
    def on_data(self, data):
        try:
            json_data = json.loads(data)
            r = get_coordinates(json_data)

            if r != "":

                for dict in r[0]['politics']:
                    if dict['type'] == 'admin6':
                        code = dict['code']
                        code = code.replace('_', '')
                        text = str(json_data['text'])
                        print(text)
                        print("\n")
                        textb = TextBlob(text)
                        sentiment = 5*float(textb.sentiment.polarity)
                        print(sentiment)
                        print("\n")
                        line = counties[code]
                        avg = line[0]
                        count = line[1]
                        new_avg = (avg * count + sentiment) / (count + 1)
                        counties[code] = (new_avg, count + 1)
                        print(code, line, counties[code])
                        write_counties(counties)

        except BaseException as e:
            #print("Error on_data: %s" % str(e))
            pass



    def on_error(self, status):
        print(status)
        return True


counties = read_counties()

while True:
    try:
        # Connect/reconnect the stream
        twitter_stream = Stream(auth, MyListener())
        # DON'T run this approach async or you'll just create a ton of streams!
        twitter_stream.filter(track=['Trump', '#Trump', 'POTUS'])
    except KeyboardInterrupt:
        # Or however you want to exit this loop
        twitter_stream.disconnect()
        break
    except:
        # Oh well, reconnect and keep trucking
        continue
