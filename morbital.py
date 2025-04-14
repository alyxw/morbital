import serial
import time
from enum import Enum


def sendAction(target, payload):
    target.write(serial.to_bytes(payload))


# clearDisplay(target)
# expects the following values:
#     target - the initialized serial device of the display
# # Clears the display.
def clearDisplay(target):
    payload = [0xFE, 0x58]
    sendAction(target, payload)


# resetCursor(target)
# expects the following values:
#     target - the initialized serial device of the display
# Sends the cursor to the top left corner of the display.
def resetCursor(target):
    payload = [0xFE, 0x48]
    sendAction(target, payload)


# resetDisplay(target)
# expects the following values:
#     target - the initialized serial device of the display
# Performs a soft reset of the display
def resetDisplay(target):
    payload = [0xFE, 0xFD, 0x4D, 0x4F, 0x75, 0x6E]
    sendAction(target, payload)
    time.sleep(4)  # sleep for 4 seconds to allow the display to come back up before performing additional commands


# setCursorPosition(target,x,y)
# expects the following values:
#     target - the initialized serial device of the display
#     x - column from 1-27
#      y - row from 1-8
# sets the cursor row/column
def setCursorPosition(target, x, y):
    if (x < 1 or x > 27 or y < 1 or y > 8):
        raise Exception("The position specified is out of range.")
    payload = [0xFE, 0x47, x, y]
    sendAction(target, payload)


# setCursorCoordinate(target,x,y)
# expects the following values:
#     target - the initialized serial device of the display
#     x - pixel from 1-27
#      y - pixel from 1-8
# sets the cursor pixel position
def setCursorCoordinate(target, x, y):
    if (x < 1 or x > 192 or y < 1 or y > 64):
        raise Exception("The coordinate specified is out of range.")
    payload = [0xFE, 0x79, x, y]
    sendAction(target, payload)


def keypadBacklightOff(target):
    payload = [0xFE, 0x9B]
    sendAction(target, payload)


def setDeviceKeypadBacklightBrightness(target, brightness):
    payload = [0xFE, 0x9C, brightness]
    sendAction(target, payload)


def displayBacklightOff(target):
    payload = [0xFE, 0x46]
    sendAction(target, payload)


def displayBacklightOn(target, minutes):
    if (minutes > 255 or minutes < 0):
        raise Exception("minutes out of range")
    payload = [0xFE, 0x42, minutes]
    sendAction(target, payload)


def setBacklightBrightness(target, brightness):
    if (brightness < 0 or brightness > 255):
        raise Exception("brightness out of range")
    payload = [0xFE, 0x99, brightness]
    sendAction(target, payload)


def setStartupBacklightBrightness(target, brightness):
    if (brightness < 0 or brightness > 255):
        raise Exception("brightness out of range")
    payload = [0xFE, 0x98, brightness]
    sendAction(target, payload)


def setDisplayContrast(target, contrast):
    if (contrast < 0 or contrast > 255):
        raise Exception("contrast out of range")
    payload = [0xFE, 0x50, contrast]
    sendAction(target, payload)


def setStartupDisplayContrast(target, contrast):
    if (contrast < 0 or contrast > 255):
        raise Exception("contrast out of range")
    payload = [0xFE, 0x91, contrast]
    sendAction(target, payload)

def setDeviceLED(target, led, colour):
    if (led < 0 or led > 2 or colour > 3 or colour < 0):
        raise Exception("LED must be 0-2 and color must be 0-3")
    payload = [0xFE, 0x5A, led, colour]
    sendAction(target, payload)

