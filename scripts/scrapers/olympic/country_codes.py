import requests
from bs4 import BeautifulSoup
import pandas as pd


class CountryCodes:

    def __init__(self, data_path, url):
        self.url = url
        self.data_path = data_path

    def fetch_url(self):
        html = requests.get(self.url)
        with open(f"{self.data_path}/countries.html", "w+") as htmlFile:
            htmlFile.write(html.text)

    def get_data(self):
        with open(f"{self.data_path}/countries.html", "r+") as htmlFile:
            html = htmlFile.read()
        bs_parser = BeautifulSoup(html, "html.parser")
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

    def create_csv(self, country_codes, country_names):
        data = {"country_code": country_codes, "country_name": country_names}
        df = pd.DataFrame(data=data, index=None)
        df.to_csv(f"{self.data_path}/countries.csv")

    def run_scrape(self):
        print("Running country codes data scraper.")
        self.fetch_url()
        codes, names = self.get_data()
        self.create_csv(codes, names)
        print("Completed country codes data scraper.")
