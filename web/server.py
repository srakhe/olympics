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
        last_run = snt_util.get_last_run()
        if last_run:
            params["last_run"] = last_run
            params["view_state"] = ""
        else:
            params["last_run"] = None
            params["view_state"] = "disabled"
        return render_template("sentiments.html", params=params)
    else:
        if "run_analysis" in request.form:
            game_for = request.form["game_value"]
            snt_util.run_analysis(game_for=game_for)
            return redirect(url_for("sentiment_analysis"))
        elif "refresh" in request.form:
            return redirect(url_for("sentiment_analysis"))
        else:
            snt_util.get_analysis()


@app.route("/predict_host/", methods=["GET", "POST"])
def predict_host():
    if request.method == "GET":
        params = {"years": prdt_util.get_years(), "countries": prdt_util.get_countries()}
        return render_template("predict_host.html", params=params)
    else:
        return render_template("predict_host_result.html")


if __name__ == "__main__":
    app.run(debug=True)
