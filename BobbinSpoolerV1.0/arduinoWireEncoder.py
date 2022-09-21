# Stator Winder/Bobbin Spooler V1.0
# Linear Labs Inc
# Doug Gammill
# 3/15/22

import serial # handles TDTI USBserial devices like arduino
import configTemplate
from time import sleep # handles delay
idResponse = configTemplate.idResponseWireEncoder
passFail=0

def getPorts():
    ports = [] # list of possible ports
    result = [] # list of open ports
    # this is the method for Windows
    for i in range(5,256): # generate a list of ports to try
        ports.append('COM%s' % (i+1)) # eg. COM1, COM2 ...

    for port in ports: # try each port in the list
        try:
            s = serial.Serial(port) # attempt to open the port
            s.close() # close the port
            result.append(port) # save the available port
        except(OSError, serial.SerialException):
            pass # ignore the exception and continue
    return result
idQuery = "*idn?\n" # query string
idQuery = idQuery.encode()

def isConnected(s): # if there is a controller tester on the USB port
    global idResponse
    sleep(2)
    s.flushInput() # make sure the input buffer is empty
    s.write(idQuery) # send the ID command
    y = s.readline()  # read response
    y = y.decode()
    y = y.strip() # strip \n
    return y == idResponse # if expected reponse = actual response
    
def connect(comPorts): # try to locate
    global idResponse, usbPort
    for port in comPorts: # try each port in the list                                                 
        s = serial.Serial(port,baudrate=115200,timeout = .2) # open port at 57600
        if isConnected(s):  # if found
            print('\r\n'+ idResponse + ', found on',s.port)
            usbPort=s.port
            return s # return the port
        else:
            s.close() # if it's not a Controller Tester, close port     
    return  False # none found, return False
usb1 = False # device handle

def checkArduino():
    global idResponse, passFail
    usb1.flushInput() # get rid of any stale input
    usb1.write(idQuery) # request the data
    sleep(1.8)
    result = usb1.readline() # capture the result
    result = result.decode() # convert from bytes to string
    result = result.strip() # strip off \n
    print(result)
    if result == idResponse: # we have something other than blank bytes
        passFail=0
        return passFail
    
def connectArduino(): # get data from the tester
    global usb1,passFail
    result = "" # start with a bad result
    if len(result) != 3: # if we don't have a good result
        if not usb1: # check for no port

            print('.',end='',flush=True) # slen(result) == 3:how we are searching
            comPorts = getPorts() # get the list of available ports
            usb1 = connect(comPorts) # connect if available
            sleep(1) # delay a bit // changed from 1
        try: # attempt to get data
            usb1.flushInput() # get rid of any stale input
            result = usb1.readline() # capture the result
            passFail=0

        except: # we failed
            try:
                passFail=1
                usb1.close() # attempt to close the open port
            except:
                pass # catch a miss on close
            usb1 = False # wipe the port handle
            result = "" # wipe the result
            return passFail

def command(query):
    global result
    i=1
    while i==1:
        dataQuery = query+'\r\n'
        dataQuery = dataQuery.encode() # converted to bytes
        usb1.flushInput() # get rid of any stale input
        usb1.write(dataQuery) # request the data
        sleep(.75)
        result = usb1.readline() # capture the result
        result = result.decode() # convert from bytes to string
        result = result.strip() # strip off \r\n
        print(result)
        if result!='': # we have something other than blank bytes
            i=0
            return result

def readMessage():
    global message, usb1
    i=1
    message = ''
    message = usb1.readline() # capture the result
    if message!='': # we have something other than blank bytes
        message = message.decode() # convert from bytes to string
        message = message.strip() # strip off \r\n
        i=0
        return message
        
