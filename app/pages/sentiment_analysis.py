from dash import dcc, html, Input, Output, State, callback
import pandas as pd
from scripts.sentiment_analysis.twitter_sentiment import TwitterSentiment
import plotly.express as px


def get_country_options():
    countries_df = pd.read_csv("../data/countries.csv")
    options = countries_df["country_name"].to_list()
    return options


def get_olympic_options():
    games_df = pd.read_csv("../data/games.csv")
    games_df = games_df[games_df["year"] >= 2004]
    games_df = games_df[games_df["year"] <= 2022]
    summer_games_df = games_df[games_df["Type"] == "Summer"]
    winter_games_df = games_df[games_df["Type"] == "Winter"]
    summer_games_df["options"] = summer_games_df["year"].astype(str) + " in " + summer_games_df["city"].astype(
        str) + ", " + summer_games_df["country_code"].astype(str)
    winter_games_df["options"] = winter_games_df["year"].astype(str) + " in " + winter_games_df["city"].astype(
        str) + ", " + winter_games_df["country_code"].astype(str)
    summer_options = summer_games_df["options"].to_list()
    winter_options = winter_games_df["options"].to_list()
    return summer_options, winter_options


summer_options, winter_options = get_olympic_options()
country_options = get_country_options()

layout = html.Div([
    dcc.Markdown("# Olympics Sentiment Analysis"),
    dcc.Dropdown(["Summer", "Winter"], "Summer", id="type-olympics"),
    dcc.Dropdown(summer_options, summer_options[0], id="games-options", searchable=True),
    dcc.Dropdown(country_options, country_options[0], id="country-options", searchable=True),
    dcc.Graph(id="sentiment-graph"),
    html.Div(id="display")
])


@callback(Output("games-options", "options"), Input("type-olympics", "value"))
def update_dropdown(value):
    print(f"value!! = {value}")
    if value == "Summer":
        return summer_options
    else:
        return winter_options


@callback(Output('sentiment-graph', 'plot'),
          Input('type-olympics', 'type_value'),
          Input('games-options', 'game_value'),
          Input('country-options', 'country_value'))
def plot(type_value, game_value, country_value):
    print(f"1. {type_value}\n2. {game_value}\n3. {country_value}")
    tw_sent = TwitterSentiment(num_tweets=50, country=country_value, start="2021-07-15",
                               end="2021-07-16")
    opinion_df = tw_sent.run()
    fig = px.pie(opinion_df, values='No Of People', names='People View', title='Sentiment Analysis')
    return fig
