import urllib2
import urllib
import re

def GetSeasons(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).readlines()

    start_tag = "<select name=\"saison_id\""
    end_tag = "<select name=\"s_w\""
    flag = 0
    season_value_regex = "value=\"(.*?)\""
    for line in html:
        if start_tag in line:
            print "got the tag"
            flag = 1
        elif end_tag in line:
            break
        if "option" in line and flag == 1:
            season_value = re.findall(season_value_regex,line)
            season_value = season_value[0]
            print season_value

GetSeasons("https://www.transfermarkt.com/premier-league/transfers/wettbewerb/GB1")