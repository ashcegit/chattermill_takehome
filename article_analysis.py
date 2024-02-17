import csv
from const import CATEGORIES,SENTIMENTS,API_KEY
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

def run_query(
    session,
    query: str,
    from_date=None,
    to_date=None,
    page_num=None
) -> dict:
    """
    Runs guardian api call. Can be used with custom session object

    :param: session: Session object, either from requests package or an analogue
    :param: query: HTML encoded string that can include ANDs and ORs etc.
    :param: from_date: dd-mm-yyyy formatted string
    :param: to_date: dd-mm-yyyy formatted string
    :param: page_num: specified page of results to ask for

    :returns: python dict of returned json
    """

    get_string='https://content.guardianapis.com/search?q={}{}{}&order-by=newest&show-blocks=body{}&show-fields=wordcount&page-size=50&api-key={}'.format(
                    query,
                    "&from-date={}".format(from_date) if from_date!=None else "",
                    "&to-date={}".format(to_date) if to_date!=None else "",
                    "&page={}".format(page_num) if page_num!=None else "",
                    API_KEY
                )
    
    response=session.get(get_string).json()

    return response

def process_article(
    article: dict
) -> list:
    """
    Processes article json into list ready to be added to csv document.
    This includes extracting metadata from api response and performing sentiment analysis on body text

    :param: article: dict object of article specific data

    :returns: List of metadata
    """

    if int(article['fields']['wordcount'])<200 or article['pillarName']!="News": return

    csv_entry=[]
    for category in CATEGORIES:
        if category=="webPublicationDate":
            #get datetime and extract time divisions
            parsed_date=parser.parse(article[category])
            formatted_date_string="{}/{}/{}".format(parsed_date.day,parsed_date.month,parsed_date.year)
            year_string=str(parsed_date.year)

            #append raw date, formatted date and year
            csv_entry.append(article[category])
            csv_entry.append(formatted_date_string)
            csv_entry.append(year_string)

        elif category=="wordcount":
            #wordcount is hidden under extra fields key
            csv_entry.append(article['fields']['wordcount'])
            
        else:
            csv_entry.append(article[category])

        corpus=article['blocks']['body'][0]['bodyTextSummary']
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

    return csv_entry   
        
def write_page(
    response: dict,
    filename: str
) -> None:
    """
    Processes and writes a page of results to a csv file

    :param: response: response dict containing many articles
    :param: file_name: name of csv file
    """
    csv_records=[]

    articles=response['results']

    for article in articles:
        csv_records.append(process_article(article))

    with open(filename,'a',newline='') as file:
        writer=csv.writer(file)
        writer.writerows(csv_records)

def analyse(
    query: str,
    filename,
    from_date,
    to_date,
    max_pages=10 #Will process up to 500 articles by default 
) -> bool:

    session=LimiterSession(per_second=1)

    categories_to_write=CATEGORIES.copy()

    categories_to_write.insert(5,"formatted_date")
    categories_to_write.insert(6,"year")

    categories_to_write.extend(SENTIMENTS)

    csv_records=[]

    csv_records.insert(0,categories_to_write)

    with open(filename,'w',newline='') as file:
        writer=csv.writer(file)
        writer.writerows(csv_records)

    first_call=run_query(
        session,
        query,
        from_date=from_date,
        to_date=to_date,
    )
    
    first_response=first_call['response']

    write_page(first_response,filename)

    num_pages=first_response['pages']

    num_pages=min(max_pages,num_pages)
    
    if num_pages>1:
        for page_num in range(2,num_pages+1):
            response=run_query(
                session,
                query,
                from_date=from_date,
                to_date=to_date,
                page_num=page_num
            )['response']

            write_page(response,filename)

    return True

if __name__=='__main__':
    dummy_query="brexit%20OR%20election"
    filename="test.csv"
    from_date=None
    to_date=None
    max_pages=2

    analyse(
        query=dummy_query,
        filename=filename,
        from_date=from_date,
        to_date=to_date,
        max_pages=max_pages
    )
    

