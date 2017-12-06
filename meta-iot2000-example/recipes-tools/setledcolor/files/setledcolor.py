#!/usr/bin/env python3

import mraa
import sys
import os


def redled(state):
    redLedFile = "/sys/class/leds/mpio_uart_led:red:user/brightness"
    if not os.path.isfile(redLedFile):
        print("Red LED not available")
        return
    file = open(redLedFile, 'w')
    if state == 1:
        file.write("1")
    else:
        file.write("0")
    file.close()


def greenled(state):
    ledpin = mraa.Gpio(13)
    ledpin.dir(mraa.DIR_OUT)
    if state == 1:
        ledpin.write(1)
    else:
        ledpin.write(0)


def usage():
    print("Usage: " + sys.argv[0] + " color")
    print("color:")
    print("\t0 | off")
    print("\t1 | green")
    print("\t2 | red")
    print("\t3 | orange")
    sys.exit()


if len(sys.argv) < 2:
    usage()

try:
    x = {'off': 0, 'green': 1, 'red': 2, 'orange': 3}[sys.argv[1]]
except KeyError:
    try:
        x = int(sys.argv[1])
    except ValueError:
        usage()

if x % 2 == 0:
    greenled(0)
else:
    greenled(1)

if x // 2 == 0:
    redled(0)
else:
    redled(1)
