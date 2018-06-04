import sqlite3
import pandas as pd 
import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import time, json, urllib2
import plotly.graph_objs as go
from collections import deque

btc = urllib2.urlopen('https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC&tsyms=USD')
btcjson = json.load(btc)
btclstprice = btcjson['RAW']['BTC']['USD']['PRICE']
OPENDAY = btcjson['RAW']['BTC']['USD']['OPENDAY']
HIGHDAY = btcjson['RAW']['BTC']['USD']['HIGHDAY']
LASTUPDATE = btcjson['RAW']['BTC']['USD']['LASTUPDATE']
print(HIGHDAY)




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
        

        x = int(60)
        y = int(60)

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
