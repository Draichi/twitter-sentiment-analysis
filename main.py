# pip install dash dash-renderer dash-html-components dash-core-components plotly
# 
# to config pylint: 
# pylint --generate-rcfile > .pylintrc
# find for "disable="
#
#
from dash.dependencies import Input, Output
import dash 
import dash_core_components as dcc 
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div(
    children = [
        dcc.Input(
            id = 'input',
            value = 'escre lucas',
            type = 'text'
        ),
        html.Div(id = 'output')
    ])

@app.callback(
    Output(
        component_id = 'output',
        component_property = 'children'
    ),
    [
        Input(
            component_id = 'input',
            component_property = 'value'
        )
    ]
)
def lucas(luc):
    return "input: {}".format(luc)

if __name__ == '__main__':
    app.run_server(debug=True)
