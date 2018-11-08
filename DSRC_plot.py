import csv
import dash
import os
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()
#BSM_DATA = pd.read_csv("C:/Users/sruthi.vs/Downloads/Wyoming_CV_Pilot_Basic_Safety_Message_One_Day_Sample.csv",
#                       nrows=10000)
#
#
BSM_DATA1 = pd.read_csv("C:/Users/sruthi.vs/Downloads/Wyoming_CV_Pilot_Basic_Safety_Message_One_Day_Sample.csv",
                       nrows=100000, low_memory=False)

#BSM_DATA1 = pd.read_csv("D:/DSRC/BSM_DATA.csv")

#range_data_heading = [0,2,4,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40]
#
#ranges_speed = [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380]
#
#data = BSM_DATA1.groupby(pd.cut(BSM_DATA1.coreData_heading, range_data_heading)).count()
#
#data1 = BSM_DATA1.groupby(pd.cut(BSM_DATA1.coreData_speed, ranges_speed)).count()
#
#data.to_csv("D:/DSRC/heading.csv")
#
#data1.to_csv("D:/DSRC/speed.csv")

data = pd.read_csv("D:/DSRC/heading.csv")

data1 = pd.read_csv("D:/DSRC/speed.csv")

data.columns

def generate_table(dataframe, max_rows=30):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

#data1 = BSM_DATA1.groupby(pd.cut(BSM_DATA1.coreData_speed, ranges_speed)).count()
#
#count_by_data_heading = BSM_DATA1.groupby('coreData_heading', as_index=False)['coreData_id'].count()
#
#count_by_data_speed = BSM_DATA1.groupby('coreData_speed', as_index=False)['coreData_id'].count()
#
#data1
#BSM_DATA1.dtypes
#
#final_data = pd.merge(BSM_DATA1,count_by_data_heading,how = 'inner',on = 'coreData_heading')
#BSM_DATA1 = pd.merge(final_data,count_by_data_speed,how = 'inner',on = 'coreData_speed')

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
    html.Div(children=[
    html.H4(children='Basic Safety Message'),
    generate_table(BSM_DATA1)
    ]),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
               go.Scatter(
                    x=data['coreData_heading'],
                    y =data['coreData_id'],
                    name = 'Data Heading',
                    marker = dict( color = 'Light blue'),
                    fill='tozeroy')
            ],
            'layout': {
                 'title': 'Core Heading Visualization',
#                 'xaxis': {'title': 'Distance_travelled'},
#                 'yaxis': {'title': 'Speed'},
                 'plot_bgcolor': colors['background'],
                 'paper_bgcolor': colors['background'],
                 'font': {
                    'color': colors['text']
                  },


            }
        }
    ),
    dcc.Graph(
        id='example-graph1',
        figure={
            'data': [
               go.Scatter(
                    x=data1['coreData_speed'],
                    y =data1['coreData_id'],
                    name = 'Vehicle Speed',
                    marker = dict( color = 'Green'),
                    fill='tonexty')
            ],
            'layout': {
                 'title': 'Core Speed Visualization',
#                 'xaxis': {'title': 'Distance_travelled'},
#                 'yaxis': {'title': 'Speed'},
                 'plot_bgcolor': colors['background'],
                 'paper_bgcolor': colors['background'],
                 'font': {
                    'color': colors['text']
                  }


            }
        }
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)
    
