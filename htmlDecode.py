from HTMLParser import HTMLParser

seasons = open('seasons_info.txt','r')
seasons_op = open('seasons_op.txt','a+')

seasons_dat = seasons.readlines()

h = HTMLParser()
for season in seasons_dat:
    seasons_op.write(h.unescape(season))
    print h.unescape(season)