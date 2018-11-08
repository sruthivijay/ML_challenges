import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

app = dash.Dash()

df = pd.read_csv('C:/Users/sruthi.vs/Downloads/actual_data.csv')

available_indicators = df['Pairing'].unique()



colors = {
    'background': '#111111',
    'text': '#FFA500'
}

app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1(
        children='Speed Vs Distance Analysis',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(
        children='Distance analysis over speed',
        style = {
            'textAlign': 'center',
            'color': colors['text']
        }),
    html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Union @ Ulster to Union/Temple @ DTC Blvd'
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

    dcc.Graph(
        id='Time_plot_graph')

])

@app.callback(
    dash.dependencies.Output('Time_plot_graph', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value')
    ])

def update_graph(xaxis_column_name):
    return{

            'data': [go.Bar(
                        x=df[df['Pairing'] == xaxis_column_name]['hour'],
                        y=df[df['Pairing'] == xaxis_column_name]['No'],
                        name='No_volume'
)],
            'layout': {
                 'title': 'Dash Data Visualization',
                 'xaxis': {'title': xaxis_column_name},
                 'yaxis': {'title': xaxis_column_name},
                 'plot_bgcolor': colors['background'],
                 'paper_bgcolor': colors['background'],
                 'font': {
                    'color': colors['text']
                  },
                  'barmode':'stack',
                  'hovermode': 'closest'


            }
        }

if __name__ == '__main__':
    app.run_server(debug=True)