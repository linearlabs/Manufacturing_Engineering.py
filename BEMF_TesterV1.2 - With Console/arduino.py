# Arduino V1.1
# Linear Labs Inc
# Doug Gammill
# 7/29/22

import serial # handles TDTI USBserial devices like arduino
from time import sleep # handles delay
import configparser # handles config files
import configTemplate
idResponseArduino = configTemplate.idResponseArduino

def getPorts():
    global s
    ports = [] # list of possible ports
    result = [] # list of open ports
    # this is the method for Windows
    for i in range(3,256): # generate a list of ports to try
        ports.append('COM%s' % (i+1)) # eg. COM1, COM2 ...

    for port in ports: # try each port in the list
        try:
            s = serial.Serial(port) # attempt to open the port
            s.close() # close the port
            result.append(port) # save the available port
        except(OSError, serial.SerialException):
            pass # ignore the exception and continue
    return result
idQuery = "*idn?\r\n" # query string
idQuery = idQuery.encode()


def checkArduino():
    global idResponseArduino, passFailArduino
    usb1.flushInput() # get rid of any stale input
    usb1.write(idQuery) # request the data
    sleep(1.8)
    result = usb1.readline() # capture the result
    result = result.decode() # convert from bytes to string
    result = result.strip() # strip off \r\n
    print(result)
    if result == idResponseArduino: # we have something other than blank bytes
        passFailArduino=0
        return passFailArduino

def isConnected(s): # if there is a controller tester on the USB port
    global idResponseArduino, passFailArduino
    sleep(1.8) # arduino in Stator Tester takes a little over a second to respond
    s.flushInput() # make sure the input buffer is empty
    s.write(idQuery) # send the ID command
    y = s.readline()  # read responce
    y = y.decode() # decode byte array
    y = y.strip() # strip \r\n
    return y == idResponseArduino # if expected reponse = actual response
    
def connect(comPorts): # try to locate
    global idResponseArduino
    for port in comPorts: # try each port in the list                                                 
        s = serial.Serial(port,baudrate=57600,timeout = 1) # open port at 57600
        if isConnected(s):  # if found,
            print('\r\n'+ idResponseArduino + ', found on',s.port)
            return s # return the port
        else:
            s.close() # if it's not a Controller Tester, close port     
    return  False # none found, return False
usb1 = False # device handle

def connectArduino(): # get data from the tester
    global usb1,passFailArduino
    result = "" # start with a bad result
    if len(result) != 3: # if we don't have a good result
        if not usb1: # check for no port
            print('.',end='',flush=True) # slen(result) == 3:how we are searching
            comPorts = getPorts() # get the list of available ports
            usb1 = connect(comPorts) # connect to a Stat001, if available
        try: # attempt to get data
            usb1.flushInput() # get rid of any stale input
            result = usb1.readline() # capture the result
            passFailArduino=0
        except: # we failed
            try:
                passFailArduino=1 
                usb1.close() # attempt to close the open port
            except:
                pass # catch a miss on close
            usb1 = False # wipe the port handle
            result = "" # wipe the result
            return passFailArduino

    
def command(query):
    global result
    i=1
    while i==1:
        dataQuery = query+'\r\n'
        dataQuery = dataQuery.encode() # converted to bytes
        usb1.flushInput() # get rid of any stale input
        usb1.write(dataQuery) # request the data
        sleep(.5)
        result = usb1.readline() # capture the result
        result = result.decode() # convert from bytes to string
        result = result.strip() # strip off \r\n
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
