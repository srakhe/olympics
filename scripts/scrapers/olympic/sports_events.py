from bs4 import BeautifulSoup
import os


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
            sport_data["sport_name"] = data_list[1].text
            sport_data["sport_category"] = data_list[2].text
            sport_data["sport_games"] = data_list[3].text
            sport_data["continued"] = "yes" if tr.find('span', {'class': 'glyphicon-ok'}) else "no"
            data.append(sport_data)
        return data

    def events_scraper(self):
        data = []
        for file in os.listdir(self.data_path + "/sports_pages"):
            page_data = self.scrape_utils.get_webpage_data(path=self.data_path + "/sports_pages", name=file)
            bs_parser = BeautifulSoup(page_data, "html.parser")
            events_table = bs_parser.find_all("table")[-1]
            for tr in events_table.find_all("tr"):
                events_data = {}
                data_list = tr.find_all("td")
                events_data["sport_name"] = file.replace(".html", "")
                if data_list[0].a["href"]:
                    events_data["event_code"] = data_list[0].a["href"].split("/")[-1]
                events_data["event_name"] = data_list[0].text
                events_data["event_category"] = data_list[1].text
                events_data["continued"] = "yes" if tr.find('span', {'class': 'glyphicon-ok'}) else "no"
                data.append(events_data)
        return data

    def run_scrape(self, do_fetch):
        print("Running sports list data scraper")
        webpage_scraped = True
        sports_scraped = False
        sports_data = []
        if do_fetch:
            webpage_scraped = self.scrape_utils.fetch_webpage(page_url=self.url, path=self.data_path,
                                                              name="sports.html")
        if webpage_scraped:
            sports_data = self.sports_scraper()
            self.scrape_utils.create_csv(data=sports_data, path=self.data_path, name="sports.csv")
            sports_scraped = True
        print("Completed sports list data scraper")
        if sports_scraped:
            print("Running events list data scraper")
            all_webpages_scraped = True
            if do_fetch:
                for each_sport in sports_data:
                    sports_code = each_sport["sport_code"]
                    sport_url = f"https://www.olympedia.org/sports/{sports_code}"
                    page_scraped = self.scrape_utils \
                        .fetch_webpage(page_url=sport_url, path=self.data_path + "/sports_pages",
                                       name=f"{each_sport['sport_name'].lower().replace(' ', '_')}.html")
                    if not page_scraped:
                        all_webpages_scraped = False

            if all_webpages_scraped:
                events_data = self.events_scraper()
                self.scrape_utils.create_csv(data=events_data, path=self.data_path, name="events.csv")
        print("Completed events list data scraper")
