import blescan
import sys
import requests
import datetime
import time
import bluetooth._bluetooth as bluez
import pygame
import os
import subprocess

secDelay = 60  # pause for network to spin up, usually 60
delay = 600  # delay between updates
beerName = 'test'
batchId = 'TestBatch_01'
postUrl = 'Enter Your URL Here'

# BLE devices (like the tilt) work primarily using advertisements.
# The first section of any advertisement is the universally unique identifier.
# Tilt uses a particular identifier based on the colour of the deviceblack = 'a495bb30c5b14b44b5121370f02d74de'
red = ' A495BB10C5B14B44B5121370F02D74DE'
green = 'A495BB20C5B14B44B5121370F02D74DE'
purple = 'A495BB40C5B14B44B5121370F02D74DE'
orange = 'A495BB50C5B14B44B5121370F02D74DE'
blue = 'A495BB60C5B14B44B5121370F02D74DE'
yellow = 'A495BB70C5B14B44B5121370F02D74DE'
pink = 'A495BB80C5B14B44B5121370F02D74DE'

# The default device for bluetooth scan. If you're using a bluetooth dongle you may have to change this.
dev_id = 0


def get_data():
    try:
        sock = bluez.hci_open_dev(dev_id)
    except:
        print("error accessing bluetooth adapter...")
        sys.exit(1)
    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)
    got_data = 0
    data = {}
    # scan BLE advertisements until we see one matching our tilt uuid
    while got_data == 0:
        device_list = blescan.parse_events(sock, 10)
        for beacon in device_list:
            output = beacon.split(',')
            if output[1] == black:
                got_data = 1
                data = {
                    'time': datetime.datetime.now(),
                    'sg': float(output[3]) / 1000,
                    'temp': float(output[2]),
                    'beer_name': beerName,
                    'batch_id': batchId
                }
    blescan.hci_disable_le_scan(sock)
    return data


def main():
    while True:
        data = get_data()
        r = requests.post(postUrl, data)
        print(r)
        print('SG: ' + data.tiltSG + ' -- Temp:' + data.temp)
        sleep(updateSecs)


if __name__ == "__main__":
    main()
