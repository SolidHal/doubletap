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


class DoubleTap:

    blank_code = 0b00000


    #TODO: create these automatically or replace them altogether
    left_tap = {"name":"left", "mac":"CE:BB:BB:2E:60:99"}
    right_tap = {"name":"right", "mac":"F3:64:D7:5D:8D:D1"}
    taps_by_mac = {left_tap["mac"]:left_tap["name"], right_tap["mac"]:right_tap["name"]}

    def __init__(self, lefttap, righttap, doublelayer):
        self.left = lefttap
        self.right = righttap
        self.doublelayer = doublelayer

    def _getCommand(self, hand, otherhand, prefix, code):
        # for layer + modifier prefixes, we have to find the layer in the prefix list
        # there can only ever be one internal layer in a prefix
        # we treat the blank code as an internal prefix that allows any tap from the prefix or cmd to be on the other hand
        # default to no internal prefixes on the combined prefix/cmd layer
        # if this is None for all prefixes in left_prefix, then we have only external prefixes
        cmdlayer = otherhand.default_layer
        for pre in prefix:
            print(pre)
            layer = hand.getOtherHandLayer(pre)
            if (layer != None):
                cmdlayer = layer
                # copy all of prefix over besides the internal layer so we don't try an send an internal layer marker
                # to the keyboard parser
                print("removing {} from {}".format(pre, prefix))
                prefix = [n for n in prefix if n != pre]
                print("prefix after removing: {}".format(prefix))
                break

        print(cmdlayer)
        cmd = otherhand.getCommand(code, cmdlayer)
        if (cmd !=None ):
            # this is legal
            # return combination of both lists
            return (prefix + cmd)
        else:
            return None

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
        print("("+hand+") recognized=" + str(code))
        if (hand == "left"):
            rightcode = self.blank_code
            leftcode = code
        elif (hand == "right"):
            leftcode = self.blank_code
            rightcode = code
        else:
            print ("Invalid hand arg")
            return None

        keys = self.parse(leftcode, rightcode)
        print("("+hand+") recognized code =" + str(code) + " parsed to keys =" + str(keys))

    other_hand = None
    other_hand_code = None
    other_hand_time = None
    other_hand_timer = None

    def detect(self, hand, code):
        now = datetime.now()
        if (self.other_hand != None) and ((now - self.other_hand_time) < timedelta(milliseconds=50)):
            self.other_hand_timer.cancel()
            if (hand == "left"):
                rightcode = self.other_hand_code
                leftcode = code
            elif (hand == "right"):
                leftcode = self.other_hand_code
                rightcode = code
            else:
                print ("Invalid hand arg")
                return None
            print("(dual) recognized (left) recognized code =" + str(leftcode) + " and (right) recognized code = " + str(rightcode))
            command = self.parse(leftcode, rightcode)
            print("(left) recognized code =" + str(leftcode) + " and (right) recognized code = " + str(rightcode) + " parsed to command =" + str(command))
            self.other_hand = None
            return

        self.other_hand = hand
        self.other_hand_code = code
        self.other_hand_time = datetime.now()
        self.other_hand_timer = Timer(0.07, self._timerTap, args = [hand, code])
        self.other_hand_timer.start()


    def onTapped(self, loop, address, identifier, tapcode):
        if (self.taps_by_mac[address] == "right"):
            tapcode = self._reverseBits(tapcode)
        print(self.taps_by_mac[address] + " (" + address + ") tapped " + str(tapcode))
        self.detect(self.taps_by_mac[address], tapcode)



class Tap:

    def __init__(self, address, layer_config):
        self.address = address

        self.layer_config = layer_config
        self.layer_list = layer_config[2]
        # list of cmd layers on the other hand that can be accessed by this hand through prefixes
        self.other_hand_layers = layer_config[3]
        print("other_hand_layers = {}".format(self.other_hand_layers))
        self.prefix_layer = self.layer_config[0]
        self.default_layer = self.layer_config[1]

    def getPrefix(self, code):
        prefix = self.prefix_layer.get(code, None)
        if (prefix != None):
            return prefix.copy()
        else:
            return None

    def getOtherHandLayer(self, prefix):
        print("prefix = {}".format(prefix))
        layer = self.other_hand_layers.get(prefix, None)
        if (layer != None):
            return layer.copy()
        else:
            return None

    def getCommand(self, code, layer):
        return layer.get(code, None)


left_tap = {"name":"left", "mac":"CE:BB:BB:2E:60:99"}
right_tap = {"name":"right", "mac":"F3:64:D7:5D:8D:D1"}
taps_by_mac = {left_tap["mac"]:left_tap["name"], right_tap["mac"]:right_tap["name"]}


def OnMouseModeChange(address, identifier, mouse_mode):
    print(identifier + " changed to mode " + str(mouse_mode))

def OnTapped(loop, address, identifier, tapcode):
    if (taps_by_mac[address] == "right"):
        tapcode = reverseBits(tapcode)
    print(taps_by_mac[address] + " (" + address + ") tapped " + str(tapcode))
    DetectTap(loop, taps_by_mac[address], tapcode)

def OnTapConnected(self, identifier, name, fw):
    print(identifier + " Tap: " + str(name), " FW Version: ", fw)


def OnTapDisconnected(self, identifier):
    print(identifier + " Tap: " + identifier + " disconnected")


def OnMoused(address, identifier, vx, vy, isMouse):
    print(identifier + " mouse movement: %d, %d, %d" % (vx, vy, isMouse))



async def run(loop=None, debug=True):
    # if debug:
    #     import sys

    #     loop.set_debug(True)
    #     h = logging.StreamHandler(sys.stdout)
    #     h.setLevel(logging.WARNING)
    #     logger.addHandler(h)
    left = TapSDK(left_tap["mac"], loop)
    right = TapSDK(right_tap["mac"], loop)

    left_obj = Tap(left_tap["mac"], taplayers.left)
    right_obj = Tap(right_tap["mac"], taplayers.right)
    doubletap = DoubleTap(left_obj, right_obj, taplayers.doublelayer)



    if not await left.client.connect_retrieved():
        print("Error connecting to {}".format(left_tap["mac"]))
        return None

    print("Connected to {}".format(left.client.address))

    await left.set_input_mode(TapInputMode("controller"))
    await left.register_tap_events(doubletap.onTapped)
    await left.register_mouse_events(OnMoused)

    if not await right.client.connect_retrieved():
        print("Error connecting to {}".format(right_tap["mac"]))
        return None

    print("Connected to {}".format(right.client.address))

    await right.set_input_mode(TapInputMode("controller"))
    await right.register_tap_events(doubletap.onTapped)
    await right.register_mouse_events(OnMoused)


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
