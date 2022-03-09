import snscrape.modules.twitter as sntwitter
import pandas as pd
from transformers import pipeline
import tensorflow as tf


# Creating list to append tweet data to
tweets_list2 = []
# Using TwitterSearchScraper to scrape data and append tweets to list
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('Olympics since:2021-07-17 until:2021-07-23').get_items()):
    if i>10000:
        break
    tweets_list2.append([tweet.date, tweet.id, tweet.content, tweet.username])
# Creating a dataframe from the tweets list above
tweets_df2 = pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
tweets_df2.to_csv('tokyo_before.csv')
sentiment_classifier = pipeline('sentiment-analysis')
results = sentiment_classifier(tweets_df2['Text'].tolist())
results_df = pd.DataFrame(results,columns=['label','score'])
print(results_df.groupby('label').count())
tweets_list2 = []
# Using TwitterSearchScraper to scrape data and append tweets to list
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('Olympics since:2021-07-23 until:2021-08-01').get_items()):
    # print(i)
    # print(tweet.username)
    if i>10000:
        break
    tweets_list2.append([tweet.date, tweet.id, tweet.content, tweet.username])
# Creating a dataframe from the tweets list above
tweets_df2 = pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
tweets_df2.to_csv('tokyo_after.csv')
sentiment_classifier = pipeline('sentiment-analysis')
results = sentiment_classifier(tweets_df2['Text'].tolist())
results_df = pd.DataFrame(results,columns=['label','score'])
results_df.head()
print(results_df.groupby('label').count())
