#!/bin/python3


import os

import taplayers

from threading import Timer
from tapsdk import TapSDK, TapInputMode
from tapsdk.models import AirGestures
from datetime import timedelta, datetime
from asgiref.sync import async_to_sync

import asyncio
import logging
from bleak import _logger as logger


#mappings can be partially auto generated
# ex: ctrl + letter is simply
#     ctrl_tap_code + letter_tap_code
# or
#     letter_tap_code + ctrl_tap_code
#depending on which hand has the letter




class DoubleTap:

    blank_code = 0b00000

    def __init__(self, lefttap, righttap, doublelayer):
        self.left = lefttap
        self.right = righttap
        self.doublelayer = doublelayer
        self.name = "doubletap"

        self.taplock = False

    async def register(self):
        await self.left.tap_sdk.register_tap_events(self.onTapped)
        await self.left.tap_sdk.register_mouse_events(self.onMoused)

        await self.right.tap_sdk.register_tap_events(self.onTapped)
        await self.right.tap_sdk.register_mouse_events(self.onMoused)

    # wrapper to send keys using
    # https://github.com/asweigart/pyautogui
    # input: a list of keys to press simultaneously
    def send_key_pyautogui(key):
        pyautogui.press(key)

    # wrapper to send keys using
    # https://github.com/boppreh/keyboard#keyboard.send
    def send_key_boppreh_keyboard(key):
        keystring = ""
        for i in range(0, (len(key)-1) ):
            keystring = keystring + key[i] + "+"

        last = len(key) - 1
        keystring = keystring + key[last]
        keyboard.send(keystring)

    def _send(self, keys, hand):
        print("( {} ) recognized command = {}".format(hand.name, keys))

        if (keys == None):
            return

        if (taplayers.taplock_key in keys):
            self.taplock = not self.taplock
            print("taplock set to {}".format(self.taplock))
            return

        if (self.taplock):
            print("#### TAPLOCKED ####")
            return

        #TODO: call one of the send_key wrapper functions




    def _getCommand(self, hand, otherhand, prefix, code):
        # for layer + modifier prefixes, we have to find the layer in the prefix list
        # there can only ever be one internal layer in a prefix
        # we treat the blank code as an internal prefix that allows any tap from the prefix or cmd to be on the other hand
        # default to no internal prefixes on the combined prefix/cmd layer
        # if this is None for all prefixes in left_prefix, then we have only external prefixes
        cmdlayer = otherhand.default_layer
        for pre in prefix:
            layer = hand.getOtherHandLayer(pre)
            if (layer != None):
                cmdlayer = layer
                # copy all of prefix over besides the internal layer so we don't try an send an internal layer marker
                # to the keyboard parser
                prefix = [n for n in prefix if n != pre]
                break

        cmd = otherhand.getCommand(code, cmdlayer)
        if (cmd !=None ):
            # this is legal
            # return combination of both lists
            return (prefix + cmd)
        else:
            return None

    # parses the following situations:
    # 1) a one handed tap, one normal code and one blank code where either a command or prefix key is pressed ("ctrl", or "q")
    # 2) a prefix and command 2 handed tap, the prefix decides how the command is parsed and can be a combination of internal (layers) and external (shift, ctrl, win) prefixes
    # 3) special 2 handed "doubletaps" where 2 handed taps that wouldn't make sense ("win" and "win" or "q" and "q") are instead mapped to unique functions
    # 4) and internal layer prefix is tapped with no other taps. This should be considered a non-tap
    def parse(self, leftcode, rightcode):
        left_prefix = self.left.getPrefix(leftcode)
        right_prefix = self.right.getPrefix(rightcode)

        #handle right taps with/without left prefixes
        #don't want to handle left prefix taps with no right tap
        if ( (left_prefix != None) and (rightcode != self.blank_code) ):
            keys = self._getCommand(self.left, self.right, left_prefix, rightcode)
            if (keys != None):
                return keys

        #handle left taps with/without right prefixes
        #don't want to handle right prefix taps with no left taps
        if ( (right_prefix != None) and (leftcode != self.blank_code) ):
            keys = self._getCommand(self.right, self.left, right_prefix, leftcode)
            if (keys != None):
                return keys

        # if we are this far along, we have found nothing. Maybe its a special double tap code? 
        leftcode = leftcode<<5
        doublecode = leftcode | rightcode
        keys = self.doublelayer.get(doublecode, None)
        if (keys != None):
            return keys

        #elsewise we found nothing
        return None


    def _reverseBits(self, code):
        return int('{:05b}'.format(code)[::-1], 2)

    def _timerTap(self, hand, code):
        print("("+hand.name+") recognized=" + str(code))
        if (hand == self.left):
            rightcode = self.blank_code
            leftcode = code
        elif (hand == self.right):
            leftcode = self.blank_code
            rightcode = code
        else:
            print ("Invalid hand arg")
            return None

        keys = self.parse(leftcode, rightcode)
        self._send(keys, hand)

    other_hand = None
    other_hand_code = None
    other_hand_time = None
    other_hand_thread = None

    def detect(self, hand, code):
        now = datetime.now()
        if (self.other_hand != None) and ((now - self.other_hand_time) < timedelta(milliseconds=60)):
            self.other_hand_thread.cancel()
            if (hand == self.left):
                rightcode = self.other_hand_code
                leftcode = code
            elif (hand == self.right):
                leftcode = self.other_hand_code
                rightcode = code
            else:
                print ("Invalid hand arg")
                return None
            print("(dual) recognized (left) recognized code =" + str(leftcode) + " and (right) recognized code = " + str(rightcode))
            keys = self.parse(leftcode, rightcode)
            self._send(keys, self)
            self.other_hand = None
            return

        self.other_hand = hand
        self.other_hand_code = code
        self.other_hand_time = datetime.now()
        self.other_hand_thread = Timer(0.07, self._timerTap, args = [hand, code])
        self.other_hand_thread.start()


    ### Callbacks ###
    def onTapped(self, loop, address, identifier, tapcode):
        hand = None
        if (address == self.right.address):
            tapcode = self._reverseBits(tapcode)
            hand = self.right
        else:
            hand = self.left
        print(hand.name + " (" + address + ") tapped " + str(tapcode))
        self.detect(hand, tapcode)

    def onMoused(self, address, identifier, vx, vy, isMouse):
        print(identifier + " mouse movement: %d, %d, %d" % (vx, vy, isMouse))


class Tap:

    def __init__(self, address, name, layer_config, loop):
        self.address = address
        self.name = name

        self.layer_config = layer_config
        self.layer_list = layer_config[2]
        # list of cmd layers on the other hand that can be accessed by this hand through prefixes
        self.other_hand_layers = layer_config[3]
        self.prefix_layer = self.layer_config[0]
        self.default_layer = self.layer_config[1]
        self.tap_sdk = TapSDK(address, loop)

    async def connect(self):
        if not await self.tap_sdk.client.connect_retrieved():
            print("Error connecting to {}".format(self.address))
            return None
        print("Connected to {}".format(self.tap_sdk.client.address))
        await self.tap_sdk.set_input_mode(TapInputMode("controller"))


    def getPrefix(self, code):
        prefix = self.prefix_layer.get(code, None)
        if (prefix != None):
            return prefix.copy()
        else:
            return None

    def getOtherHandLayer(self, prefix):
        layer = self.other_hand_layers.get(prefix, None)
        if (layer != None):
            return layer.copy()
        else:
            return None

    def getCommand(self, code, layer):
        key = layer.get(code, None)
        if (key == None):
            return None
        for k in key:
            if (not isinstance(k, str)):
                return None
        return layer.get(code, None)




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
    doubletap = DoubleTap(left, right, taplayers.doublelayer)
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
