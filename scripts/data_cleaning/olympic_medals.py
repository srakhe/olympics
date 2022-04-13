import os
import pandas as pd

summer_games_data_path = "../scrapers/olympic/data/medals/Olympic Games (Summer)"
winter_games_data_path = "../scrapers/olympic/data/medals/Olympic Games (Winter)"


def perform_preprocessing():
    summer_games = {}
    for file in os.listdir(summer_games_data_path):
        summer_games[file.replace(".csv", "")] = pd.read_csv(summer_games_data_path + "/" + file)

    winter_games = {}
    for file in os.listdir(winter_games_data_path):
        winter_games[file.replace(".csv", "")] = pd.read_csv(winter_games_data_path + "/" + file)
