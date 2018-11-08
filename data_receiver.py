# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 11:17:40 2018

@author: sruthi.vs
"""

import os
import sys
#import logging
from azure.eventhub import EventHubClient, Receiver, Offset

#import examples
#logger = examples.get_logger(logging.INFO)

# Address can be in either of these formats:
# "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@<mynamespace>.servicebus.windows.net/myeventhub"
# "amqps://<mynamespace>.servicebus.windows.net/myeventhub"
ADDRESS = 'sb://bsmdata.servicebus.windows.net/bsmprocess'
USER = 'rootpolicy'
KEY = 'zgzJhiPxpW4PE5qRhQvyCl3/YBfer3VyQ0F3MCajjmY='
CONSUMER_GROUP = "$default"
OFFSET = Offset("-1")
PARTITION = "1"


total = 0
last_sn = -1
last_offset = "-1"

try:
    if not ADDRESS:
        raise ValueError("No EventHubs URL supplied.")
    client = EventHubClient(ADDRESS, debug=False, username=USER, password=KEY)
    receiver = client.add_receiver(CONSUMER_GROUP, PARTITION, prefetch=5000, offset=OFFSET)
    client.run()
    try:
        batched_events = receiver.receive(timeout=20)
    except:
        raise
    finally:
        client.stop()
    for event_data in batched_events:
        last_offset = event_data.offset.value
        last_sn = event_data.sequence_number
        total += 1
        print("Partition {}, Received {}, sn={} offset={}".format(
            PARTITION,
            total,
            last_sn,
            last_offset))

except KeyboardInterrupt:
    pass


messages = event_data.message

process_events_async(context, messages)


event_data.sequence_number

msg = Message()

msg.body


uamqp.message.Message

