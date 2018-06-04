import sqlite3
import pandas as pd 
import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque



app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1*1000
        ),
    ]
)

@app.callback(
    Output(
        'live-graph', 
        'figure'
        ),
    events = [
        Event(
            'graph-update', 
            'interval'
        )
    ]
)
def update_graph_scatter():
    try:
        conn = sqlite3.connect('twitter.db')
        c = conn.cursor()

        df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE '%trump%' ORDER BY unix DESC LIMIT 5000", conn)

        df.sort_values('unix', inplace=True)

        df['smoothed_sentiment'] = df['sentiment'].rolling(int(len(df)/5)).mean()

        df.dropna(inplace=True)

        x = df.unix.values[-100:]
        y = df.smoothed_sentiment.values[-100:]

        data = plotly.graph_objs.Scatter(
            x=x,
            y=y,
            name='Scatter',
            mode= 'lines+markers'
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
                    )
                ,
            )
        }
    except Exception as e:
        with open('error.txt', 'a') as f:
            f.write(str(e))
            f.write('\n')

if __name__ == '__main__':
    app.run_server(debug=True)
