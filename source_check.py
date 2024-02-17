import csv
from requests_ratelimiter import LimiterSession
from newsapi import NewsApiClient
import newspaper as news
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

news_api_key="7ab38518b3114edb91a15c568fae8b46"

source_finder=NewsApiClient(news_api_key)

response=source_finder.get_sources(country="gb")

print(response)

