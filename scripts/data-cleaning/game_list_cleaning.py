import pandas as pd


class GamesListCleaning:

    def __init__(self, filePath, type_of_game):
        self.olympics_games = pd.read_csv(filePath)
        self.type_of_game = type_of_game

    def pre_process_data(self):
        k = 0
        start_date = []
        end_date = []
        start_month = []
        for row in self.olympics_games.iterrows():
            timeline = row[1][-1].split('–')
            if len(timeline) >= 2:
                start_date.append(timeline[0].strip())
                end_date.append(timeline[1].strip())
                start_month.append(timeline[1].split(' ')[-1].strip())
            elif len(timeline) < 2:
                start_date.append('NA')
                end_date.append('NA')
                start_month.append('NA')
            k = k + 1
        self.olympics_games['Type'] = self.type_of_game
        self.olympics_games['start_date'] = start_date
        self.olympics_games['end_date'] = end_date
        self.olympics_games['start_month'] = start_month

    def post_process_data(self):
        start_date = []
        for row in self.olympics_games.iterrows():
            if (len(row[1]['start_date']) <= 2) and (row[1]['start_date'] != 'NA'):
                start_date.append(row[1]['start_date'] + ' ' + row[1]['start_month'])
            else:
                start_date.append(row[1]['start_date'])
        self.olympics_games['start_date'] = start_date
        self.olympics_games.drop(columns=['start_month'], inplace=True)

    def run(self):
        self.pre_process_data()
        self.post_process_data()
        return self.olympics_games


if __name__ == "__main__":
    summer = GamesListCleaning(filePath="../scrapers/olympic/data/games/summer.csv",
                               type_of_game="Summer")
    winter = GamesListCleaning(filePath="../scrapers/olympic/data/games/winter.csv",
                               type_of_game="Winter")
    summer_df = summer.run()
    winter_df = winter.run()
    games_list = pd.concat([summer_df, winter_df], ignore_index=True)
    games_list.to_csv("data/games.csv")
