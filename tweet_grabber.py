import tweepy
import json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

#put twitter credentials below
consumer_key = 'iSRtkvFpgktayh7zBDO5SmjV4'
consumer_secret = 'ftam77i3aZtrknDrVWAsJzfI3WRD3V02o8gFzv73NU0A1sZb9K'
access_token = '2737819997-eUJxIDNiSuHuQssQIOtWvWrfPTcg04Jwoxw3KCo'
access_secret = '3Z4J9Bv0mWXBjEqG311NJorplyCq3KL7C5kMUzUlcqKPY'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

class MyListener(StreamListener):
    def on_data(self, data):
        try:
            # Grabs all new tweets with coordinates enabled and prints the tweet info to a .json file.
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
            #print("Error on_data: %s" % str(e))
            return True

    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#irma', 'irma'])
