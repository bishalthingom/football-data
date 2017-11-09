import json
from haralyzer import HarParser

with open('/home/bishal/Desktop/test_har.har','r') as f:
    har_parser = HarParser(json.loads(f.read()))

for page in har_parser.pages:
    for entry in page.entries:
        if "whoscored" in entry['request']['url']:
            print entry['request']['url']
            for value in entry['request']['headers']:
                print value['name'] + ", " + value['value']
            print "\n\r"
