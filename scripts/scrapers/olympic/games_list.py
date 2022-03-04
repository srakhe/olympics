from bs4 import BeautifulSoup


class GamesList:

    def __init__(self, data_path, url, scrape_utils):
        self.url = url
        self.data_path = data_path
        self.scrape_utils = scrape_utils

    def scraper(self):
        html_data = self.scrape_utils.get_webpage_data(path=self.data_path, name="games.html")
        if not html_data:
            return
        bs_parser = BeautifulSoup(html_data, "html.parser")
        game_headers = bs_parser.find_all("h3")
        pos = 0
        games = {}
        for index, table in enumerate(bs_parser.find_all("table")):
            if index == 2:
                break
            games[game_headers[pos].text] = []
            for each_row in table.find_all("tr"):
                data_list = each_row.find_all("td")
                if len(data_list) > 0:
                    temp = data_list[0].find('a')
                    game_data = {}
                    if temp:
                        game_data["edition_code"] = temp['href'].split('/')[-1]
                        game_data["edition"] = temp.text
                    game_data["year"] = data_list[1].text
                    game_data["city"] = data_list[2].text
                    game_data["country_code"] = data_list[3].find("img")["src"].split("/")[-1].split(".")[0]
                    game_data["timeline"] = data_list[6].text
                    games[game_headers[pos].text].append(game_data)
            pos += 1
        return games

    def run_scrape(self, do_fetch):
        print("Running games list data scraper.")
        webpage_scraped = True
        if do_fetch:
            webpage_scraped = self.scrape_utils.fetch_webpage(page_url=self.url, path=self.data_path, name="games.html")
        if webpage_scraped:
            games_data = self.scraper()
            for each_game, each_game_data in games_data.items():
                self.scrape_utils.create_csv(data=each_game_data, path=self.data_path + "/games",
                                             name=f"{each_game.lower()}.csv")
        print("Completed games list data scraper.")
