import json

# Program extracts the tweet and coordinates from the twitterdata.json file and prints them to txt files
# This will eventually be changed to run sentiment analysis on the tweet and give a numerical value
# corresponding to the sentiment of the tweet. The coordinates need to be converted to county as well.

with open('twitterdata.json', 'r', encoding='utf-8') as f:
    try:
        with open('tweet_coordinates.txt', 'a', encoding='utf-8') as c:
            with open('tweet_text.txt', 'a', encoding='utf-8') as t:
                for line in f:
                    tweet = json.loads(line)
                    longitude, latitude = (tweet["coordinates"]["coordinates"]) # extract coordinates from dictionary
                    coordinates = str(latitude) + "," + str(longitude) # put coordinates in correct order
                    text = str(tweet["text"]).replace("\n", " ").replace("\t", " ").replace("\r", "") # replace non-text
                    c.write(coordinates + "\n")
                    t.write(text + "\n")
    except BaseException as e:
        print("Error: %s" % str(e))
