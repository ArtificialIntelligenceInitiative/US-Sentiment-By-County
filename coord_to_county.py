import json
import requests

total_count = {}
with open("Sample Tweets/tweet_coordinates.txt") as coords:
    for line in coords:
        line1 = line.replace('\n','').split(',')
        #print(line1)
        lat, lon = map(float,line1)
        result = dstk.coordinates2politics([lat,lon])
        try:
            for dict in result[0]['politics']:
                if dict['type'] == 'admin6':
                    code = dict['code']
                    code = code.replace('_','')
                    if len(code) == 5:
                        print(code)

                        if code in total_count:
                            total_count[code] += 1
                        else:
                            total_count[code] = 1
        except:
            pass


