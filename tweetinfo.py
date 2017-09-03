import json

#Program takes the tweet itself and the coordinates and prints them to
#seperate .txt files. Note: The coordinate part needs to be fixed to
#only write the coordinates and in the correct order (they are currently
#inversed).
with open('twitterdata.json', 'r') as f:
    for line in f:
        tweet = json.loads(line)
        with open('tweet_text', 'a', encoding='utf-8') as t:
            t.write(tweet['text'] + "\n\n")
        with open('tweet_coordinates', 'a') as c:
            if tweet['coordinates']:
                json.dump(tweet["coordinates"],c)
                print(tweet['coordinates'])
                print("a\n")

