# tweet_grabber
This project is an ongoing effort by the *Artificial Intelligence Initiative*, an organization at Texas Tech University.  

The goal of this project is to gather sentiment on tweets over a given topic and display it using interactive maps. Currently, the program only works for tweets written in English and maps the sentiment to United States counties. Further efforts will focus on allowing the map type to display sentiment by state and country, and to provide more interactive features.

![](https://i.imgur.com/wvkkSJo.png)
*Figure-1: A map of sentiment analysis from October 10th through October 13th, 2017 on tweets including "Trump" and/or "POTUS", seperated by county. 
(Note: An average sentiment near zero for a county has the same color as a county with no data, and will be fixed in future versions)* 

## Dependencies: 
[Tweepy (v3.5.0)](http://www.tweepy.org/) - Twitter's API

[TextBlob](https://textblob.readthedocs.io/en/dev/) - Python library for text processing.

Works with [Python 3.0-3.6](https://www.python.org/downloads/) 


## Usage:

#### -Mapping Coordinates
The program currently acquires coordinates using the twitter api through two methods. After filtering out the tweets for key words the user enters, the program first checks if the user has enabled the security setting allowing for their coordinates to be printed in the .json file. If not, the program next checks if the user has provided the place where they live on their profile. The twitter api gives a coordinate box around any given city, and can therefore be mapped to a county.

After acquiring the coordinates, the program uses the 'coordinates2politics' function from the Data Science Toolkit [Link](http://www.datasciencetoolkit.org/). This function returns a dictionary like so:

![](https://i.imgur.com/svE9Tox.png)

If the dictionary contains the county code (06_075 in the example case), the program moves on to run sentiment analysis on the tweet. Using TextBlob, a python library for text processing, a score is returned indicating whether it was a favorable or unfavorable tweet. That score is then averaged together with all other tweets gathered for that county. That data is then saved in a tab seperated value file (.tsv), with one column for county code, and the second for average sentiment.

With this data, we can now create our graph. We use D3JS's [Choropleth](https://bl.ocks.org/mbostock/4060606) graph to display the data. We changed the HTML flie to give a sentiment score ranging from -5 to 5, and a color scheme ranging from  red -> blue.