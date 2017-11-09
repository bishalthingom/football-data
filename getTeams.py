import os
import sys
from os import listdir
from os import chdir
import gzip
import magic
import codecs
from  subprocess32 import call
from subprocess32 import check_output

import re
import time
from HTMLParser import HTMLParser

def clearCache():
    command = "rm -rf /home/bishal/.cache/mozilla/firefox/mw7he6gs.default/cache2/entries/*"
    result = call(command, shell=True)
    time.sleep(1)

def firefox(url):
    command = "firefox " + url + " &"
    os.system(command)
    time.sleep(20)
    command = "pkill firefox -f"
    os.system(command)

def readCache():
    cachedir = "/home/bishal/.cache/mozilla/firefox/mw7he6gs.default/cache2/entries/"
    output = open('seasons_info.txt','a+')
    failed = open('failed.txt','a+')
    files = listdir(cachedir)
    filelist = []
    stop = False
    for file in files:
        if "gzip" in magic.from_file(cachedir + file):
            command = "mv " + cachedir + file + " " + cachedir + file + ".gz"
            result = call(command, shell=True)
            command = "gunzip " + cachedir + file + ".gz"
            result = call(command, shell=True)
            filelist.append(cachedir + file)

    return filelist

def getTeams(file,season):
    h = HTMLParser()
    f = open(file,'r')
    data = f.readlines()

    search_pattern = 'DataStore.prime\(\'streaks\', \{  stageId:[0-9]*, idx:[0-9]*, field: \'overall\', type: \'season\''
    search_end_pattern = 'DataStore.prime\(\'history\''
    stage_pattern_start = '<span><select id="stages" name="stages">'
    stage_pattern_end = '</select></span>'
    element_pattern = '\[(.*?)\]'
    flag = False
    stage_flag = False
    flag_found = False

    output = open('teams.txt','a+')
    #failed = open('failed.txt','a+')

    for line in data:
        if re.search(search_pattern,line) and not flag:
            flag_found = True
            flag = True
            element = re.findall(element_pattern,line)
            element = element[0]
            values = element.split(',')
            output.write(values[1] + "," + values[2] + "," + values[27] + "," + values[28] + '\n')
        elif flag and re.search(search_end_pattern,line):
            flag = False
        elif flag:
            element = re.findall(element_pattern,line)
            if element.__len__() > 0:
                element = element[0]
                values = element.split(',')
                output.write(values[1] + "," + values[2] + "," + values[27] + "," + values[28] + '\n')
        # elif not stage_flag and re.search(stage_pattern_start,line):
        #     stage_flag = True
        #     flag_found = True
        #     stage_pattern = '>(.*?)<'
        #     stageval = re.findall(stage_pattern,line)
        #     stageval = stageval[stageval.__len__()-1]
        #     stageval = stageval.replace(' ','-')
        #     url_pattern = 'value="(.*?)"'
        #     url_stage = re.findall(url_pattern,line)
        #     url_stage = url_stage[0]
        #     failed.write(h.unescape(url_stage) + '\n')
        # elif stage_flag and re.search(stage_pattern_end, line):
        #     stage_flag = False
        # elif stage_flag:
        #     stage_pattern = '>(.*?)<'
        #     stageval = re.findall(stage_pattern,line)
        #     stageval = stageval[stageval.__len__()-1]
        #     stageval = stageval.replace(' ','-')
        #     url_pattern = 'value="(.*?)"'
        #     url_stage = re.findall(url_pattern,line)
        #     url_stage = url_stage[0]
        #     failed.write(h.unescape(url_stage) + '\n')

    # failed.close()
    output.close()
    return flag_found


seasonsfile = open('pending.txt','r')
seasons = seasonsfile.readlines()

for season in seasons:
    seasonval = season.replace("\n", "")
    seasonval = seasonval.replace("\r", "")
    flag = False
    url = "https://www.whoscored.com" + seasonval
    print "Retrieving " + seasonval
    clearCache()
    firefox(url)

    files = readCache()
    failed = open('failed.txt','a+')

    for file in files:
        result = getTeams(file,season)
        if result:
            flag = True
            break

    if not flag:
        failed.write(seasonval + '\n')

    failed.close()

    time.sleep(10)

