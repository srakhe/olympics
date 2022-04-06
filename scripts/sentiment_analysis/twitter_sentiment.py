import pandas as pd
from transformers import pipeline
from twitter_scraper import TwitterScraper


class TwitterSentiment:

    def __init__(self, data_path, start, end):
        self.data_path = data_path
        tw_scraper = TwitterScraper(data_path=self.data_path)
        tw_scraper.scrape(start=start, end=end)
        self.twitter_df = pd.read_csv(self.data_path + "/tweets_data.csv")

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
        return self.get_strong_opinion_count(), self.get_other_opinion_count()


if __name__ == "__main__":
    tw_sent = TwitterSentiment(data_path="data", start="2021-07-15", end="2021-07-16")
    opinion_df, neutral_df = tw_sent.run()
