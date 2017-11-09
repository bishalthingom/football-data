from os import listdir
from os import chdir
import gzip
import magic
import codecs
from subprocess import call
#call("rm -rf /home/bishal/Desktop/broken-links/*", shell=True)
cachedir = "/home/bishal/.cache/mozilla/firefox/mw7he6gs.default/cache2/entries/"
files = listdir(cachedir)

for file in files:
    if "gzip" in magic.from_file(cachedir + file):
        command = "mv " + cachedir + file + " " + cachedir + file + ".gz"
        result = call(command, shell=True)
        command = "gunzip " + cachedir + file + ".gz"
        result = call(command, shell=True)
        f = open(cachedir + file, 'r')
        data = f.readlines()
        if "playerTableStats" in data[0]:
            print file + "  " + data[0]