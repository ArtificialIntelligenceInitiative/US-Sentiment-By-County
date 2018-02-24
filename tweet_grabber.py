import tweepy                   # Allows use of Twitter's API
import json                     # Allows for manipulation of JSON data
import requests                 # Used to request from datasciencetoolkit.org
from textblob import TextBlob   # Used to run sentiment analysis on tweets
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from http.client import IncompleteRead # Python 3


# Functions "clean_coordinates" and "clean place" take in JSON data of a tweet and return
# the coordinates ordered by latitude, longitude. The coordinates are ordered in the JSON
# data by longitude, latitude, and these functions serve to standardize the order throughout
# the rest of the program.

def clean_coordinates(tweet):
    longitude, latitude = (tweet["coordinates"]["coordinates"])  # extract coordinates from dictionary
    return str(latitude), str(longitude)

def clean_place(tweet):
    longitude, latitude = (tweet["place"]["bounding_box"]["coordinates"][0][0])
    return str(latitude), str(longitude)

# Function "get_coordinates" takes the JSON data of a tweet and returns JSON data
# based on the coordinates from which the tweet originated by passing a request to
# www.datasciencetoolkit.org.
# Note: If the owner of the tweet did not have coordinates enabled, but had a 'place'
# listed on their account, then the function returns the info on the coordinates of
# that city/place.

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

# Function "read_counties" initializes a dictionary with US county codes
# listed in counties.txt.
def read_counties():
    dict = {}
    with open("counties.txt", "r+") as c:
        for line in c:
            code = line.rstrip()
            dict[code] = (None, 0)
    return dict

# Function "write_counties" takes in the dictionary of US counties and updates their
# sentiment values in mapvalues.txt.
def write_counties(counties):
    with open("mapvalues.txt", "w+") as f:
        f.write("id\trate\n")
        for key, val in counties.items():
            f.write(key + "\t" + str(val[0]) + "\n")

# Function "printFormat" prints tweet text, sentiment analysis
# county code and its current sentiment analysis average.
def printFormat(text,sentiment,code,line):
    print("Text:\t\t\t",text)
    print("Sentiment:\t\t",sentiment)
    print("County Code:\t",code)
    print("(Avg, #):\t\t",line,"\n")

# Function "getSentiment" returns sentiment analysis on input text with a
# range from -5(negative, unfavorable) to 5(positive, favorable).
def getSentiment(text):
    textb = TextBlob(text)
    sentiment = 5 * float(textb.sentiment.polarity)
    return sentiment

# Function "updateCounty" updates mapvalues.txt with the new average
# sentiment and total tweet count.
def updateCounty(code,sentiment):
    line = counties[code]
    if line[0] == None:
        counties[code] = (sentiment, 1)
    else:
        avg = line[0]
        count = line[1]
        new_avg = (avg * count + sentiment) / (count + 1)
        counties[code] = (new_avg, count + 1)
    write_counties(counties)

class MyListener(StreamListener):
    def on_data(self, data):
        try:
            # Get JSON data of tweet and acquire coordinates
            json_data = json.loads(data)
            r = get_coordinates(json_data)

            # If coordinates could be matched to the tweet
            # mapvalues.txt is updated accordingly
            if r != "":
                for dict in r[0]['politics']:
                    if dict['type'] == 'admin6':
                        code = dict['code'].replace('_', '')
                        text = str(json_data['text'])
                        sentiment = getSentiment(text)
                        updateCounty(code,sentiment)
                        printFormat(text,sentiment,code,counties[code])

        except BaseException as e:
            #print("Error on_data: %s" % str(e))
            pass

    def on_error(self, status):
        print(status)
        return True


# List twitter credentials below
# Access yours by creating an app on https://apps.twitter.com/
consumer_key = 'TelkaEC2GUWR0IJogWxkrpZKy'
consumer_secret = 'ENYYJseZJ1IY0wqXUSnEj0i2L0Xz3v2c6MRvPEzY6hnrt3ZEEj'
access_token = '1620837440-0p8voswXhMYGO8upThRqeGwzUuh3TI9sPnQkZim'
access_secret = 'obvlWiW1Tvkdl1JYyA6hbIrJ96yvq1OS2hILRHs3R0HHy'


# Confirms credentials with twitter and connect to API
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)
counties = read_counties()

# Streams tweets until exit.
while True:
    try:
        # Connect/reconnect the stream
        twitter_stream = Stream(auth, MyListener())
        # DON'T run this approach async or you'll just create a ton of streams!
        twitter_stream.filter(track=['texas tech', 'TTU'])
    except KeyboardInterrupt:
        # Or however you want to exit this loop
        twitter_stream.disconnect()
        break
    except:
        # Oh well, reconnect and keep trucking
        continue