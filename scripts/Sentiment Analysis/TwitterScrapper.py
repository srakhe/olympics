#!/usr/bin/env python
# coding: utf-8

# In[28]:


import nest_asyncio
import snscrape.modules.twitter as sntwitter
import pandas as pd

nest_asyncio.apply()


# In[50]:


class TwitterScrapper :
    
    def __init__(self):
        self.twitter_list=[]
        self.scrape()
        
    def scrape(self):
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper('Olympics since:2021-07-17 until:2021-07-23').get_items()):
            if i>10:
                break
            self.twitter_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username])
        
        self.convert_to_pd()
    

    def convert_to_pd(self):
        self.tweets_df = pd.DataFrame(self.twitter_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
#         print(self.tweets_df)
    
    def get_twitter_dataframe(self):
        return self.tweets_df

        


# In[51]:


if __name__ == "__main__":
    tweet=TwitterScrapper()
    print(tweet.get_twitter_dataframe())

