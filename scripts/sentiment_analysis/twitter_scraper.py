import snscrape.modules.twitter as sntwitter
import pandas as pd


class TwitterScraper:

    def __init__(self):
        self.twitter_list = []
        self.tweets_df = None

    def convert_to_pd(self):
        self.tweets_df = pd.DataFrame(self.twitter_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
        return self.tweets_df

    def get_twitter_dataframe(self):
        return self.tweets_df

    def scrape(self, num_tweets, country, start, end):
        for i, tweet in enumerate(
                sntwitter.TwitterSearchScraper(f'olympics near:{country} since:{start} until:{end}').get_items()):
            if i > num_tweets:
                break
            self.twitter_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username])
        data = self.convert_to_pd()
        return data
