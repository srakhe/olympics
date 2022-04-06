from dash import Dash, dcc, html, Input, Output, callback
from pages import sentiment_analysis

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

layout_index = html.Div([
    dcc.Markdown("# Olympics project"),
    dcc.Markdown("## Please select the type of analysis to view the data for:"),
    dcc.Markdown("- [Sentiment Analysis](/sentiment-analysis)"),
    html.Br()
])


@callback(Output('page-content', 'children'),
          Input('url', 'pathname'))
def display_page(pathname):
    if pathname == "/":
        return layout_index
    if pathname == '/sentiment-analysis':
        return sentiment_analysis.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
