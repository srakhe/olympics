import pandas as pd
from datetime import datetime
import pickle
import numpy as np
import plotly.graph_objects as go


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
                    forecasted_values[indicator].append(float(indicator_value[0]))
                else:
                    forecasted_values[indicator].append(float(0))
        return forecasted_values

    def get_predictions(self, forecasted_values):
        predicted_values = {}
        for indicator in self.eco_indicators:
            model = pickle.load(open(f"{self.data_path}/models/{indicator}.pkl", "rb"))
            forecasted_values[indicator].append("1")
            forecasted_values[indicator] = np.array(forecasted_values[indicator]).reshape(1, -1)
            predicted_val = float(model.predict(forecasted_values[indicator]))
            predicted_values[indicator] = predicted_val
        return predicted_values

    def generate_plot(self, forecasted: dict, predicted: dict):
        forecasted_copy = forecasted.copy()
        for key, val in forecasted_copy.items():
            forecasted_copy[key] = val[:-1]
        forecasted_vals = list(forecasted_copy.values())
        predicted_vals = list(predicted.values())
        fig = go.Figure(data=[go.Table(
            header=dict(values=["Forecasted", "Predicted"],
                        line_color='darkslategray',
                        fill_color='lightskyblue',
                        align='left'),
            cells=dict(values=[forecasted_vals,  # 1st column
                               predicted_vals],  # 2nd column
                       line_color='darkslategray',
                       fill_color='lightcyan',
                       align='left'))
        ])
        fig.show()
