import tweepy
import json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

#put twitter credentials below
#consumer_key =
#consumer_secret =
#access_token =
#access_secret =

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

class MyListener(StreamListener):
    def on_data(self, data):
        try:
            #This code grabs all tweets and prints their data into twitterdata.json. If you want only tweets that have
            # coordinates enabled, comment this code out and use the other variation
            #with open('twitterdata.json', 'a', newline='') as f:
                #f.write(data)
                #return True

            #If you want to only grab tweets where the user has coordinates enabled, use this code
            #Note: Tweets where the user does not have coordinates enabled will throw an exception and
            #      will be printed to the console. If it is enabled, the coordinates will be printed.

            json_data = json.loads(data)
            if json_data['coordinates']:
                coords = json_data["coordinates"]
                if coords is not None:
                    with open('twitterdata.json', 'a', newline='') as f:
                        f.write(data)
                        print(coords)
                        print('\n')
                        return True


        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['irma'])
