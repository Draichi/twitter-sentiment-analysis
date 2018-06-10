import sqlite3, dash, plotly, random, datetime
import pandas as pd 
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Output, Event, Input
from collections import deque

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.H2('Live Twitter Sentiment'),
        dcc.Input(
            id = 'sentiment_term', 
            value = 'o', 
            type = 'text'
        ),
        dcc.Graph(
            id = 'live-graph', 
            animate = False
        ),
        dcc.Interval(
            id = 'graph-update',
            interval = 1*1000
        ),
    ]
)

@app.callback(
    Output(
        'live-graph', 
        'figure'
    ),
    [Input(
        component_id = 'sentiment_term', 
        component_property = 'value'
    )],
    events = [
        Event(
            'graph-update', 
            'interval'
        )
    ]
)
def update_graph_scatter(sentiment_term):
    try:
        conn = sqlite3.connect('twitter.db')
        c = conn.cursor()

        df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 200", conn ,params=('%' + sentiment_term + '%',))

        df.sort_values('unix', inplace=True)

        df['smoothed_sentiment'] = df['sentiment'].rolling(int(len(df)/5)).mean()

        df['date'] = pd.to_datetime(
            df['unix'],
            unit='ms'
        )
        df.set_index('date', inplace=True)
        df = df.resample('1s').mean()
        df.dropna(inplace=True)

        x = df.index
        y = df.smoothed_sentiment

        data = plotly.graph_objs.Scatter(
            x = x,
            y = y,
            name = 'Scatter',
            mode = 'lines+markers'
        )
        return {
            'data': [data],
            'layout': go.Layout(
                xaxis = dict(
                    range = [
                        min(x),
                        max(x)
                    ]
                ),
                yaxis = dict(
                    range = [
                        min(y),
                        max(y)
                    ]
                ),
                title = 'Searching for {}'.format(sentiment_term)
            )
        }
    except Exception as e:
        with open('errors.txt', 'a') as f:
            f.write(str(datetime.datetime.now()))          
            f.write(' ')          
            f.write(str(e))
            f.write('\n')

if __name__ == '__main__':
    app.run_server(debug=True)
