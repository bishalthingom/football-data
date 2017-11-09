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
    files = listdir(cachedir)
    filelist = []
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

    flag_found = False

    output = open('players_data.txt','a+')
    #failed = open('failed.txt','a+')

    if '"playerTableStats"' in data[0]:
        flag_found = True
        output.write(data[0] + "\n")

    # failed.close()
    output.close()
    return flag_found


stagesfile = open('pending.txt','r')
stages = stagesfile.readlines()

for stage in stages:
    stageval = stage.replace("\n", "")
    stageval = stageval.replace("\r", "")
    flag = False

    print "Retrieving " + stageval
    clearCache()
    firefox(stageval)

    files = readCache()
    failed = open('failed.txt','a+')

    for file in files:
        result = getTeams(file,stageval)
        if result:
            flag = True
            break

    if not flag:
        failed.write(stageval + '\n')

    failed.close()

    time.sleep(10)

