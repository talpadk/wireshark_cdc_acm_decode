#!/usr/bin/python

import json

import sys
import os
if len(sys.argv)<2:
  print("Usage: python wireshark_cdc_acm_decoder.py path_to_json_file [compact|programming|bin|binr|binw|bintag]")
  print("* compact removes the ':' between the serial bytes thus making it easier")
  print("  to paste into things like reveng (https://reveng.sourceforge.io/)")
  print("* programming outputs the bytes as hex values separated by ','")
  print("  for easy usage in most programming languages")
  print("* bin binary output both read and writes in one big blob, only data in binary mode")
  print("* binr binary output only reads")
  print("* binw binary output only writes")
  print("* bintag binary output both read and writes the data is tagged with extra bytes to help id them")
  os._exit(1)

BIN_READ_ONLY = 1
BIN_WRITE_ONLY = 2
BIN_BOTH = 3
BIN_BOTH_TAGGED = 4

BIN_READ_TAG  = bytes([27, ord('R'), ord(':')])
BIN_WRITE_TAG = bytes([27, ord('W'), ord(':')])


file = sys.argv[1]
compact = False
programming = False
binaryType = 0

if len(sys.argv)>2:
  remaining = sys.argv[2:]
  if 'compact' in remaining:
    compact = True
  if 'programming' in remaining:
    programming = True
  if 'bin' in remaining:
    binaryType = BIN_BOTH
  if 'binr' in remaining:
    binaryType = BIN_READ_ONLY
  if 'binw' in remaining:
    binaryType = BIN_WRITE_ONLY
  if 'bintag' in remaining:
    binaryType = BIN_BOTH_TAGGED


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

      if binaryType == 0:
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

      else:
        doOutput = True
        if binaryType == BIN_READ_ONLY and (not isRead):
          doOutput = False
        if binaryType == BIN_WRITE_ONLY and isRead:
          doOutput = False
        if doOutput:
          if binaryType == BIN_BOTH_TAGGED:
            if isRead:
              sys.stdout.buffer.write(BIN_READ_TAG)
            else:
              sys.stdout.buffer.write(BIN_WRITE_TAG)
          for x in data.split(':'):
            sys.stdout.buffer.write(bytes([int(x, 16)]))


