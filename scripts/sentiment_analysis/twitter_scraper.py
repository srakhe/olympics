import snscrape.modules.twitter as sntwitter
import pandas as pd


class TwitterScraper:

    def __init__(self, data_path):
        self.data_path = data_path
        self.twitter_list = []
        self.tweets_df = None

    def convert_to_pd(self):
        self.tweets_df = pd.DataFrame(self.twitter_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

    def get_twitter_dataframe(self):
        return self.tweets_df

    def save_data(self):
        self.tweets_df.to_csv(self.data_path + "/tweets_data.csv")

    def scrape(self, start, end):
        for i, tweet in enumerate(
                sntwitter.TwitterSearchScraper(f'Olympics since:{start} until:{end}').get_items()):
            if i > 10:
                break
            self.twitter_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username])
        self.convert_to_pd()
        self.save_data()
