# coding: utf-8

import time
import urllib2
import urllib
import re
import sys, select

def GetSeasons(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    seasons = []
    req = urllib2.Request(url, None, headers)
    try:
        html = urllib2.urlopen(req).readlines()
    except urllib2.HTTPError, err:
        if err.code == 404:
            print "Page not found for " + url
            return seasons


    start_tag = "<select name=\"saison_id\""
    end_tag = "<select name=\"s_w\""
    flag = 0
    season_value_regex = "value=\"(.*?)\""

    for line in html:
        if start_tag in line:
            flag = 1
        elif end_tag in line:
            break
        if "option" in line and flag == 1:
            season_value = re.findall(season_value_regex,line)
            season_value = season_value[0]
            seasons.append(season_value)
    return seasons

def getTransfersForLeagueSeason(league, season, s_w, lineno, fileno):
    url = league + "/plus/?saison_id=" + season + "&s_w=" + s_w + "&leihe=1&intern=0"
    # url = "https://www.google.com"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    # 'Accept-Language' :	'en-US,en;q=0.5', 'Accept-Encoding' : 'gzip, deflate, br', 'DNT' : '1' }

    print url
    # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    # opener.addheaders.append(('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'))
    # response = opener.open(url)
    # html = response.readlines()
    req = urllib2.Request(url, None, headers)
    flag = 0
    retry_count = 0
    while flag == 0:
        try:
            html = urllib2.urlopen(req, timeout=30).readlines()
            flag = 1
        except:
            print "Error. Retrying. \n"
            time.sleep(30)
            retry_count += 1
            if (retry_count == 3):
                print "Expecting input for long wait."
                i, o, e = select.select([sys.stdin], [], [], 10)
                if (i):
                    time.sleep(600)
                    retry_count = 0
                else:
                    time.sleep(120)
                    retry_count = 0
    # with open('Premier League - Transfers 15_16 | Transfermarkt.html') as f:
    #     html = f.readlines()
    #     f.close()



    country1_search = "class=\"miniflagge\" />&nbsp;"
    country1_regex = "title=\"(.*?)\""
    arrivals_search = "<th class=\"spieler-transfer-cell\">Arrivals</th>"
    departures_search = "<th class=\"spieler-transfer-cell\">Departures</th>"
    club1_search = "<div class=\"table-header\" id="
    club1_regex = "alt=\"(.*?)\" class="
    player_search = "class=\"hide-for-small\"><a title=\""
    player_regex1 = "href=\"(.*?)/a>"
    player_regex2 = ">(.*?)<"
    age_search = "<td class=\"zentriert alter-transfer-cell\">"
    age_regex = "<td class=\"zentriert alter-transfer-cell\">(.*?)</td>"
    nationality_search = "class=\"flaggenrahmen\" /></td>"
    nationality_regex = "title=\"(.*?)\" alt="
    club2_search = "<td class=\"no-border-rechts zentriert\">"
    club2_regex = "alt=\"(.*?)\""
    country2_search = "<td class=\"no-border-links verein-flagge-transfer-cell\">"
    country2_regex = "alt=\"(.*?)\""
    market_value_search = "<td class=\"rechts mw-transfer-cell\">"
    fee_search = "<td class=\"rechts"
    fee_regex = ">(.*?)<"

    filename = "output1.csv"

    if(lineno % 5000 == 0):
        time.sleep(10)
    if s_w == 'w':
        season = str(int(season) + 1)

    output = open(filename, 'a+')

    #output.write("Player, Age, Nationality, FromClub, FromCountry, ToClub, ToCountry, Season, Window, Type, Fee\r")

    for line in html:
        if country1_search in line:
            country1 = re.findall(country1_regex, line)
            dat_country1 = country1[0]
        if club1_search in line:
            club1 = re.findall(club1_regex, line)
            dat_club1 = club1[0]
        elif arrivals_search in line:
            arrivals_flag = 1
        elif departures_search in line:
            arrivals_flag = 0
        elif player_search in line:
            player = re.findall(player_regex1, line)
            player = re.findall(player_regex2, player[0])
            dat_player = player[0]
        elif age_search in line:
            age = re.findall(age_regex, line)
            dat_age = age[0]
        elif nationality_search in line:
            nationality = re.findall(nationality_regex, line)
            dat_nationality = nationality[0]
        elif club2_search in line:
            club2 = re.findall(club2_regex, line)
            dat_club2 = club2[0]
        elif country2_search in line:
            country2 = re.findall(country2_regex, line)
            if len(country2) == 0:
                dat_country2 = "-"
            else:
                dat_country2 = country2[0]
        elif fee_search in line and market_value_search not in line:
            fee = re.findall(fee_regex, line)
            #Swap Deal
            if "End of loan" in fee[1]:
                dat_type = "EL"
                dat_fee = "-"
            elif "Free transfer" in fee[1]:
                dat_type = "T"
                dat_fee = "0"
            elif "-" in fee[1]:
                dat_type = "-"
                dat_fee = "-"
            elif "?" in fee[1]:
                dat_type = "T"
                dat_fee = "?"
            elif "€" in fee[1]:
                dat_type = "T"
                if "Mill" in fee[1]:
                    multiplier = 1000000
                elif "Th" in fee[1]:
                    multiplier = 1000
                else:
                    multiplier = 1

                values = re.findall('[0-9,]', fee[1])

                stringval = ""
                for char in values:
                    if char == ',':
                        stringval += '.'
                    else:
                        stringval += char

                dat_fee = str(float(stringval) * multiplier)
            elif "Loan" in fee[1]:
                dat_type = "L"
                if len(fee) > 3:
                    if "Mill" in fee[3]:
                        multiplier = 1000000
                    elif "Th" in fee[3]:
                        multiplier = 1000
                    else:
                        multiplier = 1

                    values = re.findall('[0-9,]', fee[3])

                    stringval = ""
                    for char in values:
                        if char == ',':
                            stringval += '.'
                        else:
                            stringval += char

                    dat_fee = str(float(stringval) * multiplier)
                else:
                    dat_fee = "0"
            elif "Swap" in fee[1]:
                dat_type = 'S'
                dat_fee = '-'
            try:
                if (arrivals_flag == 1):
                    dat_transfer = dat_player + "," + dat_age + "," + dat_nationality + "," + dat_club2 + "," + dat_country2 + "," + dat_club1 + "," + dat_country1 + "," + season + "," + s_w + "," + dat_type + "," + dat_fee
                    output.write(dat_transfer + "\n")
                    lineno += 1
                else:
                    dat_transfer = dat_player + "," + dat_age + "," + dat_nationality + "," + dat_club1 + "," + dat_country1 + "," + dat_club2 + "," + dat_country2 + "," + season + "," + s_w + "," + dat_type + "," + dat_fee
                    output.write(dat_transfer + "\n")
                    lineno += 1
            except:
                output.close()
                return lineno, fileno

    output.close()

    return lineno, fileno

#getTransfersForLeagueSeason()

def createData():
    with open('allLeagues.txt') as f:
        leagues = f.readlines()
        f.close()

    lineno = 0
    fileno = 0

    for league in leagues:
        seasons = GetSeasons(league)
        leagueval = league.replace("\n", "")
        leagueval = leagueval.replace("\r", "")
        league = leagueval
        for season in seasons:
            lineno, fileno = getTransfersForLeagueSeason(league, str(season), 's', lineno, fileno)
            lineno, fileno = getTransfersForLeagueSeason(league, str(season), 'w', lineno, fileno)
            print "Done for " + league + " for season " + season + "\n"
            print "\n****\n"


# createData()
lineno = 0
fileno = 0
league = 'https://www.transfermarkt.com/oberliga-nofv-sud-bis-07-08-/transfers/wettbewerb/OL4'
#lineno, fileno = getTransfersForLeagueSeason(league, str(1994), 'w', lineno, fileno)
for i in range(1870,2004,1):
    lineno, fileno = getTransfersForLeagueSeason(league, str(i), 's', lineno, fileno)
    print "Done for " + str(i) + " season of " + league
    lineno, fileno = getTransfersForLeagueSeason(league, str(i), 'w', lineno, fileno)
    print "Done for " + str(i) + " season of " + league





