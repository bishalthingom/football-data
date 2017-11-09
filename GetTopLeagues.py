import urllib2
import urllib
import re

def GetTopLeagues():
    f = open('Football Statistics _ Football Live Scores _ WhoScored.com.html','r')

    data =f.readlines()

    league_search = "ul id=\"popular-tournaments-list\""

    league_link_regex = "href=\"(.*?)\""

    i = 0

    for line in data:
        if league_search in line:
            league_link = re.findall(league_link_regex, line)
            for comp in league_link:
                print comp


GetTopLeagues()