# About
wireshark_cdc_acm_decoder is a small script that you can run on a json export of a usb "Export Packet Dissections" "As JSON"

This script is heavily inspired by [Capturing-usb-serial-using-wireshark by Dave Hylands](https://blog.davehylands.com/capturing-usb-serial-using-wireshark/])

It is however implemented in Python not javascript/node and features options for formating the output in a few ways for easier copy pasting into different applications

# Usage
Just run the script though python with no arguments and it prints a help text

As an example (the program output is always up to date, this README may not be):

```
Usage: python wireshark_cdc_acm_decoder.py path_to_json_file [compact|programming]
* compact removes the ':' between the serial bytes thus making it easier
  to paste into things like reveng (https://reveng.sourceforge.io/)
* programming outputs the bytes as hex values separated by ','
  for easy usage in most programming languages
* bin binary output both read and writes in one big blob, only data in binary mode
* binr binary output only reads
* binw binary output only writes
* bintag binary output both read and writes the data is tagged with extra bytes to help id them
```

# Example output

```
W:	89	485.056215000	0f:02:01:00:01:00:f7:30:03:f0
R:	91	485.056583000	0f:02:01:00:02:00:f7:01:9e:8b:f0
W:	93	485.061894000	0f:03:01:00:02:00:f8:00:e0:33:f0
R:	95	485.135584000	0f:03:01:00:02:00:f8:01:c1:23:f0
W:	97	485.139967000	0f:04:00:00:01:00:fa:2d:f5:f0
```