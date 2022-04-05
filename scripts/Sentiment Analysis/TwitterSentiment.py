#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from transformers import pipeline
from TwitterScrapper import TwitterScrapper


# In[2]:


class TwitterSentiment:
    def __init__(self, twitter_Dataframe):
        self.twitter_df= twitter_Dataframe        
        self.perform_sentiment_analysis()
    
    def perform_sentiment_analysis(self):
        sentiment_classifier = pipeline('sentiment-analysis')  #huggging face transformer used to perform NLP
        self.results = sentiment_classifier(self.twitter_df['Text'].tolist())
        self.tune_results()
#         for result in self.results:
#             print(f"label: {result['label']}, with score: {round(result['score'], 4)}")
  
#     function used for hyper parameter tuning 
    def tune_results(self): 
        results_df = pd.DataFrame(self.results,columns=['label','score'])
        self.strong_opinion_df=results_df[results_df['score']>=0.7]
        self.other_opinion_df=results_df[results_df['score']<0.7]
    
    def get_strong_opinion_count(self):
        return self.strong_opinion_df.groupby('label').count().reset_index().rename(columns={'label':'People View', 'score': 'No Of People'})
    
    def get_other_opinion_count(self):
        return self.other_opinion_df.groupby('label').count().reset_index().rename(columns={'label':'People View', 'score': 'No Of People'})


# In[3]:


tweet_Df = TwitterScrapper().get_twitter_dataframe()
twitter_sentiment_analysis=TwitterSentiment(tweet_Df)
twitter_sentiment_analysis.get_strong_opinion_count()


# In[61]:


twitter_sentiment_analysis.get_other_opinion_count()

