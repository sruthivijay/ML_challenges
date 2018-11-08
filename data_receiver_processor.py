# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 16:59:47 2018

@author: sruthi.vs
"""

import os
import sys
#import logging
from azure.eventhub import EventHubClient, Receiver, Offset, EventData
import pandas as pd
import json

#import examples
#logger = examples.get_logger(logging.INFO)

# Address can be in either of these formats:
# "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@<mynamespace>.servicebus.windows.net/myeventhub"
# "amqps://<mynamespace>.servicebus.windows.net/myeventhub"
ADDRESS = 'sb://bsmdatasource.servicebus.windows.net/databsm'
USER = 'rootpolicy'
KEY = 'LtImOadqyO85BvRpp1INvOHsyhbu2URBFSu76Vgh5CY='
CONSUMER_GROUP = "$default"
OFFSET = Offset("-1")
PARTITION = "0"


total = 0
last_sn = -1
last_offset = "-1"
data_batch = []
data = []

try:
    if not ADDRESS:
        raise ValueError("No EventHubs URL supplied.")
    client = EventHubClient(ADDRESS, debug=False, username=USER, password=KEY)
    receiver = client.add_receiver(CONSUMER_GROUP, PARTITION, prefetch=5000, offset=OFFSET)
    client.run()
    batched_events = receiver.receive()
    for message in batched_events:
        event_data = next(message.body)
        #data = next(event_data)
        data_batch.append(event_data)
        last_offset = message.offset.value
        last_sn = message.sequence_number
        total += 1
        print("Partition {}, Received {}, sn={} offset={}".format(
            PARTITION,
            total,
            last_sn,
            last_offset))

except KeyboardInterrupt:
    pass
finally:
    client.stop()
    
data = next(message.body).decode("utf-8")

final_data = pd.read_json(event_data,lines = True)

def data_process(BSM_DATA):
    
    BSM_DATA1 = BSM_DATA.round({'coreData_position_lat': 3,'coreData_position_long' : 3})

    Count_by_latlong = BSM_DATA1.groupby(['coreData_position_lat','coreData_position_long'], 
                                      as_index=False)['coreData_speed'].count()

    Count_by_latlong = Count_by_latlong.rename(columns= {'coreData_speed': 'row_count'})

    MeanSpeed_by_latlong = BSM_DATA1.groupby(['coreData_position_lat','coreData_position_long'], 
                                      as_index=False)['coreData_speed'].mean()
    MeanSpeed_by_latlong1 = MeanSpeed_by_latlong.rename(columns= {'coreData_speed': 'Mean_speed'})

    BSM_DATA = pd.merge(BSM_DATA1,Count_by_latlong,how = 'inner',on = ['coreData_position_lat','coreData_position_long'])

    BSM_DATA = pd.merge(BSM_DATA,MeanSpeed_by_latlong1,how = 'inner',on = ['coreData_position_lat','coreData_position_long'])


    Violated_count = BSM_DATA[BSM_DATA['coreData_speed'] >= BSM_DATA['Mean_speed']].groupby(['Mean_speed']).size().reset_index(name='count')

    BSM_DATA = pd.merge(BSM_DATA,Violated_count,how = 'inner',on = ['Mean_speed'])

    BSM_DATA = BSM_DATA.rename(columns= {'count': 'violation_count'})

    return(BSM_DATA)

BSM_DATA = pd.read_json(data,lines=True)

final_data = data_process(BSM_DATA)

final_data.to_csv("D:/DSRC/Processed_data_SMALL.csv")