import pandas as pd
from datetime import datetime


class PredictHost:

    def __init__(self, data_path, web_data_path):
        self.data_path = data_path
        self.web_data_path = web_data_path

    def get_years(self):
        this_year = datetime.today().year
        if not 2022 <= this_year < 2050:
            this_year = 2022
        years = [i for i in range(this_year + 1, 2051)]
        return years

    def get_countries(self):
        countries_df = pd.read_csv(f"{self.data_path}/countries.csv")
        country_codes = countries_df["country_code"]
        country_names = countries_df["country_name"]
        countries = {}
        for code, name in zip(country_codes, country_names):
            countries[code] = name
        return countries
