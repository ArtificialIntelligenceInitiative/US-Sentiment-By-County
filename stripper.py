with open("sentiment.tsv", 'r+') as f:
    with open("counties.txt", 'w+') as c:
        for line in f:
            print(line.split())
            county = line.split()[0]
            c.write(county+'\n')
