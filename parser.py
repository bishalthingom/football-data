# coding: utf-8
import json
from pprint import pprint

output = open('players_data.csv','a+')
# input = 'trial.txt'
input = 'players_data.txt'
with open(input) as data_file:
    data_lines = data_file.readlines()
    for line in data_lines:
        data = json.loads(line)
        records = len(data["playerTableStats"])
        for i in range(0,records,1):
            stringval = ""
            for key, value in data["playerTableStats"][i].items():
                try:
                    value = value.encode('utf-8')
                    value = value.replace(',','-')
                    stringval += value
                except:
                    value = str(value)
                    value = value.replace(',','-')
                    stringval += value
                if key != 'passSuccess':
                    stringval += ','
            #print stringval
            output.write(stringval + '\n')
#print len(data)
output.close()