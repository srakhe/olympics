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
        pos = 0
        bs_parser = BeautifulSoup(html_data, "html.parser")
        for table in bs_parser.find_all("table"):
            pos += 1
            for each_row in table.find_all("tr"):
                data_list = each_row.find_all("td")
                if len(data_list) > 0:
                    temp = data_list[0].find('a')
                    if temp:
                        print(f"edition_code: {temp['href'].split('/')[-1]}")
                        print(f"edition: {temp.text}")
                    print(f"year: {data_list[1].text}")
                    print(f"city: {data_list[2].text}")
                    print(f"country: {data_list[3].text}")
                    print(f"timeline: {data_list[6].text}")
        print(pos)

    def run_scrape(self):
        print("Running games list data scraper.")
        # webpage_scraped = self.scrape_utils.fetch_webpage(page_url=self.url, path=self.data_path, name="games.html")
        # if webpage_scraped:
        if True:
            self.scraper()
            # data = {"country_code": codes, "country_name": names}
            # self.scrape_utils.create_csv(data=data, path=self.data_path, name="games.csv")
        print("Completed games list data scraper.")
