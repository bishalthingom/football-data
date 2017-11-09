import urllib2
import urllib
import re

def GetTopLeagues():
    url = "https://www.transfermarkt.com/wettbewerbe/asien"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    # 'Accept-Language' :	'en-US,en;q=0.5', 'Accept-Encoding' : 'gzip, deflate, br', 'DNT' : '1' }
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).readlines()

    league_search = "</table></td><td class=\"zentriert\">"
    league_search1 = "<a href=\""
    league_search2 = "\" title=\""

    league_link_regex = "href=\"(.*?)\""

    i = 0

    for line in html:
        if league_search in line and league_search1 in line and league_search2 in line:
            i += 1
            league_link = re.findall(league_link_regex, line)
            league_url = league_link[0].replace("startseite","transfers") + "/"
            print league_url

    print i

GetTopLeagues("https://www.transfermarkt.com/premier-league/transfers/wettbewerb/GB1")