#!/bin/python3
# Copyright Hal Emmerich <SolidHal> 2020

import os
import taplayers
from doubletap import Tap, DoubleTap

import asyncio



def OnMouseModeChange(address, identifier, mouse_mode):
    print(identifier + " changed to mode " + str(mouse_mode))

def OnTapConnected(self, identifier, name, fw):
    print(identifier + " Tap: " + str(name), " FW Version: ", fw)


def OnTapDisconnected(self, identifier):
    print(identifier + " Tap: " + identifier + " disconnected")



async def run(loop=None, debug=True):

    left_tap = {"name":"left", "mac":"CE:BB:BB:2E:60:99"}
    right_tap = {"name":"right", "mac":"F3:64:D7:5D:8D:D1"}
    taps_by_mac = {left_tap["mac"]:left_tap["name"], right_tap["mac"]:right_tap["name"]}

    left = Tap(left_tap["mac"], "left", taplayers.left, loop)
    await left.connect()
    right = Tap(right_tap["mac"], "right", taplayers.right, loop)
    await right.connect()
    doubletap = DoubleTap(left, right, taplayers.doublelayer, taplayers)
    await doubletap.register()


    #TODO: could use tap.client.list_connected_taps to detect disconnects?
    while (True):
        await asyncio.sleep(100.0)

        # print("Connected to {}".format(client.client.address))
        # await client.register_raw_data_events(OnRawData)
        # await client.register_mouse_events(OnMoused)

        # logger.info("Changing to text mode")
        #await client.set_input_mode(TapInputMode("text"))
        # await asyncio.sleep(30))
        #logger.info("Changing to raw mode")
        #await client.set_input_mode(TapInputMode("raw"))

        # await client.send_vibration_sequence([100, 200, 300, 400, 500])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop, True))
