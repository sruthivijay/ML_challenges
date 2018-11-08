############Onload SBV and Volume########################
import os
import json

from datetime import datetime , timedelta
from pytz import timezone

import threading
from flask import Flask, render_template, request, json
from azure.storage.blob import BlockBlobService
import pickle
from six.moves import cPickle
import pandas as pd
from io import BytesIO
from lxml import objectify
import json
from flask_cors import CORS, cross_origin
from ast import literal_eval
from flask_caching import Cache
import numpy as np
from azure.storage.table import TableService, Entity
import math
from flask_caching import Cache
#import jsonpickle
import pyodbc
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import dash
import os
import dash_core_components as dcc
import dash_html_components as html
import base64
day=['Monday','Tuesday','Thursday','Friday','Sunday','Wednesday','Saturday']
dayStr = ', '.join('\'{0}\''.format(w) for w in day)
start_date='12/11/2016'
end_date='12/11/2017'
state='0'
intersection=['0C053AFF5F37603A']
interStr = ', '.join('\'{0}\''.format(w) for w in intersection)
server = 'edmsqlserver.database.windows.net'
database = 'edmdb'
username = 'edmsqladmin@edmsqlserver'
password = 'Logan123&'
driver= '{SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
qry33='SELECT DATEADD(minute, AP.FiveMinutesPeriod * 5, \'2010-01-01T00:00:00\') AS DateTime, AP.AvgVol, AP.AvgSpaceOccupancy,AP.AvgSpeed FROM (SELECT P.FiveMinutesPeriod, AVG(CAST(P.Volume AS FLOAT)) AS AvgVol, AVG(CAST(P.SpaceOccupancy AS FLOAT)) AS AvgSpaceOccupancy,AVG(CAST(P.speed AS FLOAT)) AS AvgSpeed  FROM (SELECT top 1000 s."Space Occupancy" as SpaceOccupancy,s."Arithmetic Mean Speed" as speed, CAST(s.Volume AS FLOAT) as Volume, datediff(minute, \'2010-01-01T00:00:00\', CONVERT(DATETIME, CONVERT(varchar(20), "Date",101)  + \' \' + CONVERT(varchar(8), "Time", 108)))/5 AS FiveMinutesPeriod  from (sbvpostprocess s INNER JOIN intersectiondetails ON s."CPU Identifier" = intersectiondetails."CPU Identifier")where s."CPU Identifier"  in  ('+interStr+') )  AS P GROUP BY P.FiveMinutesPeriod) AS AP'

#print(dayStr)
onload_volume=pd.read_sql(qry33,cnxn)
qry44='SELECT  DATEADD(minute, AP.timeperiod  * 5, \'2010-01-01T00:00:00\') AS DateTime,AP.SBV FROM (SELECT P.timeperiod,COUNT(P.Status) AS SBV FROM (SELECT top 1000 s.Status,s."Detector Title",datediff(minute, \'2010-01-01T00:00:00\', CONVERT(DATETIME, CONVERT(varchar(20), "Date",101)  + \' \' + CONVERT(varchar(8), "Time", 108)))/5 AS timeperiod  FROM (sbvpostprocess s INNER JOIN intersectiondetails ON s."CPU Identifier" = intersectiondetails."CPU Identifier") where s."CPU Identifier"  in  ('+interStr+') AND s.Status=\'100\' AND s."Detector Title" LIKE \'RLR%\' ) AS P GROUP BY P.timeperiod) AS AP'
onload_sbv=pd.read_sql(qry44,cnxn)

onload_volume=onload_volume.merge(onload_sbv,how='left',left_on='DateTime',right_on='DateTime')
onload_volume=onload_volume.fillna(0)
onload_volume.DateTime=onload_volume.DateTime.astype(str)
onload_volume.DateTime=onload_volume['DateTime'].str.partition(' ')[2]
onload_volume['DateTime'] = pd.to_datetime(onload_volume['DateTime'])
#onload_volume=onload_volume.set_index('DateTime', inplace=True)
#onload_volume.DateTime=onload_volume.DateTime.astype(str)
#onload_volume.DateTime=onload_volume['DateTime'].str.partition(' ')[2]
#onload_volume.DateTime=onload_volume['DateTime'].str.replace('-',',')
#onload_volume.DateTime=onload_volume['DateTime'].str.replace(':',',')
#onload_volume.DateTime=onload_volume['DateTime'].str.replace(' ',',')

print(onload_volume)
###########Onload weather#########
def extract_data():
    server = 'edmsqlserver.database.windows.net'
    database = 'edmdb'
    username = 'edmsqladmin@edmsqlserver'
    password = 'Logan123&'
    driver= '{SQL Server}'
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    #cursor = cnxn.cursor()
    #cursor.execute("select top 10000 * from traveltimedatastream")
    qry='select top 1000 * from weather_data'
    df=pd.read_sql(qry,cnxn)
    cnxn.close()
    return df

weather_data  = extract_data()
weather_data['DateTime']=onload_volume['DateTime'].copy()
weather_data.DateTime=weather_data.DateTime.astype(str)
weather_data.DateTime=weather_data['DateTime'].str.partition(' ')[2]
weather_data['DateTime'] = pd.to_datetime(weather_data['DateTime'])


weather_info=weather_data[['DateTime','temp','weather_icon','weather_description']].copy()
print(weather_info.info())

###########Resampling weather############
weather_info.set_index('DateTime', inplace=True)
resampledValue = weather_info['temp'].resample('15min').mean()
   
resampledValue = resampledValue.fillna(0)
      
df2 = resampledValue.to_frame().reset_index()
print(df2)

##################Conditional column creation######################

conditions = [
    (df2['temp'] <= 5),
    (df2['temp'] <= 15),
    ((df2['temp'] > 15) & (df2['temp'] <=25)),
    ((df2['temp'] > 25) & (df2['temp'] <=35)),
    (df2['temp'] >45)]
choices = ['snow','fog', 'drizzle', 'broken clouds','clear sky']
df2['description'] = np.select(conditions, choices, default='black')
conditions1 = [
    (df2['description'] =='snow'),
    (df2['description'] =='fog'),
    (df2['description']=='drizzle'),
    (df2['description']=='broken clouds'),
    (df2['description'] =='clear sky')]
choices1 = [ 'http://openweathermap.org/img/w/13n.png', 'http://openweathermap.org/img/w/50n.png ', 'http://openweathermap.org/img/w/09n.png' , 'http://openweathermap.org/img/w/04n.png','http://openweathermap.org/img/w/01d.png']
df2['image_url'] = np.select(conditions1, choices1, default='black')
print(df2)

####################merging sbv df and weather df##############
onload_data=onload_volume.merge(df2,how='inner',left_on='DateTime',right_on='DateTime')
onload_data['DateTime'] = pd.to_datetime(onload_data['DateTime'],format= '%H:%M:%S' ).dt.time
onload_data=onload_data.set_index('DateTime')
onload_data=onload_data.fillna(0)
print(onload_data)
#a=onload_data.DateTime
#b=onload_data.image_url
#xfilt=a[data.parameter==88101]
#yfilt=b[data.parameter==88101]
app=dash.Dash()
colorscale = [ [0.25, 'rgb(17, 123, 215)'],
                [0.5, 'rgb(37, 180, 167)'], [0.75, 'rgb(249, 210, 41)'], [1.0, 'rgb(54, 50, 153)']]


app.layout=html.Div(children=[
         
     dcc.Graph(
        id='example-graph1',
        figure={
            'data': [ 
               go.Bar(
                    x=onload_data.index,
                    y =onload_data['SBV'],
					 marker = dict(
          color = 'red'
        ),
					
					name='SBV'
					
					
                    
                    ),
               go.Scatter(
                    x=onload_data.index,
                    y =onload_data['AvgVol'],
                    name='Volume',
					
                    yaxis='y2',
					line = dict(
        color = ('rgb(22, 96, 167)'),
        width = 4,)
                    ),
               go.Scatter(
                    x=onload_data.index,
                    y =onload_data['AvgSpeed'],
                    name='Arithmetic Mean Speed',
					line = dict(
        color = ('rgb(100, 00, 150)'),
        width = 4)
					
                   ),
               go.Scatter(
                    x=onload_data.index,
                    y =onload_data['AvgSpaceOccupancy'],
					
                    name='SpaceOccupancy',
					line = dict(
        color = ('rgb(50,100, 00)'),
        width = 4,)
					
                    ),
               go.Scatter(
                    x=onload_data.index,
                    y =onload_data['temp'],
                    name='temperature',
					mode = 'markers',
                    marker = dict(
                            color=onload_data['temp'],
                            colorscale=colorscale,
                            showscale=True,
							
                            cmax=60,
                            cmin=0,
                            size=10,
                            opacity=0.7,
							symbol= 'triangle' ))
            ],
			'layout':go.Layout(
    title='Stop Bar Violation',
	legend= {
"orientation": "h",
"xanchor": "center",
"y": 1.2,
"x": 0.5
},
	
    yaxis=dict(
        title='SBV,Arithmetic Mean Speed,Space Occupancy',
		titlefont=dict(
            color='rgb(0, 0, 0)'
        ),showline=True,
        tickfont=dict(
            color='rgb(0, 0, 0)'
        )
    ),
    yaxis2=dict(
        title='Volume',
        titlefont=dict(
            color='rgb(0, 0, 0)'
        ),showline=True,
        tickfont=dict(
            color='rgb(0, 0, 0)'
        ),
        overlaying='y',
        side='right'
    ),xaxis=dict(
        title='15m aggregated time',
		 titlefont=dict(
            color='rgb(0, 0, 0)'
        ),showline=True,
        tickfont=dict(
            color='rgb(0, 0, 0)'
        )
    )
	
)
	
	  
		})
#        ,style={'width': '35%', 'display': 'inline-block', 'padding': '0 20','float':'left'}
    
 #,style={'width': '30%', 'display': 'inline-block', 'padding': '0 20','float':'left'}),

    ])
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
	
   
if __name__ == '__main__':
    app.run_server(debug=True)