'''
Stator Test Fixture V2.3

Functions:
    Retrieve a list of COM ports
    Identify which is connected to the MCR-5100, GPT-9803 and Stator tester
    Read and return the inductance and resistance values
    Read and return hi pot values
    Conduct a magnetic flux test of stators
    This version can handle live discovery, connects and disconnects
    This version has data bounding and documentation
    Heavy modifications from Doug (9/9/2021)


Author: Doug Gammill, Noel Henson
Date:   9/10/2021
Copyright (c) 2021
Linear Labs, Inc.
'''

from tkinter import filedialog
from tkinter import * # handles GUI
import tkinter as tk # handles GUI
import subprocess as sub
from threading import * # handles threading so GUI doesnt freeze during main functions
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk # handles GUI Image
import openpyxl
import pandas as pd # library for handling data inputted into csv file
from pandas import ExcelWriter # used with saving spread sheets with sheet numbers
import serial # library for serial communication (pyserial)
import numpy as np # library for numerical/matrix manipulation
from time import sleep # used for pausing program for set time
import time # used for adding time stamps
import serial.tools.list_ports # used to get full list of available COM ports
from serial.serialutil import SerialException # used for exception handling
import pathlib # for determining if path/file exists
import os # for working with file paths
from pathlib import Path # for working with file paths
import configparser
index=0
comOK=0
configParser = configparser.RawConfigParser()

configParser.read('folderConfig.txt')
folder = configParser.get('folderPath', 'savePath')
configFolder = configParser.get('folderPath', 'configPath')
idResponseLCR = configParser.get('folderPath', 'idResponseLCR')
idResponseHpot = configParser.get('folderPath', 'idResponseHpot')
idResponseStat = configParser.get('folderPath', 'idResponseStat')
usbPassFail1 = 0 # 0 = not fail LCR
usbPassFail2 = 0 # 0 = not fail GPT
usbPassFail3 = 0 # 0 = not fail Arduino stator tester

#### Stator Variables, update these with every new stator ####
# returns number of magnets, number of steps in the y-direction, and starting/initial pole, (cont.)
# and alot of other settings for hi pot and LCR testing
def getPartParams(partNum, sn):                 # breaks down part number to determine variables needed
    global magNum,yAxis,aPol,cPol,initPole,biidNum,mcrFreq,resMin,resMax,indMin,indMax,mode,gptV,gptI,gptImin,gptFreq,folder,failStatus1,failStatus2,index,poleStrengthMinimum,pOff,sOff
    
    try:

        configFile = partNum
        configParser = configparser.RawConfigParser()   
        configFilePath = configFolder+'/'+configFile+'.txt'
        print(configFilePath)
        
        if Path(configFilePath).is_file():
            configParser.read(configFilePath)
            poleStrengthMinimum = configParser.get(configFile, 'poleStrengthMinimum')
            print ('poleStrengthMinimum='+poleStrengthMinimum)
            magNum = configParser.get(configFile, 'magNum')
            print ('magNum='+magNum)
            yAxis = configParser.get(configFile, 'yAxis')
            print ('yAxis='+yAxis)
            aPol = configParser.get(configFile, 'aPol')
            print ('aPol='+aPol)
            cPol = configParser.get(configFile, 'cPol')
            print ('cPol='+cPol)
            initPole = configParser.get(configFile, 'initPole')
            print ('initPole='+initPole)
            biidNum = configParser.get(configFile, 'biidNum')
            print ('biidNum='+biidNum)
            mcrFreq = configParser.get(configFile, 'mcrFreq')
            print ('mcrFreq='+mcrFreq)
            resMin = configParser.get(configFile, 'resMin')
            print ('resMin='+resMin)
            resMax = configParser.get(configFile, 'resMax')
            print ('resMax='+resMax)
            indMin = configParser.get(configFile, 'indMin')
            print ('indMin='+indMin)
            indMax = configParser.get(configFile, 'indMax')
            print ('indMax='+indMax)
            mode = configParser.get(configFile, 'mode')
            print ('mode='+mode)
            gptV = configParser.get(configFile, 'gptV')
            print ('mode='+gptV)
            gptI = configParser.get(configFile, 'gptI')
            print ('gptI='+gptI)
            gptImin = configParser.get(configFile, 'gptImin')
            print ('gptImin='+gptImin)
            gptFreq = configParser.get(configFile, 'gptFreq')
            print ('gptFreq='+gptFreq)
            pOff = configParser.get(configFile, 'pOff')
            print ('pOff='+pOff)
            sOff = configParser.get(configFile, 'sOff')
            print ('sOff='+sOff)
        
        else:
            raise NameError
            
        if int(yAxis) >= 7500: # y axis soft limit
            raise ValueError
    except NameError: # print error message and return default values
        print('ERROR: Invalid partNumber! Returning default values.')
        comstat= 'ERROR: Invalid partNum!'
        label.config(fg="black",bg='red',text=comstat)
        failStatus1=comstat
        failStatus2='Verify Configuration, Reset and try again'
        index=0
        failure()

    except ValueError: # print error message and return default values #####fix new error for magNum != (aPol + cPol)(4)
        print('ERROR: Out of bounds, check yAxis!')
        comstat= 'Yaxis Out of Bounds'
        label.config(fg="black",bg='red',text=comstat)
        failStatus1=comstat
        failStatus2='Y axis in config set too high, needs to be below 7500'
        index=0
        failure()

    return magNum,yAxis,aPol,cPol,initPole,biidNum,mcrFreq,resMin,resMax,indMin,indMax,mode,gptV,gptI,gptImin,gptFreq

#ComPort Function ###########################################
def getPorts():
    ports = []                                                      # list of possible ports
    result = []                                                     # list of open ports
    # this is the method for Windows
    for i in range(5,256):                                          # generate a list of ports to try
        ports.append('COM%s' % (i+1))                               # eg. COM1, COM2 ...

    for port in ports:                                              # try each port in the list
        try:
            s = serial.Serial(port)                                 # attempt to open the port
            s.close()                                               # close the port
            result.append(port)                                     # save the available port
        except(OSError, serial.SerialException):
            pass # ignore the exception and continue
    return result
idQuery = "*idn?\r\n" # query string
idQuery = idQuery.encode()                                           


#MCR-5100 Functions ###########################################
def isMCR5100(s):# if it's an MCR-5100 on the line
    global idResponseLCR
    s.flushInput() # make sure the input buffer is empty
    s.write(idQuery) # send the ID command
    x = s.readline() # read the response
    x = x.decode() 
    x = x.strip()
    #print(idResponseLCR)
    #print(x)
    return x == idResponseLCR

def connectMCR5100(comPorts): # try to locate an MCR-5100
    global usbPassFail1, comstat1
    for port in comPorts: # try each port in the list
                                                                    
        comstat='Searching'
        label1.config(fg="black",bg='white',text=comstat)
        s = serial.Serial(port,baudrate=115200,timeout = 1) # open port at 115200
        if isMCR5100(s): # if found,
            print('\r\nMCR-5100 found on port ',s.port)
            comstat1=str(s.port)
            label1.config(fg="black",bg='#3399ff',text=comstat1)
            usbPassFail1=0
            return s # return the port
        else:
            s.close() # it's not an MCR-5100, close port
    return False # none found, return False
mcr = False # device handle

def connectLCR(): # get data from the tester
    global mcr, usbPassFail1
    result = "" # start with a bad result
    if len(result) != 3: # if we don't have a good result
        if not mcr: # check for no port

            print('.',end='',flush=True) # slen(result) == 3:how we are searching
            comPorts = getPorts() # get the list of available ports
            mcr = connectMCR5100(comPorts) # connect to a LCR, if available
            #sleep(1) # delay a bit
        try: # attempt to get data
            mcr.flushInput() # get rid of any stale input
            result = mcr.readline() # capture the result
            #break

        except: # we failed
            try:
                usbPassFail1=1
                mcr.close() # attempt to close the open port
            except:
                pass # catch a miss on close
            mcr = False # wipe the port handle
            result = "" # wipe the result
            return usbPassFail1

def bound(v,vmin,vmax): # put limits on v
    return min(max(v,vmin),vmax)                                    # Force: vmin <= v <= vmax

def mcrComm(query):             
    global L,R
    #numberFormat = '{:7.3f}'                                       # field lenth: 7, decimal places: 3, fixed-point
    dataQuery = query+'\r\n'
    dataQuery = dataQuery.encode()                                  # converted to bytes
    mcr.flushInput()                                                # get rid of any stale input
    mcr.write(dataQuery)                                            # request the data
    #sleep(.5)
    result = mcr.readline()                                         # capture the result
    if result:                                                      # we have something
        result = result.decode()                                    # convert from bytes to string
        result = result.strip()                                     # strip off \r\n
        result = result.split(',')                                  # split into two strings
        l=len(result)
        if (l == 3) or (l == 2):                                    # must have 2 or 3 fields
            L = float(result[0])                                    # the first value is inductance
            R = float(result[1])                                    # the second value is resistance
            L = L*1000                                              # convert to mH
            R = R*1000                                              # convert to mOhm
            L = bound(L,0,10000)                                    # limit inductance values
            R = bound(R,0,10000)                                    # limit resistance values
            #L = print("L = ",numberFormat.format(L),"mH")          # inductance first
            #R = print("R = ",numberFormat.format(R),"mOhm")        # resistance next
            return L,R                                              # return the value pair

def mcrComms(query):
    global resultMCR
    dataQuery = query+'\r\n'
    dataQuery = dataQuery.encode()                                  # converted to bytes
    mcr.flushInput()                                                # get rid of any stale input
    mcr.write(dataQuery)                                            # request the data
    sleep(.5)
    resultMCR = mcr.readline()                                      # capture the result
    if resultMCR:                                                   # we have something
        resultMCR = resultMCR.decode()                              # convert from bytes to string
        resultMCR = resultMCR.strip()                               # strip off \r\n
        resultMCR = int(resultMCR)      
        return resultMCR
    
def readMCR():                                                      #send command to GPT-9803 to check errors
    return mcrComm(':fetch?')                                       #serial text to send

def readMCRf():                                                     #send command to GPT-9803 to check errors
    return mcrComms('freq?')                                        #serial text to send

def writeMCRf(f):                                                   #send command to GPT-9803 to check errors
    f = ' ' + f                                                     #add a space before f
    return mcrComms('freq' + f)                                     #enter: writeMCRf("100") for 100Hz

#get LCR reading
def appendSensorReadingsMCR(L, R, row):

    row.append
    row.append(status)
    row.append(L)                                                   # (2.5V/512)*readingADC/100mV=mT (this works for hall sensor PN DRV5055A1)
    row.append('mH')
    row.append(R)                                                   # append values to row
    row.append('mΩ')

def checkMCR():
    global index, failStatus1, failStatus2
    numberFormat = "{0:.3f}"                                        # field lenth: 7, decimal places: 3, fixed-point
    if (R<=float(resMin)):                                                 # checks to make sure resistance isnt too LOW
        print('\nFailed, ',status,':',numberFormat.format(R),'mΩ is too LOW')
        print('\nResistance should be in-between', resMin,'mΩ and ', resMax, 'mΩ\n')
        
        failStatus1='Failed, '+str(status)+': '+str(numberFormat.format(R))+'mΩ is too LOW'
        failStatus2='Resistance should be in-between '+ resMin+'mΩ and '+ resMax+ 'mΩ'
        
        comstat= 'Failed, Resistance too Low'
        label.config(fg="black",bg='red',text=comstat)
        failure()
        
        return False
    elif(R>=float(resMax)):                                                # checks to make sure resistance isnt too HIGH
        print('\nFailed, ',status,':',numberFormat.format(R),'mΩ is too HIGH')
        print('\nResistance should be in-between', resMin,'mΩ and ', resMax, 'mΩ\n')

        failStatus1='Failed, '+str(status)+': '+str(numberFormat.format(R))+'mΩ is too HIGH'
        failStatus2='Resistance should be in-between '+ resMin+'mΩ and '+ resMax+ 'mΩ'
        
        comstat= 'Failed, Resistance too High'
        label.config(fg="black",bg='red',text=comstat)
        failure()
        
        return False
    elif (L<=float(indMin)):                                               # checks to make sure inductance isnt too LOW
        print('\nFailed, ',status,':',numberFormat.format(L),'mH is too LOW')
        print('\nInductance should be in-between', indMin,'mH and ', indMax, 'mH\n')

        failStatus1='Failed, '+str(status)+': '+str(numberFormat.format(L))+'mH is too LOW'
        failStatus2='Inductance should be in-between '+ indMin+'mH and '+ indMax+ 'mH'
        
        comstat= 'Failed, Inductance is too Low'
        label.config(fg="black",bg='red',text=comstat) 
        failure()
        
        return False
    elif (L>=float(indMax)):                                               # checks to make sure inductance isnt too HIGH
        print('\nFailed, ',status,':',numberFormat.format(L),'mH is too HIGH')
        print('\nInductance should be in-between', indMin,'mH and ', indMax, 'mH\n')

        failStatus1='Failed, '+str(status)+': '+str(numberFormat.format(L))+'mH is too HIGH'
        failStatus2='Inductance should be in-between '+ indMin+'mH and '+ indMax+ 'mH'
        
        comstat= 'Failed, Inductance is too High'
        label.config(fg="black",bg='red',text=comstat)
        failure()
        
        return False
    return True
    
def testMCR():
    global dfMCR, index
    table = []                                                      # start table
    index = 1                                                       # index counts up every mcr phase to phase test 1-3, when it = 4 Hpot will know its safe to try a test
    ablrON()                                                        # will only turn on if hpot and flux relays are in the off position
    label4.config(fg="black",bg="white",text='Relays On')
    if (status == 'A-B LCR') and (value == 1):                      # checks arduino reply and makes sure correct relays are on
        sleep(1)                                                    # havn't tested minimum wait time, just waiting to make sure arduino relays have waited long enough
        readMCR()                                                   # query MCR L and R values
        ablrOFF()                                                   # A to B phase relays off
        label4.config(fg="black",bg="white",text='Relays Off')
        sleep(1)                                                    # sleep to wait on relays to settle
        if not checkMCR():                                          # check minimum and maximum set values for L and R, if bad, terminate program
            return False, False
        row = []                                                    # (value == 1) is on and (value == 0) is off
        appendSensorReadingsMCR(L, R, row)                          # expected pole is opposite of next while loop
        row.append('Pass')                                          # pass is writen in spread sheet, checkMCR() will kill program if it sees a failure
        table.append(row) 
        label4.config(fg="black",bg='#3399ff',text="PASS")
    if (status == 'A-B LCR') and (value == 0):                      # status is which phase to phase LCR test and value is if its on or off (1 or 0)
        aclrON()                                                    # if statments checking for on or off values are meant to add a layer of protection for the LCR meter
        label5.config(fg="black",bg="white",text='Relays On')
    if (status == 'A-C LCR') and (value == 1):                      # status is which phase to phase LCR test and value is if its on or off (1 or 0)
        sleep(1)                                                    # sleep to wait on relays to settle
        readMCR()                                                   # query MCR L and R values
        aclrOFF()                                                   # A to C relays OFF
        label5.config(fg="black",bg="white",text='Relays Off')
        sleep(1)                                                    # sleep to wait on relays to settle
        index = index + 1                                           # index counts up every mcr phase to phase test 1-3, when it = 4 Hpot will know its safe to try a test
        if not checkMCR():                                          # check minimum and maximum set values for L and R, if bad, terminate program
            return False, False
        row = []                                                    # new row in spread sheet
        appendSensorReadingsMCR(L, R, row)                          # expected pole is opposite of next while loop
        row.append('Pass')                                          # pass is writen in spread sheet, checkMCR() will kill program if it sees a failure
        table.append(row)
        label5.config(fg="black",bg='#3399ff',text="PASS")
    if (status == 'A-C LCR') and (value == 0):                      # status is which phase to phase LCR test and value is if its on or off (1 or 0)
        bclrON()
        label6.config(fg="black",bg="white",text='Relays On')
    if (status == 'B-C LCR') and (value == 1):                      # status is which phase to phase LCR test and value is if its on or off (1 or 0)
        sleep(1)                                                    # sleep to wait on relays to settle
        readMCR()                                                   # query MCR L and R values                                           
        bclrOFF()                                                   # B to C Phase LRC relays OFF
        label6.config(fg="black",bg="white",text='Relays Off')
        sleep(1)                                                    # sleep to wait on relays to settle
        index = index + 1                                           # index counts up every mcr phase to phase test 1-3, when it = 4 Hpot will know its safe to try a test
        if not checkMCR():                                          # check minimum and maximum set values for L and R, if bad, terminate program
            return False, False                                     # check minimum and maximum set values for L and R, if bad, terminate program
        row = []                                                    # new row in spread sheet
        appendSensorReadingsMCR(L, R, row)                          # expected pole is opposite of next while loop
        row.append('Pass')                                          # pass is writen in spread sheet, checkMCR() will kill program if it sees a failure
        table.append(row)
        label6.config(fg="black",bg='#3399ff',text="PASS")
        cols = ['Status', 'Inductance', 'mH', 'Resistance', 'mΩ', 'P/F']
        dfMCR = pd.DataFrame(table, columns=cols)                   # place table into a pandas Dataframe object
        print(dfMCR)
        index = index + 1                                           # index counts up every mcr phase to phase test 1-3, when it = 4 Hpot will know its safe to try a test
        return

            
#GPT-9803 Functions ###########################################
            
def isGPT9803(s): # if it's a GPT-9803 on the line
    global idResponseHpot

    s.flushInput() # make sure the input buffer is empty
    s.write(idQuery) # send the ID command
    z = s.readline() # read the response
    z = z.decode() # decode byte array
    z = z.strip() # strip \r\n
    #print(idResponseHpot)
    #print(z)
    return z == idResponseHpot

def connectGPT9803(comPorts): # try to locate an GPT-9803
    global usbPassFail2, comstat2
    for port in comPorts: # try each port in the list
        comstat='Searching'
        label2.config(fg="black",bg='white',text=comstat)                                              
        s = serial.Serial(port,baudrate=115200,timeout = 1) # open port at 115200
        if isGPT9803(s): # if found,
            print('\r\nGPT-9803 found on port ',s.port)
            comstat2=str(s.port)
            label2.config(fg="black",bg='#3399ff',text=comstat2)
            usbPassFail2=0
            return s # return the port
        else:
            s.close() # it's not an GPT-9803, close port
    return False # none found, return False

gpt = False # device handle

def connectGPT(): # get data from the tester
    global gpt, usbPassFail2
    result = "" # start with a bad result
    if len(result) != 3: # if we don't have a good result
        if not gpt: # check for no port
            print('.',end='',flush=True) # slen(result) == 3:how we are searching
            comPorts = getPorts() # get the list of available ports
            gpt = connectGPT9803(comPorts) # connect to a LCR, if available
            sleep(1) # delay a bit
        try: # attempt to get data
            gpt.flushInput() # get rid of any stale input
            result = gpt.readline() # capture the result
            #break

        except: # we failed
            try:
                usbPassFail2=1
                gpt.close() # attempt to close the open port
            except:
                pass # catch a miss on close
            gpt = False # wipe the port handle
            result = "" # wipe the result
            return usbPassFail2

def gptComms(query):
    global statusGPT, V, I
    dataQuery = query+'\r\n'
    dataQuery = dataQuery.encode()                                  # converted to bytes
    gpt.flushInput()                                                # get rid of any stale input
    gpt.write(dataQuery)                                            # request the data
    #sleep(.5)
    result = gpt.readline()                                         # capture the result
    if result:                                                      # we have something
        result = result.decode()                                    # convert from bytes to string
        result = result.strip()                                     # strip off \r\n
        result = result.split(',')                                  # split into two strings
        statusGPT = str(result[1])                                  # get status (first element of list)
        V = str(result[2])                                          # voltage response from Hi Pot tester
        I = str(result[3])                                          # leakage response from Hi Pot tester
        return

def gptComms1(query):
    global resultGPT
    dataQuery = query+'\r\n'
    dataQuery = dataQuery.encode()                                  # converted to bytes
    gpt.flushInput()                                                # get rid of any stale input
    gpt.write(dataQuery)                                            # request the data
    #sleep(.2)
    resultGPT = gpt.readline()                                      # capture the result
    if resultGPT:                                                   # we have something
        resultGPT = resultGPT.decode()                              # convert from bytes to string
        resultGPT = resultGPT.strip()                               # strip off \r\n
        return resultGPT

def gptTestON():
    return gptComms('func:test on')                                 # send command to hi pot to run test

def gptTestMEAS():
    return gptComms('meas?')                                        # send command to hi pot to meas last test

def hiPotMode(mode):                                                # send command to GPT-9803 to change mode (acw, dcw)
    return gptComms1('manu:edit:mode' +mode)                        # enter: 'ACW', 'DCW', 'IR', or 'GB' (acw is the only current supported mode)

def hiPotModeInq():                                                 # send command to GPT-9803 to query mode setting
    return gptComms1('manu:edit:mode?')                             
    
def dcwVolt(V):                                                     # send command to GPT-9803 to change DCW voltage
    return gptComms1('manu:dcw:volt' +V)                            # enter: dcwVolt(".2") for .2kV

def dcwAmp(A):                                                      # send command to GPT-9803 to change DCW hi set current  
    return gptComms1('manu:dcw:chis ' +A)                           # enter: dcwAmp("10") for 10mA

def dcwAmpInq():                                                    # send command to GPT-9803 to query DCW hi set current
    return gptComms1('manu:dcw:chis?')                              

def dcwVoltInq():                                                   # send command to GPT-9803 to query DCW voltage
    return gptComms1('manu:dcw:volt?')                              

def acwAmpInq():                                                    # send command to GPT-9803 to query ACW hi set current
    return gptComms1('manu:acw:chis?')                              

def acwVoltInq():                                                   # send command to GPT-9803 to query ACW voltage
    return gptComms1('manu:acw:volt?')                              

def acwVolt(V):                                                     # send command to GPT-9803 to change ACW voltage .25kV max                                                  # add a space before A    
    return gptComms1('manu:acw:volt ' +V)                            # enter: acwVOLT(".25") for 0.25kV

def acwAmp(A):                                                      # send command to GPT-9803 to change ACW hi set current .001 - 42mA range
    return gptComms1('manu:acw:chis ' +A)                           # enter: acwAmp("10") for 10mA (needs a space between command and value)

def acwAmplow(lowA):                                                # send command to GPT-9803 to change ACW LOW set current   
    return gptComms1('manu:acw:clos ' +lowA)                        # enter: acwAmplow("1") for 1mA (0 - 41.9mA range but always has to be lower than hi set) 

def acwAmplowInq():                                                 # send command to GPT-9803 to query ACW LOW set current
    return gptComms1('manu:acw:clos?')                              

def acwFreqInq():                                                   # send command to GPT-9803 to query ACW frequency
    return gptComms1('manu:acw:freq?')                              

def acwFreq(f):                                                     # send command to GPT-9803 to change ACW Frequency  
    return gptComms1('manu:acw:freq' +f)                            # enter: acwFreq("60") for 60Hz. 50 and 60 are only options
    
def systErr():                                                      # send command to GPT-9803 to check errors
    return gptComms1('syst:err?')                                   # serial text to send

def clrErr():                                                       # send command to GPT-9803 to clr registers and system errors
    return gptComms1('*cls')                                        # serial text to send


def appendSensorReadingsGPT(V, I, row):
    row.append(V)                                                   # appending rows of GPT to spreadsheet
    row.append(I)                                                   # append values to row
    row.append(statusGPT)

def setUpGPT():
    global index, failStatus1, failStatus2

    
    if mode == 'acw' or 'ACW':
        hiPotMode(mode)                                             # send mode (acw, dcw) acw is the only working mode right now
        hiPotModeInq()                                              # mode query
    if resultGPT == 'ACW':                                          # if recieved == send                             
        acwFreq(gptFreq)                                            # tells gpt to change frequency (50 or 60 Hz)
        acwFreqInq()                                                # query frequency
        x= gptFreq + ' Hz'                                          # changes sending parameter to look like recieved parameter for ERROR CHECKING
        print('Hpot freq = '+resultGPT)                             # print recived frequncy
        comStat='Freq='+resultGPT
        label7.config(fg="black",bg='white',text=comStat)
    if resultGPT == x:                                              # if recieve == send (ERROR CHECK)
        acwVolt(gptV)                                               # send V param change
        acwVoltInq()                                                # query voltage
        x = resultGPT                                               # get ready to change sent and recieved string into floats to compare for errors
        print('Hpot volt = '+x)                                     # print recieved data
        comStat='Voltage='+resultGPT
        label7.config(fg="black",bg='white',text=comStat)
        x = resultGPT.strip('kV')                                   # convert both send and recieve to floats for comparison
        x=float(x)                                                  # convert recieved stripped data to float        
        y=float(gptV)                                               # convert parameter string to float
    if x == y:                                                      # if recieve == send (ERROR CHECK)
        acwAmp(gptI)                                                #
        acwAmpInq()
        x=resultGPT
        print('Hpot hiset = '+x)
        comStat='Hiset='+resultGPT
        label7.config(fg="black",bg='white',text=comStat)
        x=resultGPT.strip('mA')
        x=float(x)
        y = float(gptI)
    if x == y:
        acwAmplow(gptImin)
        acwAmplowInq()
        x=resultGPT
        print('Hpot lowset = '+x)
        comStat='Lowset='+resultGPT
        label7.config(fg="black",bg='white',text=comStat)
        x=resultGPT.strip('mA')
        x=float(x)
        y = float(gptImin)
    if x == y:
        return
    else:
        print('\nHi Pot Parameter Error\n')
        comstat= 'Parameter Error'
        label.config(fg="black",bg='red',text=comstat)
        failStatus1= 'HiPot: Parameter Error'
        failStatus2= 'Check configuration and try again.'
        failure()
        
        return False
         

def testGPT():                                                          # combines func test and reading results of func test
    global dfGPT, index, statusGPT, V, I, failStatus1, failStatus2
    
    if (index == 4):
        setUpGPT()
        if (index == 4):
            table = []
            hpotON()
            label7.config(fg="black",bg='white',text='Relays On')
            gptTestON()                                                     # runs "func:test on" in GPT-9803
            sleep(2.2)                                                      # func:test on takes a little over 2 sec to complete
            gptTestMEAS()                                                   # read results of "func:test on" in GPT-9803
            hpotOFF()
            label7.config(fg="black",bg='white',text='Relays Off')
##    if (index !=4):
##        print('Error.')                                      #index helps make sure correct relays are on for hi pot test
##        comstat= 'Index Error'
##        label.config(fg="black",bg='red',text=comstat)
##        failStatus1= 'HiPot Index Error'
##        failStatus2= 'Something might be trying to operate out of safe order.'
##        failure()
##        return False
    
    if (statusGPT == 'PASS '):
        row = []                                                        # initialize row of data to append
        row.append(status)                                              # append index
        appendSensorReadingsGPT(V, I, row)                              # expected pole is opposite of next while loop
        table.append(row)
        cols = ['Status', 'Voltage', 'Amperage', 'P/F']
        dfGPT = pd.DataFrame(table, columns=cols)                       # place table into a pandas Dataframe object
        index=5
        label7.config(fg="black",bg='#3399ff',text="PASS")
        print(dfGPT)
        return
    if (statusGPT == 'ERROR'):
        print('HiPot ERROR, possible short to ground', V, I)
        comstat= 'Short'
        label.config(fg="black",bg='red',text=comstat)
        failStatus1= 'HiPot Error: Short to ground, '+str(V)+', '+str(I)
        failStatus2= 'A direct short to ground is detected.'
        failure()
        return False
    if (statusGPT == 'FAIL '):
        print('\nHiPot Failure, ', V, I, ' high leakage current')
        comstat= 'Failure'
        label.config(fg="black",bg='red',text=comstat)
        failStatus1= 'HiPot Failure: High leakage measured- '+str(V)+', '+str(I)
        failStatus2= 'Parameters: Mode='+mode+' Voltage='+gptV+'kV Hiset='+gptI+'mA Lowset='+gptImin+'mA Frequency='+gptFreq+'Hz'
        failure()
        return False    
    
#Stator Tester Functions ###########################################
def isStat001(s): # if it's a stat001 on the line
    global idResponseStat
    sleep(1.8) # arduino in Stator Tester takes a little over a second to respond
    s.flushInput() # make sure the input buffer is empty
    s.write(idQuery) # send the ID command
    y = s.readline() # read stator tester responce
    y = y.decode() # decode byte array
    y = y.strip() # strip \r\n
    #sleep(1.8) use if Arduino is failing to connect
    #print(idResponseStat)
    #print(y)
    return y == idResponseStat #if expected reponse = actual responce then connect Stat Com port
    
def connectStat001(comPorts): # try to locate a Stat001
    global comOK, usbPassFail3,comstat3
    for port in comPorts: # try each port in the list
        comstat= 'Searching'
        label3.config(fg="black",bg='white',text=comstat)                                                
        s = serial.Serial(port,baudrate=115200,timeout = 2) # open port at 115200
        if isStat001(s): # if found,
            print('\r\nTester found on port ',s.port)
            comstat3= str(s.port)
            label3.config(fg="black",bg='#3399ff',text=comstat3)
            usbPassFail3=0
            barcode_var.set('')
            return s # return the port
        else:
            s.close() # it's not an MCR-5100, close port     
    return  False # none found, return False
sta = False # device handle

def connectTester(): # get data from the tester
    global sta, usbPassFail3
    result = "" # start with a bad result
    if len(result) != 3: # if we don't have a good result
        if not sta: # check for no port
            print('.',end='',flush=True) # slen(result) == 3:how we are searching
            comPorts = getPorts() # get the list of available ports
            sta = connectStat001(comPorts) # connect to a LCR, if available
            #sleep(1) # delay a bit
        try: # attempt to get data
            sta.flushInput() # get rid of any stale input
            result = sta.readline() # capture the result
            #break

        except: # we failed
            try:
                usbPassFail3=1
                sta.close() # attempt to close the open port
            except:
                pass # catch a miss on close
            sta = False # wipe the port handle
            result = "" # wipe the result
            return usbPassFail3

def staComms(query):                                                #used to parse biid data
    global value, status, failStatus1, failStatus2
    
    dataQuery = query+'\r\n'
    dataQuery = dataQuery.encode()                                  # converted to bytes
    sta.flushInput()                                                # get rid of any stale input
    sta.write(dataQuery)                                            # request the data
    sleep(.5)
    result = sta.readline()                                         # capture the result
    result = result.decode()                                        # convert from bytes to string
    result = result.strip()                                         # strip off \r\n
    result = result.split(',')
    status = result[0]                                              # the first value is inductance

    if status == 'homingY':                                         # next few if statements needed to fix a string to int bug
        failStatus1 = 'Failed HomingY'
        failStatus2 = 'Driver Y circuit protection trip or loose wire, try reboot and reset'
        label4.config(fg="black",bg="red",text=failStatus1)
        print('\r\n'+status+'\r\n')                                 # if arduino detects a failure data is handle as a string
        failure()
        return False
    elif status == 'failedHomingY':                                 # this could be a failure at the begining of a test these comands handle that situation
        failStatus1 = 'Failed HomingY'
        failStatus2 = 'Y driver circuit protection trip or loose wire, try reboot and reset'
        label4.config(fg="black",bg="red",text=failStatus1)
        print('\r\n'+status+'\r\n')                                 # if arduino detects a failure data is handle as a string
        failure()
        return False
    elif status == 'failedHomingX':                                 # homing Y fails more often but this is here to handle X if it fails
        failStatus1 = 'Failed HomingX'
        failStatus2 = 'X driver circuit protection trip or loose wire, try reboot and reset'
        label4.config(fg="black",bg="red",text=failStatus1)
        print('\r\n'+status+'\r\n')                                 # if arduino detects a failure data is handle as a string
        failure()                                                   # if arduino detects a failure data is handle as a string
        return False
    else:
        value = int(result[1])                                      # if no failures are detected, data from stator arduino can be handled as int variables
        return
    

def hall():                                                         #fetch a sample from hall sensor
    return staComms('hall:')                                        #serial text to send

def ablrON():                                                       #turn on A-B LRC relays
    return staComms('ablr:1')                                       #serial text to send

def ablrOFF():                                                      #turn off A-B LRC relays
    return staComms('ablr:0')                                       #serial text to send

def aclrON():                                                       #turn on A-C LRC relays
    return staComms('aclr:1')                                       #serial text to send

def aclrOFF():                                                      #turn off A-C LRC relays
    return staComms('aclr:0')                                       #serial text to send

def bclrON():                                                       #turn on B-C LRC relays
    return staComms('bclr:1')                                       #serial text to send

def bclrOFF():                                                      #turn off B-C LRC relays
    return staComms('bclr:0')                                       #serial text to send

def hpotON():                                                       #turn on hi pot relays
    return staComms('hpot:1')                                      #serial text to send

def hpotOFF():
    return staComms('hpot:0')                                      #serial text to send

def biid():                                                         #fetch back iron ID
    return staComms('biid:')                                        #serial text to send

def magNumSend(magNum):                                             #total magnet/Pole number
    return staComms('mnum:' +magNum)                           #enter magNum("48") for 48 stator poles

def yAxisSend(yAxis):                                               #Y axis stepper motor
    return staComms('yaxi:' +yAxis)                            #enter yAxis("4300") for 4300 stepper steps

def aPolSend(aPol):                                                 #number of a to b poles Ex. AabB would be 4
    return staComms('apol:' +aPol)                             #enter aPole("4") for 4 a to b poles

def cPolSend(cPol):                                                 #number of c poles Ex. cC would be 2
    return staComms('cpol:' +cPol)                             #enter cPole("2") for 2 c poles

def pOffSend(pOff):                                                 #pole number offset
    return staComms('poff:' +pOff)                            

def sOffSend(sOff):                                                #step number offset
    return staComms('soff:' +sOff)                             


def fluxTest():                                                     #B2 params
    global index, failStatus1, failStatus2

    if index==5: 
        biid()                                                          #start test by checking back iron id
        if value >= 98:                                                 #if back iron result is greater than or equal to 98 then no back iron is detected
            print('\r\nBack iron is missing or not seated correctly.\r\n')
            label8.config(fg="black",bg='red',text="BackIron missing.")
            failStatus1= "Back Iron is missing or isn't seated correctly"
            failStatus2= "Check Back Iron is installed and seated tight."
            failure()
            return False
        if value==int(biidNum) or value==int(biidNum)+1 or value==int(biidNum)-1:                                                #if biid: responce from arduino is is within range of 48 to 50 then continue on!
            magNumSend(magNum)
            comstat = 'Flux: poles='+ magNum
            label8.config(fg="black",bg='white',text=comstat)
        else:                                                           #else print wrong back iron installed and exit flux test.
            print('\r\nWrong back iron installed.\r\n')
            label8.config(fg="black",bg='red',text="Wrong BackIron")
            failStatus1= "Wrong Back Iron Installed"
            failStatus2= "Replace Back Iron with the correct one."
            failure()
            return False
        if value == int(magNum):                                             #if arduino responded magnet number continue on!
            yAxisSend(yAxis)
            comstat = 'Yaxis='+ str(yAxis)
            label8.config(fg="black",bg='white',text=comstat)
        if value == int(yAxis):                                              #if arduino responded Y steps continue on!                            
            aPolSend(aPol)
            comstat = 'aPol='+ aPol
            label8.config(fg="black",bg='white',text=comstat)
        if value == int(aPol):                                               #if arduino responded apol number continue on!
            cPolSend(cPol)
            comstat = 'cPol='+ cPol
            label8.config(fg="black",bg='white',text=comstat)
        if value == int(cPol):                                               #if arduino responded cpol number continue on!
            pOffSend(pOff)
            comstat = 'pOffset='+ pOff
            label8.config(fg="black",bg='white',text=comstat)
        if value == int(pOff):                                               #if arduino responded pOff number continue on!
            sOffSend(sOff)
            comstat = 'sOffset='+ sOff
            label8.config(fg="black",bg='white',text=comstat)
        if value == int(sOff):                                               #if arduino responded sOff number continue on!
            index=6
            return
    else:
        print('\r\nWrong back iron installed.\r\n')
        label8.config(fg="black",bg='red',text="Config Fault")
        failStatus1= "Stator tester returned incorrect configuration value."
        failStatus2= "Check configuration and try again."
        failure()
        return False


# sets pole direction based on sensor value
def getPole(HSRawVal):                                              # HS Raw val is ADC value (hall sensor)
    if HSRawVal > 4:                                                # if raw value greater than 4, magnet is South pole
        return 'S'
    if HSRawVal < -4:                                               # if raw value greater than 4, magnet is South pole
        return 'N'
    
# get status of magnet based on sensor reading (pass/fail)
def getPassFail(HSVal, actualPole, expectedPole):
    global poleStrengthMinimum
                                                                    
    if HSVal < float(poleStrengthMinimum):                                 # desired cutoff for a "strong" magnet, adjust this value as desired
        return 'strength failure'                                   # fails if magnet reading is not high enough
    elif actualPole != expectedPole:
        return 'polarity failure'                                   # fails if magnet pole is incorrect
    else:
        return 'pass'                                               # magnet passes test

# get sensor readings
def appendSensorReadings(HSRawVal, expectedPole, row):
    actualPole = getPole(HSRawVal)                                  # gets polarity from raw sensor value
    HSVal = abs(HSRawVal)                                           # converts raw sensor value to absolute value
    HSVal=(2.5/512)*HSVal*10                                        #       converts adc value to flux value in mT
    HSPassFail = getPassFail(HSVal, actualPole, expectedPole)       # get if magnet passes or fails test
    row.append(HSVal)                                               #(2.5V/512)*readingADC/100mV=mT (this works for hall sensor PN DRV5055A1)
    row.append('mT')
    row.append(actualPole)                                    
      # append values to row
    row.append(HSPassFail)


# swaps the expected pole direction
def swapDir(expectedPole1):
    if expectedPole1 == 'N': # switch N to S
        return 'S'
    return 'N'  # vice versa (S to N)

# prints failure loations, if any
def passFail():
    global df, dfGPT, dfMCR, barcode, folder, failStatus1, failStatus2

    tableHS1Status = df.filter(['Pole#', 'status']) # filter table to only contain relevant columns for each sensor
    failureTableHS1 = tableHS1Status[np.isin(tableHS1Status, ['strength failure','polarity failure']).any(axis=1)]  # gets table rows where failure(s) occur for each sensor
    
    if failureTableHS1.empty: # if no failures found, test passes
        print('Passed - no failures detected!')
        label8.config(fg="black",bg='#3399ff',text='PASS')
        timestr = time.strftime("(%Y%m%d-%H%M%S)") # add date time stamp and save location
        file = barcode+timestr # file name with date time stamp
        extension = '.xlsx' # file extension
        fullPath = pathlib.Path(os.path.join(folder, file + extension)) # the full file path
        writer = pd.ExcelWriter(path = fullPath, engine='xlsxwriter',engine_kwargs={'options': {'strings_to_formulas': False}})
        df.to_excel(writer, sheet_name='Flux')
        dfGPT.to_excel(writer, sheet_name='HiPot')
        dfMCR.to_excel(writer, sheet_name='IndRes')
        writer.save()
    else:
        
        if not failureTableHS1.empty: # checks each if reading should exist and has a failure
            print('Failure(s) for hall sensor occur at the following magnets:')
            print(failureTableHS1.to_string(index=False))
            label8.config(fg="black",bg='red',text="Failed")
            failStatus1= "Flux Pole strength or polarity failure(s)"
            failStatus2= "Failure(s) listed in spread sheet."
            failure()

def getData():
    global index, folder
    if index!=0:
        return
    passFail()
    print('The full data table can be found at', folder) # lets user know location of full data output
    sleep(2)
    return

def fluxStatus(mag):
    comstat = 'PoleNumber='+str(mag)
    label8.config(fg="black",text=comstat)

def fluxFailure(status):
    global failStatus1, failStatus2
    if status == 'setupY': # status handling
        print(status)
        label8.config(fg="black",bg="white",text='SetupY')
    elif status == 'homingY': # status handling
        print(status)
        label8.config(fg="black",bg="white",text='HomingY')
    elif status == 'homingX': # status handling
        print(status)
        label8.config(fg="black",bg="white",text='HomingX')

    elif status == 'failedHomingY': # failure handling
        print(status)
        label8.config(fg="black",bg="red",text='Failed HomingY')
        failStatus1 = 'Failed Homing Y'
        failStatus2 = 'Check connections and Y limit switches then try again'
        failure()
    elif status == 'failedHomingX':                                 # failure handling
        print(status)
        label8.config(fg="black",bg="red",text='Failed HomingX')
        failStatus1 = 'Failed Homing X'
        failStatus2 = 'Check connections and X limit switch then try again'
        failure()

def dataCollection(partNum, sn):
    global index, failStatus1, failStatus2, df
    # get partNum params
    magNum,yAxis,aPol,cPol,initPole,biidNum,mcrFreq,resMin,resMax,indMin,indMax,mode,gptV,gptI,gptImin,gptFreq=getPartParams(partNum,sn)


    # data collection
    writeMCRf(mcrFreq)
    sleep(.2)
    readMCRf()
    if (resultMCR == int(mcrFreq)):
        testMCR()
    else:
        failMCR = 'MCR frequncy failed, frequency is set to '+ str(resultMCR)+'Hz'
        print('\n'+failMCR)
        failStatus1 = 'Failed MCR Frequency'
        failStatus2 = failMCR
        label4.config(fg="black",bg="red",text=failStatus1)
        failure()
        return False
    testGPT()
    fluxTest()
    if index != 6:                                                          # index used for error handling
        return False
    
    # init flux data collection
    table = []                                                              # blank table for data collection
    mag = 1                                                                 # initial magnet count
    expectedPole = initPole                                                 # set expected pole for first magnet to specified initial pole
    i = 0;                                                                  # all veriables reset
    j = 0;
    k = 0;
    h = int(magNum) / (int(aPol) + int(cPol));                              # h = loop number variable Ex. 48/6 = 8
    h = h/2                                                                 # divide in half so the next while statements will work 8/2=4
    while i < h:                                                            # while i is less than h
        while (j < int(aPol)):                                                   # j should = AabB (k would equal aABb) *if apol = 4 and magNum=48
            serialLineList = sta.readline().decode().split(',')             # read line and split into list
            status = serialLineList[0]                                      # get status (first element of list)
            if status == 'runAB':                                           # if status != standby, collect magnet flux data
                hs1Val= int(serialLineList[1])                              # get hall sensor values
                row = []                                                    # initialize row of data to append
                row.append(mag)                                             # append index
                row.append(expectedPole)                                    # append expected pole direction
                appendSensorReadings(hs1Val, expectedPole, row)             # expected pole is opposite of next while loop
                table.append(row)                                           # append row of data to list
                expectedPole = swapDir(expectedPole)                        # swap direction of pole 
                print(mag, status, hs1Val)
                fluxStatus(mag)                                             # updates GUI what pole# its on
                mag += 1                                                    # increment number of magnets checked
                j += 1
            fluxFailure(status)                                             # update GUI on other status and checks for odd errors
        expectedPole = swapDir(expectedPole)                                # swap direction of pole
        while (k < int(aPol)):                                                   # j should = AabB (k would equal aABb) *if apol = 4 and magNum=48
            serialLineList = sta.readline().decode().split(',')             # read line and split into list
            status = serialLineList[0]                                      # get status (first element of list)
            if status == 'runAB':                                           # if status != standby, collect magnet flux data
                hs1Val= int(serialLineList[1])                              # get hall sensor values
                row = []                                                    # initialize row of data to append
                row.append(mag)                                             # append index
                row.append(expectedPole)                                    # append expected pole direction
                appendSensorReadings(hs1Val, expectedPole, row)             # expected pole is opposite of previous while loop
                table.append(row)                                           # append row of data to list
                expectedPole = swapDir(expectedPole)                        # swap direction of pole 
                print(mag, status, hs1Val)
                fluxStatus(mag)                                             # updates GUI what pole# its on
                mag += 1                                                    # increment number of magnets checked
                k += 1
            fluxFailure(status)                                             # update GUI on other status and checks for odd errors
        k=0
        j=0
        i +=1
        expectedPole = swapDir(expectedPole)
    k=0    
    j=0
    i=0
    while i < h:
        while (j < int(cPol)):
            serialLineList = sta.readline().decode().split(',')             # read line and split into list
            status = serialLineList[0] 
            if status == 'runBC':                                           # if status != standby, collect magnet flux data
                hs1Val= int(serialLineList[1])                              # get hall sensor values
                row = []                                                    # initialize row of data to append
                row.append(mag)                                             # append index
                row.append(expectedPole)                                    # append expected pole direction
                appendSensorReadings(hs1Val, expectedPole, row)
                table.append(row)                                           # append row of data to list
                expectedPole = swapDir(expectedPole)                        # swap direction of pole
                print(mag, status, hs1Val)
                fluxStatus(mag)                                             # updates GUI what pole# its on
                mag += 1
                j += 1
            fluxFailure(status)                                             # update GUI on other status and checks for odd errors
        expectedPole = swapDir(expectedPole)
        while (k < int(cPol)):
            serialLineList = sta.readline().decode().split(',')             # read line and split into list
            status = serialLineList[0] 
            if status == 'runBC':                                           # if status != standby, collect magnet flux data
                hs1Val= int(serialLineList[1])                              # get hall sensor values
                row = []                                                    # initialize row of data to append
                row.append(mag)                                             # append index
                row.append(expectedPole)                                    # append expected pole direction
                appendSensorReadings(hs1Val, expectedPole, row)
                table.append(row)                                           # append row of data to list
                expectedPole = swapDir(expectedPole)                        # swap direction of pole
                print(mag, status, hs1Val)
                fluxStatus(mag)                                             # updates GUI what pole# its on
                mag += 1
                k += 1
            fluxFailure(status)                                             # update GUI on other status and checks for odd errors
        k=0
        j=0
        i +=1
        expectedPole = swapDir(expectedPole)
    k=0    
    j=0
    i=0
        
    # sending data
    cols = ['Pole#', 'expected pole', 'sensor value','mT', 'actual pole', 'status'] # column labels
    df = pd.DataFrame(table, columns=cols)                                          # place table into a pandas Dataframe object
    print (df)
    index=0
    getData()
    if mag != int(magNum)+1:
        failStatus1 = 'Failed: Expected Pole# Should ='+magNum
        failStatus2 = 'Actual Pole# Tested ='+str(mag)
        print (failStatus1)
        print (failStatus2)
        label.config(fg="black",bg='red',text="Failed Flux Test")
        label8.config(fg="black",bg='red',width=25,font=16, text="Test Failed")
        index=0
        failure()
    label.config(fg="black",bg='#3399ff',text="Enter Barcode")
    barcode_var.set('') # clears text inside of gui entry field and sets cursor
    return                                                                         

def openConfig():
    configFile = filedialog.askopenfilename(initialdir=configFolder, title="Stator Tester Config Files",filetypes=(("txt files", "*.txt"),("all files", "*.*")))
    configFile = '"'+configFile+'"'
    if len(configFile) >=3:
        path = str('start '+ "notepad " + configFile)
        os.system(path)
        
# gives instructions/about the program          
def about():
    window = tk.Tk()
    window.title("About")
    window.rowconfigure(0, minsize=400, weight=1)      #about window row#, size, wieght
    window.wm_iconbitmap('icon.ico')
    window.geometry('1200x600')
    window.config(bg='#3399ff')
    message ='''
    --About the program--
    Stator Tester GUI
    Author: Doug Gammill
    Date: 10/31/2021
    Copyright (c) 2021
    Tests a Stator for flux strength and polarity for each of its poles.
    Conducts a phase to phase inductance and resistance test for all three phases.
    Conducts a Hi Pot test.
    
    General Test Procedure:
    1. Turn on MCR-5100 (LCR meter), and GPT-9803 (hi pot meter).
    2. Turn on Stator tester power switch on the back and then the power supply LCD located on the front.
    3. Ensure all USB cables for each device are connected to the laptop
    4. Ensure Linear Labs Stator Tester computer application (gui) has indicated USB coms are good with each device.
    5. Place the desired part into the test fixture. Make sure to use the correct adapter for the part.
    6. Scan the barcode located in the part folder using the barcode scanner.
    7. Confirm part number selected is correct
    8. Confirm that there are no failure(s) for the part by reading the label outputs.
    9. Check the excel output file if desired in Options Menu under Results.
    '''
    text_box = Text(window,height=23,width=95, font=("Adobe",16))
    text_box.pack(expand=True)
    text_box.insert('end', message)
    text_box.config(state='disabled')#change to normal for edit mode
    window.mainloop()

def configPaths():
    #os.system('folderConfig.txt') # opens config with cmd
    os.popen('folderConfig.txt', 'w') # opens config without cmd

def open_file():
    global folder
    filename = filedialog.askopenfilename(initialdir=folder, title="Stator Test Results",filetypes=(("xlsx files", "*.xlsx"),("all files", "*.*")))
    filename = '"'+filename+'"'
    if len(filename) >=3:
        path = str('start '+ "excel " + filename)
        os.system(path)

def failure():
    global failStatus1, failStatus2, barcode, df, dfMCR, dfGPT, folder, index
    fail = tk.Tk()

    def save_file():
        
        table = []
        
        row = []                                                    # initialize row of data to append
        row.append(failStatus1)
        table.append(row)

        row = []
        row.append(failStatus2)
        table.append(row)

        row = []
        input1 = txt_edit.get("1.0",END)
        str(txt_edit)
        row.append(input1)
        table.append(row)
 
        cols = ['Failures:']
        dfFail = pd.DataFrame(table, columns=cols)

        # add date time stamp and save location
        timestr = time.strftime("(%Y%m%d-%H%M%S)")
        file = 'Failure-'+barcode+timestr                                           # file name with date time stamp
        extension = '.xlsx'                                                         # file extension
        fullPath = pathlib.Path(os.path.join(folder, file + extension))             # the full file path
        writer = pd.ExcelWriter(path = fullPath, engine='xlsxwriter',engine_kwargs={'options': {'strings_to_formulas': False}})       
        if index > 0 and index < 4:                                                 # index should be inbetween 1 and 3 if MCR fails
            dfFail.to_excel(writer, sheet_name='Failures')                          # include failure data only
            writer.save()
        elif index == 4:                                                              # index should be 4 if hi pot fails
            dfFail.to_excel(writer, sheet_name='Failures')                      # include failure data
            dfMCR.to_excel(writer, sheet_name='IndRes')                         # include MCR data
            writer.save()
        elif index >= 5:
            dfFail.to_excel(writer, sheet_name='Failures')                      # include failure data
            dfGPT.to_excel(writer, sheet_name='HiPot')                          # include HiPot data
            dfMCR.to_excel(writer, sheet_name='IndRes')
            writer.save()
        elif index == 0:                                                        # index should be 0 if flux fails or passes
            dfFail.to_excel(writer, sheet_name='Failures')                      # include failure data
            df.to_excel(writer, sheet_name='Flux')                              # include Flux test data
            dfGPT.to_excel(writer, sheet_name='HiPot')                          # include HiPot data
            dfMCR.to_excel(writer, sheet_name='IndRes')                         # include MCR data
            writer.save()
        reset()
        barcode_var.set('')                                                             # clears text inside of gui entry field and sets cursor
        return
        
    def reset():

        label.config(fg="black",bg='#3399ff',text='Enter Barcode')
        label4.config(fg="black",bg="white",text='A-B LCR:')
        label5.config(fg="black",bg="white",text='A-C LCR:')
        label6.config(fg="black",bg="white",text='B-C LCR:')
        label7.config(fg="black",bg="white",text='HiPot:')
        label8.config(fg="black",bg="white",width=25,font=16, text='Flux:')
        index=0
        barcode_var.set('')
        fail.destroy()
    
    fail.title("Failure!!!")
    fail.rowconfigure(0, minsize=200, weight=1)       #about window row#, size, wieght
    fail.columnconfigure(1, minsize=400, weight=1)    #main window col#, size, wieght
    fail.geometry('1000x300')
    fail.wm_iconbitmap('icon.ico')
    fail.config(bg='red')

    txt_edit = tk.Text(fail, height=3, width=35, font=("Adobe",16))
    txt_edit.grid(row=0, column=1, sticky="nsew")
    txt_edit.insert('1.0', '------------Enter Any Notes Here------------')

    failLabel = tk.Label(fail, fg="black",bg='red',width=80, font='12', text='Enter additional notes and save or reset to start again.')
    failLabel.grid(row=1, column=1)

    failLabel1 = tk.Label(fail, fg="black",bg='red',width=80, font='12', text=failStatus1)
    failLabel1.grid(row=2, column=1)
    
    failLabel2 = tk.Label(fail, fg="black",bg="red",width=80, font='12', text=failStatus2)
    failLabel2.grid(row=3, column=1)
    
    fr_buttons = tk.Frame(fail)
    btn_reset = tk.Button(fr_buttons,font='12', text="Reset", command=reset)
    btn_save = tk.Button(fr_buttons,font='12', text="Save", command=save_file)

    btn_reset.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_save.grid(row=1, column=0, sticky="ew", padx=5)
    fr_buttons.grid(row=0, column=0, sticky="ns")
    fr_buttons.configure(bg='red')
      
    fail.mainloop()

def resetGui():
    label.config(fg="black",bg='#3399ff',text='Enter Barcode')
    label4.config(fg="black",bg="white",text='A-B LCR:')
    label5.config(fg="black",bg="white",text='A-C LCR:')
    label6.config(fg="black",bg="white",text='B-C LCR:')
    label7.config(fg="black",bg="white",text='HiPot:')
    label8.config(fg="black",bg="white",width=25,font=16, text='Flux:')
    index=0
    barcode_var.set('')

def threading(event): # threading used to execute main functions and allow GUI main loop to not freeze
    t2=Thread(target=getPartInfo)# event is used for gui entry .bind <return>
    t2.start()  

def getPartInfo(): # event is used for gui entry .bind <return>
    global barcode, partNum, sn, comOK, index
    barcode=barcode_var.get()
    usbComs()
    if comOK==1:
        try:
            index=1
            #barcode=barcode_var.get()
            print(barcode)
            resetGui()                                                
            if len(barcode.split('-')) == 4: # check if the barcode is the correct length/format
                first, second, third, sn = barcode.split('-')       # put barcode into list of strings
                partNum=first+'-'+second+'-'+third
                status='Testing: '+partNum
                label.config(fg="black",bg='Yellow',text=status)
                dataCollection(partNum, sn)                                                                                      # if correct format, do nothing
            else:
                raise ValueError # if wrong format, ask to scan again
        except ValueError:
            print('ERROR: Invalid barcode! Please scan again.')
            barcode_var.set('Error: Invalid barcode!')
            return
    else:
        label.config(fg="black",bg='red',text='Connect USB')
        barcode_var.set('Connect USB')
        
def checkUSB():
    global comOK,index,comstat1,comstat2,comstat3,usbPassFail1, usbPassFail2, usbPassFail3
    if comOK == 1 and index == 0: # comOK means at some point USB was good and index=0 means not currently testing
        label.config(fg="black",bg='orange',text='Checking USB')
        try:
            mcr.flushInput() # get rid of any stale input
            mcr.write(idQuery) # request the data
            sleep(.5)
            result = mcr.readline() # capture the result
            result = result.decode() # convert from bytes to string
            result = result.strip() # strip off \r\n
            print(result)
            
            if result!= idResponseLCR:
                if result != 'homingX,' and result != 'homingY,':
                    label.config(fg="black",bg='red',text='Connect USB')
                    usbPassFail1 = 1  # fail
            else:
                label1.config(fg="black",bg='#3399ff',text=comstat1)
                usbPassFail1 = 0  # pass
                
            gpt.flushInput() # get rid of any stale input
            gpt.write(idQuery) # request the data
            sleep(.5)
            result = gpt.readline() # capture the result
            result = result.decode() # convert from bytes to string
            result = result.strip() # strip off \r\n
            print(result)
            if result != idResponseHpot:
                if result != 'homingX,' and result != 'homingY,':
                    label.config(fg="black",bg='red',text='Connect USB')
                    usbPassFail2 = 1 # fail
            else:
                label2.config(fg="black",bg='#3399ff',text=comstat2)
                usbPassFail2 = 0  # pass
                
            sta.flushInput() # get rid of any stale input
            sta.write(idQuery) # request the data
            sleep(.5)
            result = sta.readline() # capture the result
            result = result.decode() # convert from bytes to string
            result = result.strip() # strip off \r\n
            print(result)
            if result != idResponseStat:
                if result != 'homingX,' and result != 'homingY,':
                    label.config(fg="black",bg='red',text='Connect USB')
                    usbPassFail3 = 1  # fail
            else:
                label3.config(fg="black",bg='#3399ff',text=comstat3)
                usbPassFail3 = 0 # pass
            label.config(fg="black",bg='#3399ff',text='Enter Barcode')
        except:
            comOK=0
            label.config(fg="black",bg='red',text='Connect USB')
            #break


def connectUSB():
    global usbPassFail1, usbPassFail2, usbPassFail3, comOK
    # Put that code inside the try block
    # which may generate the error
    while comOK == 0 and index==0:
        try:
            connectLCR() # get MCR COM port
            if usbPassFail1 == 1: # error handling
                label1.config(bg='red', text='Error')
        except:
            label1.config(bg='red', text='Error')
        try:
            connectGPT() # get GPT COM port
            if usbPassFail2 == 1: # error handling
                label2.config(bg='red', text='Error')
        except:
            label2.config(bg='red', text='Error')
        try:       
            connectTester() # get Arduino COM port
            if usbPassFail3 == 1: # error handling
                label3.config(bg='red', text='Error')
        except:
            label3.config(bg='red', text='Error')
        if usbPassFail1 == 0 and usbPassFail2 == 0 and usbPassFail3 == 0:
            comOK=1

def usbComs():
    checkUSB()
    connectUSB()
    checkUSB()
    return

def usbThread():
    t1=Thread(target=usbComs)
    t1.start()

    
# main program; user interface
if __name__ == "__main__":
    gui = tk.Tk()

    for i in range(8):  ###rows = 10
        gui.columnconfigure(i, weight=1)#, minsize=5)
        gui.rowconfigure(i, weight=1,minsize=40)
        for j in range(0,2): ###column=5
            frame = tk.Frame(
                master=gui,
                relief=tk.RAISED,
                borderwidth=1
            )
    gui.configure(background="black")
        
    gui.title("Linear Labs Stator Tester")
        
    gui.wm_iconbitmap('icon.ico')
        
    gui.geometry("850x450") #width x hieght
        
    gui.resizable(width=False, height=False)
          
    label = tk.Label(fg="white",bg="red",relief='ridge',width=50,font='12',borderwidth=5,text="Do Not Enter Barcode Yet")
    label.grid(row=0, columnspan=2)
    label.update()

    barcode_var = tk.StringVar()
    expression_field = tk.Entry(gui,width=50,font='12',borderwidth=5,textvariable=barcode_var)
    expression_field.grid(row=1, columnspan=2)
    expression_field.bind('<Return>', threading)
    expression_field.icursor('end')
    expression_field.focus_set() # insert cursor
    expression_field.update()

    menubar = Menu(gui, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')
    help = Menu(menubar, tearoff=0)  
    help.add_command(label="About", command=about)
    help.add_command(label="Results", command=open_file)
    help.add_command(label="Configs", command=openConfig)
    help.add_command(label="Paths", command=configPaths)
    help.add_command(label="CheckUSB", command=usbThread)
    menubar.add_cascade(label="Options", menu=help)
    gui.config(menu=menubar)

    usb1 = tk.Label(fg="white",bg='purple',relief='ridge',width=15,font='12',borderwidth=5,text='MCR5100 USB: ')
    usb1.grid(row=0, column=2)
    usb1.update()
    
    usb2 = tk.Label(fg="white",bg="purple",relief='ridge',width=15,font='12',borderwidth=5,text='GPT9803 USB: ')
    usb2.grid(row=0, column=3)
    usb2.update()

    usb3 = tk.Label(fg="white",bg='purple',relief='ridge',width=15,font='12',borderwidth=5,text='Tester USB: ')
    usb3.grid(row=0, column=4)
    usb3.update()
      
    label1 = tk.Label(fg="black",bg='white',relief='ridge',width=15,font='12',borderwidth=5,text='MCR5100 USB: ')
    label1.grid(row=1, column=2)
    label1.update()
    
    label2 = tk.Label(fg="black",bg="white",relief='ridge',width=15,font='12',borderwidth=5,text='GPT9803 USB: ')
    label2.grid(row=1, column=3)
    label2.update()

    label3 = tk.Label(fg="black",bg='white',relief='ridge',width=15,font='12',borderwidth=5,text='Tester USB: ')
    label3.grid(row=1, column=4)
    label3.update()

    label4 = tk.Label(fg="black",bg="white",relief='ridge',width=25,font='12',borderwidth=5, text='A-B LCR:')
    label4.grid(row=2, column=1)
    label4.update()

    label5 = tk.Label(fg="black",bg="white",relief='ridge',width=25,font='12',borderwidth=5, text='A-C LCR:')
    label5.grid(row=3, column=1)
    label5.update()

    label6 = tk.Label(fg="black",bg="white",relief='ridge',width=25,font='12',borderwidth=5, text='B-C LCR:')
    label6.grid(row=4, column=1)
    label6.update()

    label7 = tk.Label(fg="black",bg="white",relief='ridge',width=25,font='12',borderwidth=5, text='HiPot:')
    label7.grid(row=5, column=1)
    label7.update()

    label8 = tk.Label(fg="black",bg="white",relief='ridge',width=25,font='12',borderwidth=5, text='Flux:')
    label8.grid(row=6, column=1)
    label8.update()

    test4 = tk.Label(fg='#3399ff',bg="black",width=25,font='12',borderwidth=5, text='A-B LCR:')
    test4.grid(row=2, column=0)
    test4.update()

    test5 = tk.Label(fg='#3399ff',bg="black",width=25,font='12',borderwidth=5, text='A-C LCR:')
    test5.grid(row=3, column=0)
    test5.update()

    test6 = tk.Label(fg='#3399ff',bg="black",width=25,font='12',borderwidth=5, text='B-C LCR:')
    test6.grid(row=4, column=0)
    test6.update()

    test7 = tk.Label(fg='#3399ff',bg="black",width=25,font='12',borderwidth=5, text='HiPot:')
    test7.grid(row=5, column=0)
    test7.update()

    test8 = tk.Label(fg='#3399ff',bg="black",width=25,font='12',borderwidth=5, text='Flux:')
    test8.grid(row=6, column=0)
    test8.update()

    load= Image.open("logo4.ppm")
    render = ImageTk.PhotoImage(load)
    img = Label(gui, image=render)
    img.grid(row=4, column=2, columnspan=3)
    img.update()

    usbThread()

    gui.mainloop()

