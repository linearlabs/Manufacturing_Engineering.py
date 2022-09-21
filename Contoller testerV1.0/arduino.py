# Controller Tester V1.0
# Linear Labs Inc
# Doug Gammill
# 3/15/22

import serial # handles TDTI USBserial devices like arduino
from time import sleep # handles delay
import configparser # handles config files

configParser = configparser.RawConfigParser() # config
configFilePath = '//CTGTECH-LLDC01.linearlabs.local/Production/Production Data/Controller Config Files/folderConfig.txt'
configParser.read(configFilePath)
folder = configParser.get('folderPath', 'savePath')
configFolder = configParser.get('folderPath', 'configFolder')
idResponse = configParser.get('folderPath', 'idResponseArduino')
idResponse = idResponse + "\r\n"

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
idQuery = "*idn?\r\n" # query string
idQuery = idQuery.encode()


def isConnected(s): # if there is a controller tester on the USB port
    global idResponse
    #idResponse = 'Controller Tester, V1.0\r\n' # response string
    idResponse = idResponse.encode() # convert to a byte array
    sleep(1)
    s.flushInput() # make sure the input buffer is empty
    s.write(idQuery) # send the ID command
    y = s.readline()  # read responce
    return y == idResponse # if expected reponse = actual response
    
def connect(comPorts): # try to locate
    global idResponse
    for port in comPorts: # try each port in the list                                                 
        s = serial.Serial(port,baudrate=57600,timeout = 1) # open port at 57600
        if isConnected(s):  # if found,
            idResponse = idResponse.decode()
            idResponse = idResponse.strip()
            print('\r\n'+ idResponse + ', found on',s.port)
            return s # return the port
        else:
            s.close() # if it's not a Controller Tester, close port     
    return  False # none found, return False
usb1 = False # device handle

def connectArduino(): # get data from the tester
    global usb1                  
    result = "" # start with a bad result
    if len(result) != 3: # if we don't have a good result
        if not usb1: # check for no port

            print('.',end='',flush=True) # slen(result) == 3:how we are searching
            comPorts = getPorts() # get the list of available ports
            usb1 = connect(comPorts) # connect to a Stat001, if available
            sleep(1) # delay a bit
        try: # attempt to get data
            usb1.flushInput() # get rid of any stale input
            result = usb1.readline() # capture the result
            #break

        except: # we failed
            try:
                usb1.close() # attempt to close the open port
            except:
                pass # catch a miss on close
            usb1 = False # wipe the port handle
            result = "" # wipe the result

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
        
