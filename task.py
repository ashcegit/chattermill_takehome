import csv
from requests_ratelimiter import LimiterSession
from dateutil import parser
from time import sleep
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk import tokenize
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np

### Uncomment to download required corpora/lexicons/models on first time running
# nltk.download('punkt')
# nltk.download('vader_lexicon')

session=LimiterSession(per_second=1)

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

sentiments=[
    "negative",
    "neutral",
    "positive",
    "compound"
]

categories_to_write=categories.copy()

categories_to_write.insert(5,"formatted_date")
categories_to_write.insert(6,"year")

categories_to_write.extend(sentiments)

csv_records=[]

csv_records.insert(0,categories_to_write)

with open('guardian_data.csv','w',newline='') as file:
    writer=csv.writer(file)
    writer.writerows(csv_records)

from_date="{}-{}-{}".format("2016","01","01")

### limit pages requested
max_page_num=10
num_pages=min(max_page_num,session.get('https://content.guardianapis.com/search?q=brexit%20OR%20election&from-date={}&order-by=newest&page-size=50&api-key=44c54c3b-1bb5-4b01-9f06-7ea0496ca617'.format(from_date)).json()['response']['pages'])

for page_num in range(1,num_pages+1):
    csv_records=[]
    response=session.get('https://content.guardianapis.com/search?q=brexit%20OR%20election&from-date={}&order-by=newest&page={}&show-blocks=body&show-fields=wordcount&page-size=50&api-key=44c54c3b-1bb5-4b01-9f06-7ea0496ca617'.format(from_date,page_num)).json()['response']

    results=response['results']

    for result in results:
        if int(result['fields']['wordcount'])<200: continue

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

            corpus=result['blocks']['body'][0]['bodyTextSummary']
            sentences=tokenize.sent_tokenize(corpus)

        article_sentiment=np.empty((0,4))

        for sentence in sentences:
            sentence_sentiment=np.array([])
            sia=SentimentIntensityAnalyzer()
            sentiment_dict=sia.polarity_scores(sentence)
            for sentiment_key in sentiment_dict:
                sentence_sentiment=np.append(sentence_sentiment,sentiment_dict[sentiment_key])
            
            article_sentiment=np.append(article_sentiment,np.array([sentence_sentiment]),axis=0)

        avg_article_sentiment=article_sentiment.mean(axis=0)
        csv_entry.extend(avg_article_sentiment.tolist())

        csv_records.append(csv_entry)

    with open('guardian_data.csv','a',newline='') as file:
        writer=csv.writer(file)
        writer.writerows(csv_records)

