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

def getTeams(file,url):
    h = HTMLParser()
    f = open(file,'r')
    data = f.readlines()

    stage_pattern_start = '<select id="stageId" name="stageId">'
    stage_pattern_end = '</select>'
    flag = False
    stage_flag = False
    flag_found = False

    output = open('teams_stages.txt','a+')
    #failed = open('failed.txt','a+')

    for line in data:
        if not stage_flag and re.search(stage_pattern_start,line):
            stage_flag = True
            flag_found = True
            stage_pattern = 'value="(.*?)"'
            stageval = re.findall(stage_pattern,line)
            stageval = stageval[0]
            stage_url = url + '?stageId=' + stageval
            output.write(stage_url + '\n')
        elif stage_flag and re.search(stage_pattern_end, line):
            break
        elif stage_flag:
            stage_pattern = 'value="(.*?)"'
            stageval = re.findall(stage_pattern,line)
            stageval = stageval[0]
            stage_url = url + '?stageId=' + stageval
            output.write(stage_url + '\n')

    # failed.close()
    output.close()
    return flag_found


teamsfile = open('team_urls.txt','r')
teams = teamsfile.readlines()

for team in teams:
    teamval = team.replace("\n", "")
    teamval = teamval.replace("\r", "")
    flag = False

    print "Retrieving " + teamval
    clearCache()
    firefox(teamval)

    files = readCache()
    failed = open('failed.txt','a+')

    for file in files:
        result = getTeams(file,teamval)
        if result:
            flag = True
            break

    if not flag:
        failed.write(teamval + '\n')

    failed.close()

    time.sleep(10)

