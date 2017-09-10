#goal:
#read tilt hydrometer
#diplay data
#pause xyz seconds (usually 600)
#repeat

#initialization stuff

import blescan
import sys
import requests
import datetime
import time
import bluetooth._bluetooth as bluez
import pygame
import os


from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

secDelay = 60 #pause for network to spin up, usually 60
delay = 600 #delay between spreadsheet updates, usually 600

beerName ='test'
batchId = 'TestBatch_01'

#Assign uuid's of various colour tilt hydrometers. BLE devices like the tilt work primarily using advertisements.
#The first section of any advertisement is the universally unique identifier. Tilt uses a particular identifier based on the colour of the device
red     = 'a495bb10c5b14b44b5121370f02d74de'
green   = 'a495bb20c5b14b44b5121370f02d74de'
black   = 'a495bb30c5b14b44b5121370f02d74de'
purple  = 'a495bb40c5b14b44b5121370f02d74de'
orange  = 'a495bb50c5b14b44b5121370f02d74de'
blue    = 'a495bb60c5b14b44b5121370f02d74de'
yellow  = 'a495bb70c5b14b44b5121370f02d74de'
pink    = 'a495bb80c5b14b44b5121370f02d74de'

#The default device for bluetooth scan. If you're using a bluetooth dongle you may have to change this.
dev_id = 0

#scan BLE advertisements until we see one matching our tilt uuid
def getdata():
        try:
                sock = bluez.hci_open_dev(dev_id)
        except:
                print "error accessing bluetooth device..."
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                draw.text((x, top),"error accessing bluetooth device...",  font=font, fill=255)
                disp.image(image)
                disp.display()
                sys.exit(1)

        blescan.hci_le_set_scan_parameters(sock)
        blescan.hci_enable_le_scan(sock)

        gotData = 0
        while (gotData == 0):

                returnedList = blescan.parse_events(sock, 10)
                #lcd.message(returnedList)
                #print returnedList ###
                for beacon in returnedList: #returnedList is a list datatype of string datatypes seperated by commas (,)
                        output = beacon.split(',') #split the list into individual strings in an array
                        if output[1] == black: #Change this to the colour of you tilt
                                tempf = float(output[2]) #convert the string for the temperature to a float type
                                gotData = 1
                                tiltTime = datetime.datetime.now()
                                tiltSG = float(output[3])/1000
                                tiltTemp = tempf

#assign values to a dictionary variable for the http POST 
        data=   {
                        'time': tiltTime,
                        'sg': tiltSG,
                        'temp': tiltTemp,
                        'beer_name': beerName,
                        'batch_id': batchId
                        }
        blescan.hci_disable_le_scan(sock)
        return data



        while True:
                data = getdata()
                #tempf = (float(data["Temp"]) #temp in f
                tempc = (float(data["Temp"])-32)*5/9 #convert from string to float and then farenheit to celcius just for the display
                tempc = round(tempc)                    #Round of the value to 2 decimal places
                tempf = tempc*9/5+32
                tiltSG = data['SG']



def main():

        global screen
        updateSecs = delay  #time in seconds between updating the google sheet
        screenSecs = 60

        timestamp = time.time() #Set time for beginning of loop
        updateTime = timestamp + updateSecs #Set the time for the next update to google sheets
        screenTime = timestamp + screenSecs     #Set the time to put the screen to sleep

	while True:
		data = getdata()
                #tempf = (float(data["Temp"]) #temp in f
                tempc = (float(data["temp"])-32)*5/9 #convert from string to float and then farenheit to celcius just for the display
                tempc = round(tempc)                    #Round of the value to 2 decimal places
                tempf = tempc*9/5+32
                tiltSG = data['sg']

		#Post initial data
		#Tilt_Data
                print data
                #print tempf
                r = requests.post('http://beer.jmyers.tech/api/', data)
                
if __name__ == "__main__": #dont run this as a module
        main()

