# pip install dash dash-renderer dash-html-components dash-core-components plotly

import dash 
import dash_core_components as dcc 
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div('dash lucas')

if __name__ == '__main__':
    app.run_server(debug=True)
