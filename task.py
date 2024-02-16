import requests, csv

response=requests.get('https://content.guardianapis.com/search?q=brexit%20OR%20elections&api-key=44c54c3b-1bb5-4b01-9f06-7ea0496ca617')

results=response.json()['response']['results']

for result in results:
    print(result)