# Stator Winder V2.1
# Linear Labs Inc
# Doug Gammill
# 1/3/23

import serial # handles TDTI USBserial devices like arduino
from time import sleep # handles delay
import configparser # handles config files
configParser = configparser.RawConfigParser() # config
configFolder = 'folderConfig.txt'
configParser.read(configFolder)
passFail=0
idResponse = configParser.get('config', 'idResponseArduino')
idResponse = idResponse + "\r\n"
idResponse = idResponse.encode() # convert to a byte array
usbPort = configParser.get('config', 'usbPortArduino')

def connectArduino():
    global usb1, passFail
    idQuery = "*idn?\r\n" # query string
    idQuery = idQuery.encode()
    print(usbPort)
    try:
        usb1 = serial.Serial(usbPort,baudrate=115200,timeout = .2)
        sleep(1)
        usb1.flushInput() # make sure the input buffer is empty
        usb1.write(idQuery) # send the ID command
        y = usb1.readline()  # read responce
        y = y.decode()
        print(y)
    except:
        passFail=1

def command(query):
    global message, usb1
    i=1
    while i==1:
        dataQuery = query+'\r\n'
        dataQuery = dataQuery.encode() # converted to bytes
        usb1.flushInput() # get rid of any stale input
        usb1.write(dataQuery) # request the data
        sleep(1)
        message = usb1.readline() # capture the result
        #message = message.decode() # convert from bytes to string
        message = message.strip() # strip off \r\n
        if message!='': # we have something other than blank bytes
            i=0
            return message

def readMessage():
    global message, usb1
    message = ''
    message = usb1.readline() # capture the result
    if message!='': # we have something other than blank bytes
        sleep(.2)
        message = message.decode() # convert from bytes to string
        message = message.strip() # strip off \r\n
        i=0
        return message
        
