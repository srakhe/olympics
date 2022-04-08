import pandas as pd


class SentimentAnalysis:

    def __init__(self, data_path):
        self.data_path = data_path

    def get_olympic_options(self):
        games_df = pd.read_csv(f"{self.data_path}/games.csv")
        games_df = games_df[games_df["year"] >= 2004]
        games_df = games_df[games_df["year"] <= 2022]
        games_df["options"] = "[" + games_df["Type"] + "] " + games_df["year"].astype(str) + " in " + games_df[
            "city"].astype(str) + ", " + games_df["country_code"].astype(str)
        games_options = games_df["options"].to_list()
        return games_options

    def run_analysis(self):
        pass

    def get_analysis(self):
        pass
