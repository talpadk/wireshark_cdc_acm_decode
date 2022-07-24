#!/usr/bin/python

import json

import sys
import os
if len(sys.argv)<2:
  print("Usage: python wireshark_cdc_acm_decoder.py path_to_json_file [compact|programming]")
  print("* compact removes the ':' between the serial bytes thus making it easier")
  print("  to paste into things like reveng (https://reveng.sourceforge.io/)")
  print("* programming outputs the bytes as hex values separated by ','")
  print("  for easy usage in most programming languages")
  os._exit(1)

file = sys.argv[1]
compact = False
programming = False 

if len(sys.argv)>2:
  remaining = sys.argv[2:]
  if 'compact' in remaining:
    compact = True
  if 'programming' in remaining:
    programming = True


with open(file, 'rb') as fileHandle:
  data = json.load(fileHandle)
  for object in data:
    canProcess = True
    if canProcess and not '_source' in object:
      canProcess = False
    if canProcess and not 'layers' in object['_source']:
      canProcess = False

    #probably should also check the one below for existence 
    layers = object['_source']['layers']
    frame = layers['frame']
    frameNumber = frame['frame.number']
    timeRelative = frame['frame.time_relative']
    usb = layers['usb']
    isRead = usb['usb.dst'] == 'host'

    if not canProcess:
      print("WARNING unable to process: "+str(object))

    #empty objects are allowed with out a warning
    if canProcess and not 'usb.capdata' in layers:
      canProcess = False
    
    if canProcess:
      direction = "W:"
      if isRead:
        direction = "R:"
      data = layers['usb.capdata']
      dataAsString = data
      if compact:
        dataAsString = ""
        for x in  data.split(':'):
          dataAsString += x
      if programming:
        dataAsList = []
        for x in data.split(':'):
          dataAsList.append("0x{:02X}".format(int(x, 16)))
        dataAsString = ', '.join(dataAsList)

      print("{:s}\t{:s}\t{:s}\t{:s}".format(direction, frameNumber, timeRelative, dataAsString))

