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
        print("******-------   Start data Filtering  ------****** ")
        # define behavior for receiving an input message on input1
        while True:
            input_message = await module_client.receive_message_on_input("input1")  # blocking call
            print("the data in the message received on input1 was ")
            print(input_message.data)
            print("custom properties are")
            print(input_message.custom_properties)
            sample_data = input_message.data
            decoded_sample = sample_data.decode('utf-8')
            decoded_dict = json.loads(decoded_sample)
            data = decoded_dict['data'][0]
            result = {}
            if data['animal_activity'] == "" or data['temp_without_drink_cycles'] == "":
                continue
            # for key in data:
            #     if data[key] != "" and dat
            if data['animal_activity'] != "" and float(data['animal_activity']) > 10:
                print("!! **  abnormal record - (" +
                              "animal_activity"+","+str(data['animal_activity'])+")")
                result['filter'] = True

            result['data'] = [data]
            j_data = json.dumps(result)
            output = bytes(j_data, encoding='utf8')
            await module_client.send_message_to_output(output, "output1")

        # define behavior for halting the application
        # def stdin_listener():
        #     while True:
        #         try:
        #             selection = input("Press Q to quit\n")
        #             if selection == "Q" or selection == "q":
        #                 print("Quitting...")
        #                 break
        #         except:
        #             time.sleep(10)

        # # Schedule task for C2D Listener
        # listeners = asyncio.gather(input1_listener(module_client))

        # print ( "The sample is now waiting for messages. ")

        # # Run the stdin listener in the event loop
        # loop = asyncio.get_event_loop()
        # user_finished = loop.run_in_executor(None, stdin_listener)

        # Wait for user to indicate they are done listening for messages
        # await user_finished

        # Cancel listening
        # listeners.cancel()

        # Finally, disconnect
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