from bs4 import BeautifulSoup


class CountryCodes:

    def __init__(self, data_path, url, scrape_utils):
        self.url = url
        self.data_path = data_path
        self.scrape_utils = scrape_utils

    def scraper(self):
        html_data = self.scrape_utils.get_webpage_data(path=self.data_path, name="countries.html")
        if not html_data:
            return
        bs_parser = BeautifulSoup(html_data, "html.parser")
        countries_table = bs_parser.find("table").find("tbody")
        is_code = True
        country_codes = []
        country_names = []
        for each_row in countries_table.find_all("tr"):
            for each_data in each_row.find_all("td"):
                if each_data.a:
                    countries_data = each_data.text
                    if is_code:
                        country_codes.append(countries_data)
                        is_code = False
                    else:
                        country_names.append(countries_data)
                        is_code = True
        return country_codes, country_names

    def run_scrape(self, do_fetch):
        print("Running country codes data scraper")
        webpage_scraped = True
        if do_fetch:
            webpage_scraped = self.scrape_utils.fetch_webpage(page_url=self.url, path=self.data_path,
                                                              name="countries.html")
        if webpage_scraped:
            codes, names = self.scraper()
            data = {"country_code": codes, "country_name": names}
            self.scrape_utils.create_csv(data=data, path=self.data_path, name="countries.csv")
        print("Completed country codes data scraper")
