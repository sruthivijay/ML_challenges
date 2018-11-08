# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 14:44:06 2018

@author: sruthi.vs
"""

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dat
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
from datetime import date
import calendar
import flask
from datetime import datetime as dt
import numpy as np

mapbox_access_token = 'pk.eyJ1Ijoic3J1dGhpMzAiLCJhIjoiY2psYnlwOHd2M2YwNzNvcXlndWtrcnE1cCJ9.O6SrlZ89NeY_I2GlUouH7w'
app = dash.Dash()

BSM_DATA = pd.read_csv("D:/DSRC/Processed_data_SMALL.csv",nrows=100000, low_memory=False)

BSM_DATA['coreData_position_lat_str']=BSM_DATA['coreData_position_lat'].astype(str)

BSM_DATA['coreData_position_lon_str']=BSM_DATA['coreData_position_long'].astype(str)

BSM_DATA['position'] = BSM_DATA[['coreData_position_lat_str', 'coreData_position_lon_str']].apply(lambda x: ','.join(x), axis=1)

colorscale = [[0, 'rgb(54, 50, 153)'], [0.35, 'rgb(17, 123, 215)'],
                [0.5, 'rgb(37, 180, 167)'], [0.6, 'rgb(134, 191, 118)'],
                [0.7, 'rgb(249, 210, 41)'], [1.0, 'rgb(244, 236, 21)']]


site_lat = BSM_DATA['coreData_position_lat']
site_lon = BSM_DATA['coreData_position_long']

colors = {
    'background': '#FFFFFF',
    'text': '#FFA500'
}


app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1(
        children='BSM Data Visualization',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(
        children='Data Spread',
        style = {
            'textAlign': 'center',
            'color': colors['text']
        }),
#    html.Div(children=[
#    html.H4(children='Basic Safety Message'),
#    generate_table(BSM_DATA1)
#    ]),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
               go.Scatter(
                    x=BSM_DATA['position'],
                    y =BSM_DATA['violation_count'],
                    name = 'Violation count',
                    mode = 'lines+markers',
                    line = dict(shape = 'spline'),
                    marker = dict( color = 'Light blue'),
                    fill='tozeroy')
            ],
            'layout': {
                 'title': 'Vehicle violation count',
#                 'xaxis': {'title': 'Distance_travelled'},
#                 'yaxis': {'title': 'Speed'},
                 'plot_bgcolor': colors['background'],
                 'paper_bgcolor': colors['background'],
                 'font': {
                    'color': colors['text']
                  },
                 'height': 225,
                 'margin': {'l': 10, 'b': 30, 'r': 20, 't': 30},
            }
        }
#,style={'width': '30%', 'display': 'inline-block', 'padding': '0 20','float':'left'}
    ),
  dcc.Graph(
        id='example-graph1',
        figure={
            'data': [
               go.Scatter(
                    x=BSM_DATA['position'],
                    y =BSM_DATA['Mean_speed'],
                    name = 'Vehicle Speed',
                    marker = dict( color = 'Green'),
                    fill='tonexty')
            ],
            'layout': {
                 'title': 'Average Speed across locations',
#                 'xaxis': {'title': 'Distance_travelled'},
#                 'yaxis': {'title': 'Speed'},
                 'plot_bgcolor': colors['background'],
                 'paper_bgcolor': colors['background'],
                 'font': {
                    'color': colors['text']
                  },
                 'height': 225,
                 'margin': {'l': 10, 'b': 30, 'r': 10, 't': 30},

            }
        }
#        ,style={'width': '35%', 'display': 'inline-block', 'padding': '0 20','float':'left'}
    ),
 #,style={'width': '30%', 'display': 'inline-block', 'padding': '0 20','float':'left'}),

    dcc.Graph(
            id ='Graph-mapbox',
            figure={
                'data':[
                    go.Scattermapbox(
                            lat =site_lat,
                            lon =site_lon,
                            mode='markers+text',
                            text = BSM_DATA['violation_count'],
                            hoverinfo='text',
                            marker = dict(
                            color=BSM_DATA['violation_count'],
                            colorscale=colorscale,
                            showscale=True,
                            cmax=400,
                            cmin=0,
                            size=10,
                            opacity=0.7)
                
        )],

                'layout' : {
                        'title':'Vehicle violation count',
                        'autosize':True,
                        'hovermode':'closest',
                        'showlegend':False,
                        'mapbox':dict(
                                accesstoken=mapbox_access_token,
                                bearing=0,
                                center=dict(
                                        lat=38,
                                        lon=-94
                                        ),
                                        pitch=0,
                                        zoom=3,
                                        style='light'
                                        ),
                          'margin':{'l': 0, 'b': 30, 't': 30, 'r': 40},
                          'height':575,

                                        }
        
        }
#,style={'width': '80%', 'display': 'inline-block', 'padding': '0 20','float':'right'}
        ),
  

#         html.Div([
#    html.H4('BSM Data'),
#    dat.DataTable(
#        # Initialise the rows
#        rows=BSM_DATA.to_dict('records'),
#        row_selectable=True,
#        filterable=True,
#        sortable=True,
#        selected_row_indices=[],
#        id='table'
#                ),
#            ]),

])


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)

