import requests, csv
from dateutil import parser
from time import sleep

response=requests.get('https://content.guardianapis.com/search?q=brexit%20OR%20elections&show-fields=wordcount&api-key=44c54c3b-1bb5-4b01-9f06-7ea0496ca617')

results=response.json()['response']['results']

##Sorting by date
results.sort(key=lambda x: x['webPublicationDate'],reverse=True)

csv_records=[]

categories=[
    "id",
    "type",
    "sectionId",
    "sectionName",
    "webPublicationDate",
    "webTitle",
    "webUrl",
    "apiUrl",
    "isHosted",
    "pillarId",
    "pillarName",
    "wordcount"
]

for result in results:
    if int(result['fields']['wordcount'])<1000: continue

    csv_entry=[]
    for category in categories:
        if category=="webPublicationDate":
            #get datetime and extract time divisions
            parsed_date=parser.parse(result[category])
            formatted_date_string="{}/{}/{}".format(parsed_date.day,parsed_date.month,parsed_date.year)
            year_string=str(parsed_date.year)

            #append raw date, formatted date and year
            csv_entry.append(result[category])
            csv_entry.append(formatted_date_string)
            csv_entry.append(year_string)

        elif category=="wordcount":
            #wordcount is hidden under extra fields key
            csv_entry.append(result['fields']['wordcount'])
            
        else:
            csv_entry.append(result[category])

    csv_records.append(csv_entry)
    sleep(0.1)

categories.insert(5,"formatted_date")
categories.insert(6,"year")

csv_records.insert(0,categories)

with open('guardian_data.csv','w',newline='') as file:
    writer=csv.writer(file)
    writer.writerows(csv_records)

