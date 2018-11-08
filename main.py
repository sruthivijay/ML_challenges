
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import random
import time
import sys

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
import iothub_client
# pylint: disable=E0611
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=bsmiothub.azure-devices.net;DeviceId=bsmedge;SharedAccessKey=9jzTsPjoHJnTp5Q01qcBBAx4KLNrPpEqKZyxFSCIpCQ="

# Using the MQTT protocol.
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000

# Define the JSON message to send to IoT Hub.
coreData_speed = 16.04
coreData_heading = 14.1625
coreData_position_lat = [39.7428410,	39.7428169,	39.7428451,	
39.7428116,	39.7427895,	39.7428517,	39.7428816,	39.7431656,	39.7431698,	39.7432084,	39.7431904,	39.7431825,	
39.7431859,	39.7432129,	39.7432266,	39.7432459,	39.7432370,	39.7432684,	39.7432819,	39.7432864,	39.7432190,	
39.7533279,	39.7433142,	39.7433051,	39.7432956,	39.7433369,	39.7433558,	39.7435253,	39.7442069,39.7441791,	
39.7439697,39.7439672,39.7439253,39.7438726,39.7437720,39.7435558,39.7437990,39.7438040,39.7435332
]
coreData_position_long = [-104.9936400,-104.9936725,-104.9939717,-104.9936793,-104.9937128,-104.9939813,-104.9940257,
-104.9944216,-104.9944275,-104.9944803,-104.9944571,-104.9944454,-104.9944513,-104.9944861,-104.9945033,
-104.9945254,-104.9945136,-104.9945552,-104.9945719,-104.9945777,-104.9945834,-104.9946296,-104.9946117,
-104.9946000,-104.9945892,-104.9946410,-104.9946636,-104.9948874,-104.9957746,-104.9957375,-104.9954647,
-104.9954611,-104.9954088,-104.9953427,-104.9952085,-104.9949282,-104.9952438,-104.9952512,-104.9948977]

coreData_speed = [3.94,4.36,5.22,4.40,4.52,5.26,5.38,6.80,6.84,6.86,6.80,6.82,6.80,6.90,6.96,6.96,
6.96,6.92,6.90,6.92,6.90,6.92,6.92,6.90,6.90,6.86,6.78,5.94,3.48,3.64,4.02,4.00,3.76,3.56,4.30,5.92,
4.02,4.06,5.90]
MSG_TXT = "{\"Speed\": %.2f,\"Data_heading\": %.2f,\"Latitude\": %.7f,\"Longitude\": %.7f}"

def send_confirmation_callback(message, result, user_context):
    print ( "IoT Hub responded to message with status: %s" % (result) )

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
        i = 0
        while i != 39:
            # Build the message with simulated telemetry values.
            #Speed = coreData_speed + (random.random() * 15)
            Speed = coreData_speed[i]
            Data_heading = coreData_heading + (random.random() * 20)
            lat = coreData_position_lat[i]
            long_ = coreData_position_long[i]
            msg_txt_formatted = MSG_TXT % (Speed, Data_heading, lat, long_)
            message = IoTHubMessage(msg_txt_formatted)
            i=i+1
            #if i == 38:
            #    i = 0
            #else:
            #    i=i+1

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.
            prop_map = message.properties()
            if Speed < 4:
                prop_map.add("SpeedAlert", "true")
            else:
                prop_map.add("SpeedAlert", "false")

            # Send the message.
            print( "Sending message: %s" % message.get_string() )
            client.send_event_async(message, send_confirmation_callback, None)
            time.sleep(30)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()
    print("completed!!!!!!!!!!!")