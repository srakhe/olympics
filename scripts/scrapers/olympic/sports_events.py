from bs4 import BeautifulSoup


class SportsEvents:

    def __init__(self, data_path, url, scrape_utils):
        self.url = url
        self.data_path = data_path
        self.scrape_utils = scrape_utils

    def sports_scraper(self):
        html_data = self.scrape_utils.get_webpage_data(path=self.data_path, name="sports.html")
        if not html_data:
            return
        bs_parser = BeautifulSoup(html_data, "html.parser")
        sports_table = bs_parser.find("table")
        data = []
        for tr in sports_table.find_all("tr"):
            sport_data = {}
            data_list = tr.find_all("td")
            sport_data["sport_code"] = data_list[0].text
            sport_data["sport_disc"] = data_list[1].text
            sport_data["sport_name"] = data_list[2].text
            sport_data["sport_games"] = data_list[3].text
            sport_data["continued"] = "yes" if tr.find('span', {'class': 'glyphicon-ok'}) else "no"
            data.append(sport_data)
        return data

    def events_data(self):
        pass

    def run_scrape(self, do_fetch):
        print("Running sports and events list data scraper.")
        webpage_scraped = True
        if do_fetch:
            webpage_scraped = self.scrape_utils.fetch_webpage(page_url=self.url, path=self.data_path,
                                                              name="sports.html")
        if webpage_scraped:
            sports_data = self.sports_scraper()
            self.scrape_utils.create_csv(data=sports_data, path=self.data_path, name="sports.csv")
            events_data = self.events_data()
        print("Completed games list data scraper.")
