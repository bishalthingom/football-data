# coding: utf-8

import urllib2
import re
import json
from haralyzer import HarParser


def getPlayerData(url, headers_data):
    headers = headers_data
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
    #     'Accept': 'application/json, text/javascript, */*; q=0.01',
    #     'Cookie': 'visid_incap_774904=OdRbvjYJSdymxe8ryMpemNWxiFkAAAAAQUIPAAAAAAAENuB0PU5tBJPn4nn8uBoK; incap_ses_709_774904=P0JaQeQAyzrXlVqmzt/WCQxsi1kAAAAAGZvnnOGiezDiCDDx5bOn4A==;',
    #     #'Accept-Encoding' : 'gzip, deflate, br',
    #     'Model-last-Mode' : 'u6Q/S0iMkzh29zFpBxbwlSBQq0KsyJbCNwPzz4u3MyA=',
    #     'X-Requested-With' : 'XMLHttpRequest'
    #     }
    # 'Accept-Language' :	'en-US,en;q=0.5', 'Accept-Encoding' : 'gzip, deflate, br', 'DNT' : '1' }
    req = urllib2.Request(url, None, headers)
    if 'StatisticsFeed' in url:
        html = urllib2.urlopen(req).readlines()
        # with open('Search results.html') as f:
        #     html = f.readlines()
        #     f.close()

        for line in html:
            print line

    return


def getPlayer(player_name):
    # player_name = player_name.replace(" ","+")
    # player_name = urllib.quote_plus(player_name)
    #
    # url = "http://www.whoscored.com/Search/?t=" + player_name
    # print url
    # headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
    #            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #            'Cookie': 'visid_incap_774904=wlEf+RsZRiKeiqwkgLOtpqhth1kAAAAAQUIPAAAAAADmrKYvVn9xvqxEScaO/A8R; incap_ses_704_774904=aw6lWs82mmJXAQPHUBzFCahth1kAAAAAhKiJkGumsNZOksDNuk2hhQ=='}
    # # 'Accept-Language' :	'en-US,en;q=0.5', 'Accept-Encoding' : 'gzip, deflate, br', 'DNT' : '1' }
    # req = urllib2.Request(url, None, headers)
    # html = urllib2.urlopen(req).readlines()
    with open('Search results.html') as f:
        html = f.readlines()
        f.close()

    player_search = "<td><a href=\"/Players/"
    player_regex = "href=\"(.*?)\""
    player_regex2 = "</span>(.*?)</a>"

    for line in html:
        if player_search in line:
            url = re.findall(player_regex, line)
            player_url = url[0].replace("Show", "History")
            print player_url
            break

    return

with open('/home/bishal/Desktop/test_har.har','r') as f:
    har_parser = HarParser(json.loads(f.read()))

for page in har_parser.pages:
    for entry in page.entries:
            url = entry['request']['url']
            headers = entry['request']['headers']
            req = urllib2.Request(url)
            print url
            for header in headers:
                req.add_header(header['name'], header['value'])
            try:
                resp = urllib2.urlopen(req)
            except:
                print "Exception"
            if 'https://www.whoscored.com/Players/300438/History/' in url:
                content = resp.read()
                print content









