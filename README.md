# Chattermill take-home

## Description
A small mock-up of a Flask webapp that takes a guardianAPI-compliant query and averages a sentiment analysis over a loosely given number of articles optionally within a time-period.

You can use this to compare neutrality of language between different individual or combinations of topics. To avoid opinion pieces and other non-news articles, only those specified as news by the guardian's API are selected. Due to this, you may end up with less than 50 articles returned per page requested.

Underneath the chart of displayed sentiment analysis, you can see a table of all the articles used, with clickable links and their API analogues.

## Setup
To create and activate the necessary conda environment, run:

conda env create -f environment.yml

conda activate chattermill

To start up the app, run:

python app.py

Then navigate to http://localhost:5000 in your browser of choice
