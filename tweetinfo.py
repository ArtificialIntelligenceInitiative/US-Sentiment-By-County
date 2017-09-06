import json

#Program extracts the tweet and coordinates from the twitterdata.json file and prints them to a tsv file
#This will eventually be changed to run sentiment analysis on the tweet and replace the tweet in the tsv file
#with a numerical value corresponding to the sentiment of the tweet
with open('twitterdata.json', 'r', encoding='utf-8') as f:
    try:
        for line in f:
            tweet = json.loads(line)
            with open('tweet_coordinates.tsv', 'a') as c:
                longitude, latitude = (tweet["coordinates"]["coordinates"]) #extract coordinates from dictionary
                coordinates = str(latitude) + "," + str(longitude) #put coordinates in correct order
                text = str(tweet["text"]).replace("\n", " ").replace("\t", " ").replace("\r", "") #replace non-text
                c.write(coordinates + "\t" + text + "\n") #write data to a .tsv file
                print((coordinates + "\t" + text + "\n")) #print data to terminal
    except BaseException as e:
        print("Error: %s" % str(e))
