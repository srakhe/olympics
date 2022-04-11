import pandas as pd
from datetime import datetime
import pickle
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler


class PredictHost:

    def __init__(self, data_path, web_data_path):
        self.data_path = data_path
        self.web_data_path = web_data_path
        self.eco_indicators = ["Debt", "Employment", "Foreign Investments", "GDP Growth",
                               "Gross National Expenditure", "Import Goods", "Inflation", "Revenue",
                               "Stocks", "Tax Revenue", "Trade", "Unemployment", "GDP Per Capita"]

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
        forecasted_values_transformed = {}
        for indicator in self.eco_indicators:
            country_eco_df = pd.read_csv(f"{time_series_data}/{indicator}.csv")
            country_eco_df_copy = country_eco_df.copy()
            country_eco_df = country_eco_df.iloc[:, 1:]
            country_eco_df = country_eco_df.reset_index(drop=True)
            country_eco_df = country_eco_df.set_index(["Unnamed: 0"])
            # log_data = pd.DataFrame(np.log(country_eco_df), columns=country_eco_df.columns)
            country_eco_df[country_eco_df.columns] = np.cbrt(country_eco_df[country_eco_df.columns])
            country_eco_df = country_eco_df.transpose()
            scaler = StandardScaler()
            scaler.fit(country_eco_df)
            country_eco_df.loc[:] = scaler.transform(country_eco_df)
            country_eco_df = country_eco_df.transpose()
            # country_eco_df.loc[:] = scaler.transform(country_eco_df)
            # country_eco_df = country_eco_df[country_eco_df["Unnamed: 0"] == str(country)]
            country_eco_df_copy = country_eco_df_copy[country_eco_df_copy["Unnamed: 0"] == str(country)]
            country_eco_df = country_eco_df.sort_index()
            pos = country_eco_df.index.searchsorted(str(country))
            country_eco_df = country_eco_df.iloc[[pos]]
            # country_eco_df = country_eco_df[country_eco_df["Unnamed: 0"] == str(country)]
            forecasted_values[indicator] = []
            forecasted_values_transformed[indicator] = []
            for each_year in years:
                each_year = str(each_year)
                indicator_value = country_eco_df_copy[each_year].to_list()
                indicator_value_transformed = country_eco_df[each_year].to_list()
                if indicator_value:
                    forecasted_values[indicator].append(float(indicator_value[0]))
                else:
                    forecasted_values[indicator].append(float(0))
                if indicator_value_transformed:
                    forecasted_values_transformed[indicator].append(float(indicator_value_transformed[0]))
                else:
                    forecasted_values_transformed[indicator].append(float(0))
        return forecasted_values, forecasted_values_transformed

    def get_predictions(self, forecasted_values_transformed):
        predicted_values = {}
        for indicator in self.eco_indicators:
            model = pickle.load(open(f"{self.data_path}/models/{indicator}.pkl", "rb"))
            forecasted_values_transformed[indicator].append("1")
            forecasted_values_transformed[indicator] = np.array(forecasted_values_transformed[indicator]).reshape(1, -1)
            predicted_val = float(model.predict(forecasted_values_transformed[indicator]))
            predicted_values[indicator] = predicted_val ** 3
        return predicted_values

    def generate_plot(self, forecasted: dict, predicted: dict):
        df = pd.DataFrame([], columns=["indicators", "forecasted", "predicted"])
        i = 0
        for indicator in self.eco_indicators:
            forecasted_val = forecasted[indicator][-1]
            predicted_val = abs(predicted[indicator])
            df.loc[i] = [indicator, forecasted_val, predicted_val]
            i += 1
        fig = go.Figure(data=[go.Table(
            header=dict(values=["Indicators", "Forecasted Values", "Predicted Values (upon hosting)"],
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[df.indicators, df.forecasted, df.predicted],
                       fill_color='lavender',
                       align='left'))
        ])
        fig.show()
