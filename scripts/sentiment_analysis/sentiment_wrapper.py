#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
from datetime import datetime, timedelta
from scripts.sentiment_analysis.twitter_sentiment import TwitterSentiment
from plotly.subplots import make_subplots


class SentimentWrapper:
    def __init__(self, selected_olympic_info):
        self.tw_sentiment_before_oly_world_results = None
        self.tw_sentiment_after_oly_world_results = None
        self.tw_sentiment_after_oly_host_country = None
        self.tw_sentiment_before_oly_host_country = None
        self.selected_olympics = None
        self.selected_country_name = None
        self.selected_year = None
        self.countries_df = pd.read_csv('../../data/countries.csv')
        self.olympic_games_df = pd.read_csv('../../data/games.csv')
        self.selected_olympic_info = selected_olympic_info
        self.tw_sentiment = None

    def extract_info(self):
        selected_country_code = self.selected_olympic_info.split(" ")[4]
        self.selected_year = int(self.selected_olympic_info.split(" ")[1])
        self.selected_country_name = \
            self.countries_df[self.countries_df['country_code'] == selected_country_code]['country_name'].tolist()[0]
        self.selected_olympics = self.olympic_games_df[self.olympic_games_df['country_code'] == selected_country_code]
        self.selected_olympics = self.selected_olympics[self.selected_olympics['year'] == self.selected_year]

    def generate_date_range_for_sentiment_analysis(self):
        start_date = self.selected_olympics['start_date'].tolist()[0]
        end_date = self.selected_olympics['end_date'].tolist()[0]
        start_date = start_date + ' ' + str(self.selected_year)
        if len(end_date) <= 2:
            end_date = end_date + ' ' + str(self.selected_year)

        start_date = datetime.strptime(start_date, '%d %B %Y')
        end_date = datetime.strptime(end_date, '%d %B %Y')
        one_week_before_start_date = start_date - timedelta(days=7)
        one_week_after_end_date = end_date + timedelta(days=7)
        start_date = str(start_date).split(' ')[0]
        one_week_before_start_date = str(one_week_before_start_date).split(' ')[0]
        end_date = str(end_date).split(' ')[0]
        one_week_after_end_date = str(one_week_after_end_date).split(' ')[0]
        num_of_tweets = 1000000
        self.tw_sentiment_before_oly_host_country = TwitterSentiment(num_of_tweets, self.selected_country_name,
                                                                     one_week_before_start_date,
                                                                     start_date)
        fig1 = self.tw_sentiment_before_oly_host_country.run()

        self.tw_sentiment_after_oly_host_country = TwitterSentiment(num_of_tweets, self.selected_country_name,
                                                                    end_date,
                                                                    one_week_after_end_date)
        fig2 = self.tw_sentiment_after_oly_host_country.run()

        self.tw_sentiment_before_oly_world_results = TwitterSentiment(num_of_tweets, None,
                                                                      one_week_before_start_date,
                                                                      start_date)
        fig3 = self.tw_sentiment_before_oly_world_results.run()

        self.tw_sentiment_after_oly_world_results = TwitterSentiment(num_of_tweets, None,
                                                                     end_date,
                                                                     one_week_after_end_date)
        fig4 = self.tw_sentiment_after_oly_world_results.run()

        fig5 = make_subplots(rows=2, cols=2, print_grid=True,
                             subplot_titles=['Sentiment of the world one week before Olympics',
                                             'Sentiment of the world one week before Olympics',
                                             'Sentiment of ' + self.selected_country_name + ' before '
                                                                                            'Olympics',
                                             'Sentiment of ' + self.selected_country_name + ' after '
                                                                                            'Olympics',
                                             ],
                             specs=[[{"type": "pie"}, {"type": "pie"}], [{"type": "pie"}, {"type": "pie"}]])
        fig5.append_trace(fig3, row=1, col=1)
        fig5.append_trace(fig4, row=1, col=2)
        fig5.append_trace(fig1, row=2, col=1)
        fig5.append_trace(fig2, row=2, col=2)
        fig5.write_html(self.selected_olympic_info + '.html')

    def run(self):
        self.extract_info()
        self.generate_date_range_for_sentiment_analysis()


if __name__ == "__main__":
    sentiment_wrapper = SentimentWrapper('[Summer] 2020 in Tokyo, JPN')
    sentiment_wrapper.run()
