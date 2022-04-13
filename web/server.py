from flask import Flask, render_template, request, url_for, redirect
from utils.sentiment_analysis import SentimentAnalysis
from utils.predict_host import PredictHost

app = Flask(__name__)
snt_util = SentimentAnalysis(data_path="../data", web_data_path="data/sentiment_analysis")
prdt_util = PredictHost(data_path="../data", web_data_path="data/predict_host")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sentiment_analysis/", methods=["GET", "POST"])
def sentiment_analysis():
    if request.method == "GET":
        params = {}
        games_options = snt_util.get_olympic_options()
        params["games"] = games_options
        return render_template("sentiments.html", params=params)
    else:
        game_for = request.form["game_value"]
        snt_util.run_analysis(game_for=game_for)
        return redirect(url_for("sentiment_analysis"))


@app.route("/predict_host/", methods=["GET", "POST"])
def predict_host():
    if request.method == "GET":
        params = {"years": prdt_util.get_years(), "countries": prdt_util.get_countries()}
        return render_template("predict_host.html", params=params)
    else:
        country = request.form["country_value"]
        year = request.form["year_value"]
        forecasted_values, forecasted_values_transformed = prdt_util.get_forecasts(country=country, year=year)
        forecasted_values_copy = forecasted_values.copy()
        predicted_values = prdt_util.get_predictions(forecasted_values_transformed=forecasted_values_transformed)
        prdt_util.generate_plot(forecasted_values_copy, predicted_values, country, year)
        return redirect(url_for("predict_host"))


if __name__ == "__main__":
    app.run(debug=True)
