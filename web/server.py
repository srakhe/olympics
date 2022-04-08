from flask import Flask, render_template, request
from utils.sentiment_analysis import SentimentAnalysis

app = Flask(__name__)
snt_util = SentimentAnalysis(data_path="../data")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sentiment_analysis", methods=["GET", "POST"])
def sentiment_analysis():
    if request.method == "GET":
        params = {}
        games_options = snt_util.get_olympic_options()
        params["games"] = games_options
        return render_template("sentiments.html", params=params)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
