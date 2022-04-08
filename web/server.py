from flask import Flask, render_template, request, url_for, redirect
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
        params["last_run"] = None
        params["view_state"] = ""
        return render_template("sentiments.html", params=params)
    else:
        if "run_analysis" in request.form:
            snt_util.run_analysis()
            return redirect(url_for("sentiment_analysis"))
        elif "refresh" in request.form:
            return redirect(url_for("sentiment_analysis"))
        else:
            snt_util.get_analysis()


if __name__ == "__main__":
    app.run(debug=True)
