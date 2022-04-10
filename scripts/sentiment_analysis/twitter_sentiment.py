import pandas as pd
from transformers import pipeline
from scripts.sentiment_analysis.twitter_scraper import TwitterScraper
import plotly.graph_objects as go


class TwitterSentiment:

    def __init__(self, num_tweets, country, start, end):
        tw_scraper = TwitterScraper()
        self.twitter_df = tw_scraper.scrape(num_tweets=num_tweets, country=country, start=start, end=end)
        self.strong_opinion_df = None
        self.other_opinion_df = None
        self.results = None

    def tune_results(self):
        results_df = pd.DataFrame(self.results, columns=['label', 'score'])
        self.strong_opinion_df = results_df[results_df['score'] >= 0.7]
        self.other_opinion_df = results_df[results_df['score'] < 0.7]

    def perform_analysis(self):
        sentiment_classifier = pipeline('sentiment-analysis')  # huggging face transformer used to perform NLP
        self.results = sentiment_classifier(self.twitter_df['Text'].tolist())
        self.tune_results()

    def get_strong_opinion_count(self):
        return self.strong_opinion_df.groupby('label').count().reset_index().rename(
            columns={'label': 'People View', 'score': 'No Of People'})

    def get_other_opinion_count(self):
        return self.other_opinion_df.groupby('label').count().reset_index().rename(
            columns={'label': 'People View', 'score': 'No Of People'})

    def run(self):
        self.perform_analysis()
        opinion_df, neutral_df = self.get_strong_opinion_count(), self.get_other_opinion_count()
        new_row = {'People View': 'NEUTRAL', 'No Of People': neutral_df['No Of People'].sum()}
        opinion_df = opinion_df.append(new_row, ignore_index=True)
        fig = go.Pie(labels=opinion_df['People View'], values=opinion_df['No Of People'])
        return fig
