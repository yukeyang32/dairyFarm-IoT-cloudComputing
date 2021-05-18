# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import time
import os
import sys
import asyncio
import json
from six.moves import input
import threading
import requests
from azure.iot.device.aio import IoTHubModuleClient

async def main():
    try:
        if not sys.version >= "3.5.3":
            raise Exception( "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version )
        print ( "IoT Hub Client for Python" )

        # The client object is used to interact with your Azure IoT hub.
        module_client = IoTHubModuleClient.create_from_edge_environment()

        # connect the client.
        await module_client.connect()
        print("******-------   Start Machine Learning Predicting  ------****** ")
        # define behavior for receiving an input message on input1
        while True:
            input_message = await module_client.receive_message_on_input("amlInput")  # blocking call
            print("the data in the message received on input1 was ")
            print(input_message.data)
            print("custom properties are")
            print(input_message.custom_properties)
            sample_data = input_message.data
            decoded_sample = sample_data.decode('utf-8')
            decoded_dict = json.loads(decoded_sample)
            data = decoded_dict['data'][0]
            result = {}
            result['data'] = [data]
            # scoring_url = 'http://127.0.0.1:5001/score'
            pred_data = json.dumps({'data': {
              "animal_activity": float(data['animal_activity']),
              "temp_without_drink_cycles": float(data['temp_without_drink_cycles'])}})

            pred_data = bytes(pred_data,encoding = 'utf8')
            prediction = aci_service.run(input_data = pred_data)
            # resp = requests.post(scoring_url, pred_data)
            result['label'] = prediction[0]['label']
            j_data = json.dumps(result)
            output = bytes(j_data, encoding='utf8')
            await module_client.send_message_to_output(output, "amlOutput")
        await module_client.disconnect()

    except Exception as e:
        print ( "Unexpected error %s " % e )
        raise

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

    # If using Python 3.7 or above, you can use following code instead:
    # asyncio.run(main())