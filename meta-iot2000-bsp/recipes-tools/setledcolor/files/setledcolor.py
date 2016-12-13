#!/usr/bin/python


import mraa
import sys
import os

def redled(state):
 redLedFile = "/sys/class/leds/mpio_uart_led:red:user/brightness"
 if(not os.path.isfile(redledFile)):
  print("Red LED not available")
  return
 file = open(redLedFile,'w')
 if(1==state):
  file.write("1")
 else:
  file.write("0")
 file.close()

def greenled(state):
 ledpin = mraa.Gpio(13)
 ledpin.dir(mraa.DIR_OUT)
 if(1==state):
  ledpin.write(1)
 else:
  ledpin.write(0)

if(len(sys.argv)<2):
 print("Usage: " + sys.argv[0] + " color")
 print("color:")
 print("0\t\tout")
 print("1\t\tgreen")
 print("2\t\tred")
 print("3\t\torange")
 sys.exit()

x = int(sys.argv[1])

if(x%2 == 0):
 greenled(0)
else:
 greenled(1)

if(x/2 == 0):
 redled(0)
else:
 redled(1)



