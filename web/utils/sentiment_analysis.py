import pandas as pd
from scripts.sentiment_analysis.sentiment_wrapper import SentimentWrapper


class SentimentAnalysis:

    def __init__(self, data_path, web_data_path):
        self.data_path = data_path
        self.web_data_path = web_data_path
        self.num_tweets = 50

    def get_olympic_options(self):
        games_df = pd.read_csv(f"{self.data_path}/games.csv")
        games_df = games_df[games_df["year"] >= 2004]
        games_df = games_df[games_df["year"] <= 2022]
        games_df["options"] = "[" + games_df["Type"] + "] " + games_df["year"].astype(str) + " in " + games_df[
            "city"].astype(str) + ", " + games_df["country_code"].astype(str)
        games_options = games_df["options"].to_list()
        return games_options

    def run_analysis(self, game_for):
        snt_wrapper = SentimentWrapper(selected_olympic_info=game_for, num_tweets=self.num_tweets,
                                       data_path=self.data_path)
        snt_wrapper.run()
