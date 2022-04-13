import pandas as pd
from nrclex import NRCLex
import nltk
# import plotly.express as px
import plotly.graph_objects as go


class TwitterSentiment:

    def __init__(self, data_path, start, end):
        self.data_path = data_path
        self.twitter_df = pd.read_csv(r"C:\Users\tanvi\Downloads\Semester-2\Big-data\final project\tweets_data.csv")

    def perform_analysis(self):
        self.results = NRCLex(','.join(self.twitter_df['Text']))

    def get_raw_emotion_score(self):
        self.raw_emotion_score = self.results.raw_emotion_scores

    def plot_graph(self, data):
        emotion_df = pd.DataFrame.from_dict(
            data, orient='index').reset_index().rename(
            columns={'index': 'Emotion Classification', 0: 'Emotion Count'}).sort_values(
            by=['Emotion Count'], ascending=False)

        emotion_df = emotion_df[emotion_df['Emotion Classification'] != 'positive']
        emotion_df = emotion_df[emotion_df['Emotion Classification'] != 'negative']

        fig = go.Figure(go.Pie(values=emotion_df['Emotion Count'],
                               labels=emotion_df['Emotion Classification']))  # , title='Tweets Sentiments Composition')
        # fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig

    def run(self):
        self.perform_analysis()
        self.get_raw_emotion_score()
        return self.plot_graph(self.raw_emotion_score)


if __name__ == "__main__":
    tw_sent = TwitterSentiment(data_path="data", start="2021-07-15", end="2021-07-16")
    plot_1 = tw_sent.run()
    # plot_1.show()
