import requests, csv
from dateutil import parser

response=requests.get('https://content.guardianapis.com/search?q=brexit%20OR%20elections&api-key=44c54c3b-1bb5-4b01-9f06-7ea0496ca617')

results=response.json()['response']['results']

results.sort(key=lambda x: x['webPublicationDate'],reverse=True)

for result in results:
    print(parser.parse(result['webPublicationDate']))

# raw_date=results[0]['webPublicationDate']
# parsed_date=parser.parse(raw_date)

# print(parsed_date)

# csv_records=[]

# categories=[
#     "id",
#     "type",
#     "sectionId",
#     "sectionName",
#     "webPublicationDate",
#     "webTitle",
#     "webUrl",
#     "apiUrl",
#     "isHosted",
#     "pillarId",
#     "pillarName",
#     "Wordcount"
# ]

# for result in results:
#     csv_entry=[]
#     for category in categories:
#         csv_entry.append(result[category])
#     csv_records.append(csv_entry)