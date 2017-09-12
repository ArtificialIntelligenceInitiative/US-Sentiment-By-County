import dstk
import json
dstk = dstk.DSTK()

total_count = {}
with open("Sample Tweets/tweet_coordinates.txt") as coords:
    for line in coords:
        lat,lon = map(float,line.replace('\n','').split(','))
        result = dstk.coordinates2politics([lat,lon])
        try:
            for dict in result[0]['politics']:
                if dict['type'] == 'admin6':
                    code = dict['code']
                    code = code.replace('_','')
                    if len(code) == 5:
                        code = int(code)

                        if code in total_count:
                            total_count[code] += 1
                        else:
                            total_count[code] = 1
        except:
            pass
        #print(result[0]['politics'])

