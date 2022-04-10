import pandas as pd
from datetime import datetime


class PredictHost:

    def __init__(self, data_path, web_data_path):
        self.data_path = data_path
        self.web_data_path = web_data_path
        self.eco_indicators = ["Debt", "Employment", "Exchange Rate", "Foreign Investments", "GDP Growth",
                               "GDP", "Gross National Expenditure", "Import Goods", "Inflation", "Revenue",
                               "Stocks", "Tax Revenue", "Tourism Arrival", "Trade", "Unemployment"]

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

    def get_forecasts(self, country, year):
        year = int(year)
        years = [i for i in range(year, (year - 5), -1)]
        time_series_data = f"{self.data_path}/time_series"
        forecasted_values = {}
        for indicator in self.eco_indicators:
            country_eco_df = pd.read_csv(f"{time_series_data}/{indicator}.csv")
            country_eco_df = country_eco_df[country_eco_df["Unnamed: 0"] == str(country)]
            forecasted_values[indicator] = []
            for each_year in years:
                each_year = str(each_year)
                indicator_value = country_eco_df[each_year].to_list()
                if indicator_value:
                    forecasted_values[indicator].append(indicator_value[0])
                else:
                    forecasted_values[indicator].append(None)
        return forecasted_values
