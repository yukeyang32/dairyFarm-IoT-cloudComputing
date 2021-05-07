# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import time
import os
import sys
import asyncio
import csv, json
from six.moves import input
import threading
from azure.iot.device.aio import IoTHubModuleClient

filepath = "1_DA Project_997.csv"

async def main():
    try:
        if not sys.version >= "3.5.3":
            raise Exception( "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version )
        print ( "IoT Hub Client for Python" )

        # The client object is used to interact with your Azure IoT hub.
        module_client = IoTHubModuleClient.create_from_edge_environment()

        # connect the client.
        await module_client.connect()
        print("IoT Hub module client initialized.") 
        # define behavior for receiving an input message on input1
        with open(filepath, mode='r') as csv_file:
            while True:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                col_len = 0
                col_name = []
                for row in csv_reader:
                    if line_count == 0:
                        print(f'Column names are {", ".join(row)}')
                        line_count += 1
                        col_name = [row[i] for i in range(len(row))]
                    else:
                        msg = [row[i] for i in range(len(row))]
                        data = {}
                        for i in range(len(row)):
                            data[col_name[i]] = msg[i]
                        j_data = json.dumps({'data': [data]})
                        output = bytes(j_data, encoding='utf8')
                        line_count += 1

                        # send to next client
                        await module_client.send_message_to_output(output, "outputs")

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

        # # Wait for user to indicate they are done listening for messages
        # await user_finished

        # # Cancel listening
        # listeners.cancel()

        # # Finally, disconnect
        # await module_client.disconnect()

    except Exception as e:
        print ( "Unexpected error %s " % e )
        raise

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

    # If using Python 3.7 or above, you can use following code instead:
    # asyncio.run(main())