import requests, csv
from dateutil import parser
from time import sleep

from_date="{}-{}-{}".format("2016","01","01")

response=requests.get('https://content.guardianapis.com/search?q=brexit%20OR%20election&from-date={}&order-by=newest&page-size=50&api-key=44c54c3b-1bb5-4b01-9f06-7ea0496ca617'.format(from_date)).json()['response']

print(response['pages'])

# result=response['response']['results'][0]

# body_corpus=result['blocks']['body'][0]['bodyTextSummary']

