from bs4 import BeautifulSoup


class MedalsCounts:

    def __init__(self, data_path, url, scrape_utils):
        self.url = url
        self.data_path = data_path
        self.scrape_utils = scrape_utils

    def scraper(self):
        html_data = self.scrape_utils.get_webpage_data(path=self.data_path, name="medals.html")
        if not html_data:
            return
        bs_parser = BeautifulSoup(html_data, "html.parser")
        medals_table = bs_parser.find("table")
        data = []
        for tr in medals_table.find_all("tr"):
            medals_data = {}
            data_list = tr.find_all("td")
            if data_list:
                medals_data["country"] = data_list[0].text
                medals_data["country_code"] = data_list[1].text.replace(" ", "")
                medals_data["gold"] = data_list[2].text.replace(" ", "")
                medals_data["silver"] = data_list[3].text.replace(" ", "")
                medals_data["bronze"] = data_list[4].text.replace(" ", "")
                medals_data["total"] = data_list[5].text.replace(" ", "")
                data.append(medals_data)
        return data

    def run_scrape(self, do_fetch):
        print("Running medals count data scraper.")
        webpage_scraped = True
        if do_fetch:
            webpage_scraped = self.scrape_utils.fetch_webpage(page_url=self.url, path=self.data_path,
                                                              name="medals.html")
        if webpage_scraped:
            medals_data = self.scraper()
            self.scrape_utils.create_csv(data=medals_data, path=self.data_path,
                                         name=f"medals.csv")
        print("Completed medals count data scraper.")
