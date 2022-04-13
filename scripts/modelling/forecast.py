from prophet import Prophet
import wbgapi as wb
import pandas as pd

economic_variables = {'NY.GDP.PCAP.CD': 'GDP Per Capita'}


def get_indicator_data(indicator):
    eco_df = wb.data.DataFrame(indicator, skipAggs=True)
    eco_df = eco_df.rename(columns=lambda x: int(x.replace('YR', '')))
    eco_df = eco_df.transpose().fillna(method='backfill').fillna(method='ffill')
    eco_df.dropna(inplace=True, axis=1)
    return eco_df


def get_forecast_data(country_series, colname):
    df = country_series.reset_index().rename(columns={'index': 'ds', colname: 'y'})
    future_years = [i for i in range(2020, 2051)]
    df['ds'] = pd.to_datetime(df['ds'], format='%Y')

    my_model = Prophet(interval_width=0.95)
    my_model.fit(df)
    future_dates = my_model.make_future_dataframe(periods=31, freq='Y')
    forecast_df = my_model.predict(future_dates)

    forecast_df['ds'] = pd.DatetimeIndex(forecast_df['ds']).year
    selected_df = forecast_df.drop_duplicates(subset=['ds'], keep='first')
    selected_df = selected_df.set_index('ds').rename(columns={'yhat': colname})
    selected_df = selected_df.loc[future_years]

    return selected_df[colname]


def run():
    global economic_variables
    path = "/model_input_data/"

    for key, value in economic_variables.items():
        df = get_indicator_data(key)
        forecast_df = pd.DataFrame()

        for val in df.columns:
            forecast_series = get_forecast_data(df[val], val)
            forecast_df = forecast_df.append(forecast_series, ignore_index=False)

        forecast_df.to_csv('/content/drive/MyDrive/bd2/' + value + ".csv")


if __name__ == '__main__':
    run()
