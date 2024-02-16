import requests, csv
from dateutil import parser
from time import sleep

response=requests.get('https://content.guardianapis.com/search?q=brexit&show-blocks=body&show-fields=wordcount&api-key=44c54c3b-1bb5-4b01-9f06-7ea0496ca617').json()

result=response['response']['results'][0]

print(result['blocks']['body'][0]['bodyTextSummary'])

