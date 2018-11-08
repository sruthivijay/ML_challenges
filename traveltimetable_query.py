# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 09:46:28 2018

@author: sruthi.vs
"""

import os
import json
import pyodbc 
import pandas as pd
#from datetime import datetime
#from datetime import date
import calendar
from datetime import datetime as dt
import numpy as np
#postreqdata = json.loads(open(os.environ['req']).read())
#response = open(os.environ['res'], 'w')
#response.write("hello world from "+postreqdata['name'])
#response.close()
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 10:54:23 2018

@author: sruthi.vs
"""
postreqdata = json.loads(open(os.environ['req']).read())
print(postreqdata['body'])
print(type(postreqdata['body']))
request = json.loads(postreqdata['body'])
print(request['sdate'])

#request1 = json.dumps(postreqdata['body'])

#request = json.loads(request1)
#print(type(json.dumps(request)))
sdate = "2018-07-24"
edate = "2018-07-25"
sdate1 = "2018-07-23"
edate1 = "2018-07-27"
pid = "Havana @ Dartmouth to Havana @ Girard"
pid1 = "Federal @ I-70 N to Federal @ 44th"
radioVal = ''
if len(radioVal) == 0:
        radioVal = ['Sunday Monday Tuesday Wednesday Thursday Friday Saturday']
#radioVal=radioVal.split()
print((radioVal))
dayStr = ', '.join('\'{0}\''.format(w) for w in radioVal)
print(dayStr)

server = 'edmsqlserver.database.windows.net'
database = 'edmdb'
username = 'edmsqladmin@edmsqlserver'
password = 'Logan123&'
driver= '{SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
#cursor = cnxn.cursor()
pair_array = pid.split('to')
pair_array1 = pid1.split('to')
#cursor.execute("select top 10000 * from traveltimedatastream")
qry1 = 'SELECT DATEADD(minute, AP.FiveMinutesPeriod * 15, \'2010-01-01T00:00:00\') AS Period, AP.AvgValue FROM (SELECT P.FiveMinutesPeriod, AVG(CAST(P.TravelTime AS FLOAT)) AS AvgValue FROM (SELECT datediff(minute, \'2010-01-01T00:00:00\', CONVERT(datetime,T.LastMatch, 120))/15 AS FiveMinutesPeriod, T.TravelTime FROM traveltimedatastream T WHERE T.ORIGIN = \''+pair_array[0].strip()+'\' AND T.DESTINATION = \''+pair_array[1].strip()+'\' AND CONVERT(datetime,T.LastMatch, 120) >= \''+sdate+'\' AND CONVERT(datetime,T.LastMatch, 120) <= \''+edate+'\' AND DATENAME(dw, CONVERT(datetime,T.LastMatch, 120)) IN ('+dayStr+')) AS P GROUP BY P.FiveMinutesPeriod) AP'
df1=pd.read_sql(qry1,cnxn)
print(qry1)
print(df1)
df1.columns = ['resampledTime', 'Incident_Avg']
qry2 = 'SELECT DATEADD(minute, AP.FiveMinutesPeriod * 15, \'2010-01-01T00:00:00\') AS Period, AP.AvgValue FROM (SELECT P.FiveMinutesPeriod, AVG(CAST(P.TravelTime AS FLOAT)) AS AvgValue FROM (SELECT datediff(minute, \'2010-01-01T00:00:00\', CONVERT(datetime,T.LastMatch, 120))/15 AS FiveMinutesPeriod, T.TravelTime FROM traveltimedatastream T WHERE T.ORIGIN = \''+pair_array1[0].strip()+'\' AND T.destination = \''+pair_array1[1].strip()+'\' AND CONVERT(datetime,T.LastMatch, 120) >= \''+sdate1+'\' AND CONVERT(datetime,T.LastMatch, 120) <= \''+edate1+'\' AND DATENAME(dw, CONVERT(datetime,T.LastMatch, 120)) IN ('+dayStr+')) AS P GROUP BY P.FiveMinutesPeriod) AP'
data2 = pd.read_sql(qry2,cnxn)
print(qry2)
print(data2)
data2.columns = ['resampledTime', 'Incident_Avg']
cnxn.close()  
data2.dtypes
df1['resampledTime'] = pd.to_datetime(df1['resampledTime'], format='%Y-%m-%d %H:%M:%S', utc=True)

df1['date'] = df1['resampledTime'].dt.date

df1['date'] = df1['date'].astype(str)

df1['time'] = df1['resampledTime'].dt.time

#df3 = df1.set_index('resampledTime')
pivoted_table = df1.pivot(index='time', columns='date', values='Incident_Avg')
pivoted_table['Historical_mean'] =pivoted_table.mean(axis=1)    
pivoted_table['Standard_deviation'] = pivoted_table.std(axis= 1)
data2['resampledTime'] = pd.to_datetime(data2['resampledTime'], format='%Y-%m-%d %H:%M:%S', utc=True)

data2['date'] = data2['resampledTime'].dt.date

data2['time'] = data2['resampledTime'].dt.time

data2['Incident_Avg'] = data2['Incident_Avg'].astype(float)

data3 = data2.groupby(['time'], 
									  as_index=False)['Incident_Avg'].mean()
#traveldata_final = traveltime_data.join(traveltime_data1, how='outer')
traveldata_final = pd.merge(data2,data3,how = 'inner',on = 'time')
print(traveldata_final.columns)
#del traveldata_final['Incident_Avg_x']

traveldata_final.set_index('time', inplace=True)
#pd.merge(pivoted_table,traveldata_final, on = 'time')

final_data = pivoted_table.join(traveldata_final, how='outer')
final_data1 = final_data[['resampledTime','Historical_mean','Incident_Avg_y']]    
final_data1['Variance'] = final_data1.var(axis= 1)    
del final_data1['Historical_mean']
del final_data1['Incident_Avg_y']
del final_data1['resampledTime']    
final_data2 = final_data.join(final_data1, how='outer')        
del final_data2['date']
del final_data2['Incident_Avg_x']

final_data2.dropna(inplace=True)
final_data2 = final_data.round(2)
final_data2.columns
final_data2.rename(columns = {'Incident_Avg_y':'Incident_Avg'},inplace=True)
final_data2.columns
final_data2['time'] = final_data2['resampledTime'].dt.time
del final_data2['resampledTime']
print(final_data2)
Output = final_data2.to_json(orient='records', date_format='iso')
print(Output)
response = open(os.environ['res'], 'w')
response.write(Output)
response.close()


