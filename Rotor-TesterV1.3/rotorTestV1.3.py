'''
Rotor Test
Author: Eric Tseng
Date: 8/12/2021
Copyright (c) 2021
Linear Labs, Inc.

Tests a rotor for strength and polarity for each of its magnets.

General Program Procedure:
    1. Connect to Arduino
    2. Scan a barcode
    3. Confirm model selected is correct**
    4. Get parameters for model
    5. Send parameters to Arduino
    6. Receive test data from Arduino
    7. Determines if test passes/fails and outputs failure locations, if any
    8. Output hall sensor reading statistics (average and standard deviation)
    9. Place results in an excel file. Sample data is in the Production Drive (Production (O):\Manufacturing Engineering\Rotor Test\Rotor Test Sample Data.csv)
    (** indicates required action by user)

'''

'''
Usage:
import rotorTest                                            # import the module
rotorTest.getData()                                         # runs magnet test and determines pass/fail

Demo Application:
import rotorTest                                            # import the module
rotorTest.run()                                             # entire program with UI (for technician use)
'''

import pandas as pd                                         # library for handling data inputted into csv file
import serial                                               # library for serial communication (pyserial)
import numpy as np                                          # library for numerical/matrix manipulation
from time import sleep                                      # used for pausing program for set time
import serial.tools.list_ports                              # used to get full list of available COM ports
from serial.serialutil import SerialException               # used for exception handling
from msvcrt import getch                                    # used for instantaneous user input (key press instead of key press + enter)
import pathlib                                              # for determining if path/file exists
import os                                                   # for working with file paths
import configparser                                         # handles reading config files
from pathlib import Path

configParser = configparser.RawConfigParser()   
configFilePath = 'folderConfig.txt'
configParser.read(configFilePath)
folder = configParser.get('folderPath', 'savePath')

# returns list of available COM ports; copied from mcr5100.py
def getPorts():
    ports = []                          # list of possible ports
    result = []                         # list of open ports

    # this is the method for Windows
    for i in range(256):                # generate a list of ports to try
        ports.append('COM%s' % (i+1))   # eg. COM1, COM2 ...

    for port in ports:                  # try each port in the list
        try:
            s = serial.Serial(port)     # attempt to open the port
            s.close()                   # close the port
            result.append(port)         # save the available port
        except(OSError, serial.SerialException):
            pass                        # ignore the exception and continue
    return result
    

# returns COM port of arduino; works no matter how may COM port devices are connected (including multiple Arduinos)
# heavily based off https://stackoverflow.com/questions/24214643/python-to-automatically-select-serial-ports-for-arduino
def getArduinoCOM():
    print('\n--Waiting for Arduino to Connect--')
    print('If the program is printing dots, check to make sure that the power is on and machine is plugged into the computer.')

    while True:
        ports = getPorts()
        for p in ports:                        
            ser = serial.Serial(p, 115200, timeout=1)          # open serial port with specified COM port, baud rate, and timeout
            sleep(1)                                           # wait full second for Arduino to set up - do not reduce this value
            try:
                returnMessage = ser.readline().decode().strip() # try to get return message from Arduino, if any
            except:
                returnMessage = 'blank'
            if returnMessage == '<Rotor Arduino is ready>':     # check to make sure arduino connected is for rotor
                print('\nArduino connected at port', p)         # show that Arduino connected
                return p                                        # return COM port
            ser.close()                                         # close serial port
        print('.', end='', flush=True)                          # show we are searching
        sleep(1)                                                # wait a second between searches

# asks for user to input COM port for Arduino and returns it
# backup option in place of getArduinoCOM(); use if the computer is unable to detect the COM port as an Arduino port
def getArduinoCOMManual():
    port = input("Enter a port number: ")                   # get input
    while True:
        try:
            port = int(port.decode())                       # try to convert port to int
        except ValueError:
            input('ERROR: Invalid port! Please try again: ')       # asks for port again if invalid input
        if type(port) == int:                               # if port is int
            return port                                     # return the port

# returns model, number, part
def getPartInfo():
    print('\n--Scan Barcode--')
    print('If the barcode is not scanning, make sure that the barcode scanner USB is plugged in.')

    # make sure that the barcode doesn't have too many/little values first; loops until the barcode reading is valid
    while True:
        try:
            barcode = input('Barcode reading: ')                                        # ask for barcode reading - i.e. scan barcode
            if len(barcode.split('-')) == 4:                                            # check if the barcode is the correct length/format
                modelNameFront, modelNameBack, part, modelNum = barcode.split('-')      # put barcode into list of strings
                modelName = modelNameFront + '-' + modelNameBack+ '-' + part            # splice together the model name
                file = modelName + '-' + modelNum                                       # file name w/o version number
                extension = '.xlsx'                                                     # file extension
                folder = 'O:\\Manufacturing Engineering\\Rotor Test\\Rotor Test Results\\'  # the folder where the file is located
                fullPath = pathlib.Path(os.path.join(folder, file, extension))          # the full file path
                if fullPath.exists() == True:                                           # make sure that the file does not already exist
                    fullPath = appendNewerVersion(folder, file, extension, 2)           # call recursive function that adds version number
                break                                                                   # if correct format, do nothing
            else:
                raise ValueError                                                        # if wrong format, ask to scan again
        except ValueError:
            print('ERROR: Invalid barcode! Please scan again.')
    
    # returns variables
    return modelName, modelNum, part                                        # return model name, model number, and part (ex. Beta-2, 27, H)

# returns number of magnets, number of steps in the y-direction, number of steps in the z-direction, and starting/initial pole, (cont.)
# and flags for if a reading is expected from each hall sensor (1-3)
# NOTE: y and z steps may need calibration (hardware changes throw these off easily)
# NOTE: add more instances of models accordingly by adding to the if-elif-else statement
def getPartParams(modelName, part):
    try:

        configFile = modelName
        configParser = configparser.RawConfigParser()   
        configFilePath = configFile+'.txt'
        #print(configFilePath)

        if Path(configFilePath).is_file():
            configParser.read(configFilePath)
            totalMag = configParser.get(configFile, 'totalMag')
            #print ('totalMag='+totalMag)
            ySteps = configParser.get(configFile, 'ySteps')
            #print ('ySteps='+ySteps)
            zSteps = configParser.get(configFile, 'zSteps')
            #print ('zSteps='+zSteps)
            initPole = configParser.get(configFile, 'initPole')
            #print ('initPole='+initPole)
            usesHS1 = configParser.get(configFile, 'usesHS1')
            #print ('usesHS1='+usesHS1)
            usesHS2 = configParser.get(configFile, 'usesHS2')
            #print ('usesHS2='+usesHS2)
            usesHS3 = configParser.get(configFile, 'usesHS3')
            #print ('usesHS3='+usesHS3)
            totalMag = int(totalMag)
            ySteps = int(ySteps)
            zSteps = int(zSteps)
            #initPole = 'N'
            usesHS1 = int(usesHS1)
            usesHS2 = int(usesHS2)
            usesHS3 = int(usesHS3)
        else:
            raise NameError
        if ySteps > 8200 or zSteps > 14200: # y and z step limits
            raise ValueError
    except NameError:                       # print error message and return default values
        print('ERROR: Invalid part number!')
        totalMag = 0
        ySteps = 0
        zSteps = 0
        initPole = 'N'
        usesHS1 = True
        usesHS2 = False
        usesHS3 = False
        
    except ValueError:                      # print error message and return default values
        print('ERROR: Out of bounds, check your y and z steps!')
        totalMag = 0
        ySteps = 0
        zSteps = 0
        initPole = 'N'
        usesHS1 = True
        usesHS2 = False
        usesHS3 = False
        
    return totalMag, ySteps, zSteps, initPole, usesHS1, usesHS2, usesHS3

# send params to arduino via serial
def sendPartParams(ser, totalMag, ySteps, zSteps):
    
    colonSend = ':'                          # colon to start Arduino program in string format
    mSend = 'm' + str(totalMag) + '\r\n'     # number of magnets in string format
    ySend = 'y' + str(ySteps) + '\r\n'       # number of y steps in string format
    zSend = 'z' + str(zSteps) + '\r\n'       # number of z steps in string format
    ser.write(bytearray(colonSend, 'utf-8')) # convert all strings to bytearray format and send to Arduino via serial
    ser.write(bytearray('\r\n', 'utf-8'))    # new line for spacing (carriage return)
    ser.write(bytearray(mSend, 'utf-8'))
    ser.write(bytearray(ySend, 'utf-8'))
    ser.write(bytearray(zSend, 'utf-8'))

# sets pole direction based on sensor value
def getPole(HSRawVal):
    if HSRawVal > 0:                         # if raw value greater than zero, magnet is South pole
        return 'S'
    return 'N'                               # otherwise the magnet is North pole

# get status of magnet based on sensor reading (pass/fail)
def getPassFail(HSVal, actualPole, expectedPole):
    if HSVal < 100:                          # NOTE: desired cutoff for a "strong" magnet, adjust this value as desired
        return 'strength failure'            # fails if magnet reading is not high anough
    elif actualPole != expectedPole:
        return 'polarity failure'            # fails if magnet pole is incorrect
    else:
        return 'pass'                        # magnet passes test

# get sensor readings
def appendSensorReadings(HSRawVal, expectedPole, row):
    actualPole = getPole(HSRawVal)           # gets polarity from raw sensor value
    HSVal = abs(HSRawVal)                    # converts raw sensor value to absolute value
    HSVal=(2.5/512)*HSVal/.0125
    HSPassFail = getPassFail(HSVal, actualPole, expectedPole) # get if magnet passes or fails test

    row.append(HSVal)                        # append values to row
    row.append(actualPole)
    row.append(HSPassFail)

# add null readings to rows where no hall sensor values expected
def appendNullReadings(row):
    row.append('NA')                         # append blank values to row
    row.append('NA')
    row.append('NA')

# swaps the expected pole direction
def swapDir(expectedPole):
    if expectedPole == 'N':                 # switch to N to S
        return 'S'
    return 'N'                              # vice versa (S to N)

# prints failure loations, if any
def printFailures(table, usesHS1, usesHS2, usesHS3):
    print('\n--Magnet Flux Test--')

    # filter table to only contain relevant columns for each sensor
    tableHS1Status = table.filter(['index', 'sensor 1 status'])
    tableHS2Status = table.filter(['index', 'sensor 2 status'])
    tableHS3Status = table.filter(['index', 'sensor 3 status'])

    # gets table rows where failure(s) occur for each sensor
    failureTableHS1 = tableHS1Status[np.isin(tableHS1Status, ['strength failure','polarity failure']).any(axis=1)]
    failureTableHS2 = tableHS2Status[np.isin(tableHS2Status, ['strength failure','polarity failure']).any(axis=1)]
    failureTableHS3 = tableHS3Status[np.isin(tableHS3Status, ['strength failure','polarity failure']).any(axis=1)]

    # if no failures found, test passes
    if failureTableHS1.empty and failureTableHS2.empty and failureTableHS3.empty:
        print('Passed - no failures detected!')
    else:
        # checks each if reading should exist and has a failure
        if usesHS1 and not failureTableHS1.empty:
            print('Failure(s) for sensor 1 occur at the following magnets:')
            print(failureTableHS1.to_string(index=False))
        if usesHS2 and not failureTableHS2.empty:
            print('Failure(s) for sensor 2 occur at the following magnets:')
            print(failureTableHS2.to_string(index=False))
        if usesHS3 and not failureTableHS3.empty:
            print('Failure(s) for sensor 3 occur at the following magnets:')
            print(failureTableHS3.to_string(index=False))


# read table and get summary of sensor values (average/stdev, etc.)
def printStats(table, usesHS1, usesHS2, usesHS3):
    print('\n--Statistics--')
    if usesHS1:
        print('Average of sensor 1 values:', round(table['sensor 1 value'].mean() ,2))
        print('Standard deviation of sensor 1 values:', round(table['sensor 1 value'].std(), 2))
        print('')
    if usesHS2:
        print('Average of sensor 2 values:', round(table['sensor 2 value'].mean(), 2))
        print('Standard deviation of sensor 2 values:', round(table['sensor 2 value'].std(), 2))
        print('')
    if usesHS3:
        print('Average of sensor 3 values:', round(table['sensor 3 value'].mean(), 2))
        print('Standard deviation of sensor 3 values:', round(table['sensor 3 value'].std(), 2))
        print('')

# collect data and place it into pandas dataframe
def dataCollection(ser, modelName, part):
    # get model params
    totalMag, ySteps, zSteps, initPole, usesHS1, usesHS2, usesHS3 = getPartParams(modelName, part)

    # init data collection
    table = []                                                          # blank table for data collection
    mag = 0                                                             # initial magnet count
    expectedPole = initPole                                             # set expected pole for first magnet to specified initial pole

    print('Scanning Data, please keep hands away from moving parts')    # warning message

    # data collection
    while mag < totalMag:                                               # while not all magnets have been measured
        serialLineList = ser.readline().decode().split(', ')            # read line and split into list
        status = serialLineList[0]                                      # get status (first element of list)
        
        if status == 'running':                                         # if status != standby, collect magnet flux data
            hs1Val, hs2Val, hs3Val = int(serialLineList[2]), int(serialLineList[4]), int(serialLineList[6].strip()) # get hall sensor values

            row = []                                                    # initialize row of data to append
            index = mag + 1                                             # get index (start at 1 instead of 0)
            row.append(index)                                           # append index
            row.append(expectedPole)                                    # append expected pole direction

            # get pole direction & status (pass/fail) for each sensor and send to row
            # only get readings for each sensor if a reading is expected
            if usesHS1:
                appendSensorReadings(hs1Val, expectedPole, row)
            else:
                appendNullReadings(row)
            if usesHS2:
                appendSensorReadings(hs2Val, expectedPole, row)
            else:
                appendNullReadings(row)
            if usesHS3:
                appendSensorReadings(hs3Val, expectedPole, row)
            else:
                appendNullReadings(row)

            table.append(row)                                           # append row of data to list

            expectedPole = swapDir(expectedPole)                        # swap direction of pole
            mag += 1                                                    # increment number of magnets checked

    ser.close()                                                         # close serial
    # sending data
    cols = ['index', 'expected pole direction', 'sensor 1 value', 'sensor 1 actual pole direction', 'sensor 1 status',
    'sensor 2 value', 'sensor 2 actual pole direction ', 'sensor 2 status',
    'sensor 3 value', 'sensor 3 actual pole direction', 'sensor 3 status'] # column labels
    df = pd.DataFrame(table, columns=cols)                                 # place table into a pandas Dataframe object
    return df                                                              # DataFrame is basically a table with row/column labels

# recursive function that returns the correct version number of the part by recursively scanning the file path for the same file
def appendNewerVersion(folder, file, extension):
    index = int(file.rfind('V'))                                                # get index left of current version number
    versionNum = int(file[index+1:]) + 1                                        # get current version number and increment it
    keep = file[0:index+1]                                                      # get part of file string to keep
    file = keep + str(versionNum)                                               # combine the file with its new version number
    fullPath = pathlib.Path(os.path.join(folder, file + extension))             # combine to get full file path
    if fullPath.exists() == True:                                               # if the path exists already
        return appendNewerVersion(folder, file, extension)                      # recursively call the function with new version number
    else:                                                                       # if path doesn't exist
        return fullPath                                                         # return path

# runs the rotor test
def getData():
    # set up serial port
    # use getArduinoCOM() for automatically port selection
    # if computer cannot detect COM port as Arduino, use getArduinoCOMManual() for manual input
    portNum = getArduinoCOM()                          # get Arduino COM port
    ser = serial.Serial(portNum, 115200, timeout=.5)   # open serial port with specified COM port, baud rate, and timeout

    # get model info and params
    modelName, modelNum, part = getPartInfo()
    totalMag, ySteps, zSteps, initPole, usesHS1, usesHS2, usesHS3 = getPartParams(modelName, part)
    file = modelName + '-' + modelNum
    
    if totalMag >=1:
        # buffers program until 'y' key pressed (to send) or any other key to cancel
        print('Your selected part is ' + file + '. Continue?')
        print('Press \'y\' to confirm, or any other key to cancel.')
        key = getch()                                   # wait for user input (bytearray format)
        keyStr = key.decode()                           # convert input to string format
        if keyStr == 'y' or keyStr == 'Y' and totalMag >=1:              # only continue if confirm key pressed
            # send magnet number, y steps, and z steps to arduino
            sendPartParams(ser, totalMag, ySteps, zSteps)

            # collect data
            df = dataCollection(ser, modelName, part)

            # add version number and save location
            file = modelName + '-' + modelNum + '-' + 'V1'             # file name; version 1 by default
            extension = '.xlsx'                                                     # file extension
            folder = r'O:\Manufacturing Engineering\Rotor Test\Rotor Test Results'  # the folder where the file is located
            fullPath = pathlib.Path(os.path.join(folder, file + extension))         # the full file path
            if fullPath.exists() == True:                                           # if current file and file version already exists
                fullPath = appendNewerVersion(folder, file, extension)              # call recursive function that adds version number
            df.to_excel(fullPath, index=False)                                      # output to excel file

        # print failure locations and data statistics
            printFailures(df, usesHS1, usesHS2, usesHS3)
            printStats(df, usesHS1, usesHS2, usesHS3)
            print('The full data table can be found at', fullPath) # lets user know location of full data output

            # buffers program until any key pressed (to return to main screen)
            print('Press any key to return to the main screen.')
            getch()

    else: # if the user wants to terminate (confirm key not pressed)
        print('\nThe selection has been cancelled. You will return to the main menu in 5 seconds.')
        sleep(5)

# exits the program
def exit():
    print('\nThe program has been terminated. This screen will close in 5 seconds.')
    sleep(5)

# gives instructions/about the program
def about():
    print('\n--About the program--')
    print('Rotor Test')
    print('Author: Eric Tseng')
    print('Date: 8/12/2021')
    print('Copyright (c) 2021')
    print('Linear Labs, Inc.')
    print('\nTests a rotor for strength and polarity for each of its magnets.')
    print('\nGeneral Test Procedure:')
    print('1. Turn on the power switch of the electronics box.')
    print('2. Connect the USB cable to the laptop')
    print('3. Navigate to Production (O):\Manufacturing Engineering\Rotor Test\Rotor Test Results')
    print('4. Place the desired part into the test fixture. Make sure to use the correct adapter for the part.')
    print('5. Scan the barcode located in the part folder using the barcode scanner')
    print('6. Confirm model selected is correct')
    print('7. Confirm that there are no failure(s) for the part by reading the command line output. (the pass message is: Passed - no failures!)')
    print('8. Check the excel output file is desired (located in Production (O):\Manufacturing Engineering\Rotor Test\Rotor Test)')

    # buffers program until key pressed
    print('\nPress any key to return to the main screen')
    getch()

# main program; user interface
def run():
    # set up
    print('\n------ROTOR TEST------')

    while True:
        # main menu - displays possible commands
        print('\n--Main Menu--')
        print('Enter a command:')
        print('\'s\' = Scan barcode & run test')
        print('\'x\' = Exit program')
        print('\'a\' = More information about the program')

        # ask for command and convert into string
        command = getch()                               # wait for user input (bytearray format)
        commandStr = command.decode()                   # convert user input to string format

        # perform command specified
        if commandStr == 's' or commandStr == 'S':      # start collecting data
            getData()
        elif commandStr == 'x' or commandStr == 'X':    # exits the program
            exit()
            break
        elif commandStr == 'a' or commandStr == 'A':    # gives information about the program
            about()
        else:
            print('ERROR: Invalid command! Please try again.')

run()
