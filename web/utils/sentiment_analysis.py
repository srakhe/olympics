import pandas as pd
import os
from scripts.sentiment_analysis.twitter_sentiment import TwitterSentiment


class SentimentAnalysis:

    def __init__(self, data_path, web_data_path):
        self.data_path = data_path
        self.web_data_path = web_data_path
        self.tw_sentiment = None

    def get_olympic_options(self):
        games_df = pd.read_csv(f"{self.data_path}/games.csv")
        games_df = games_df[games_df["year"] >= 2004]
        games_df = games_df[games_df["year"] <= 2022]
        games_df["options"] = "[" + games_df["Type"] + "] " + games_df["year"].astype(str) + " in " + games_df[
            "city"].astype(str) + ", " + games_df["country_code"].astype(str)
        games_options = games_df["options"].to_list()
        return games_options

    def run_analysis(self, game_for):
        self.tw_sentiment = TwitterSentiment(num_tweets=50, country=None, start=None, end=None)

    def get_analysis(self):
        pass

    def get_last_run(self):
        pass
