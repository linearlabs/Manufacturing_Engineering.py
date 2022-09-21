# Controller Tester V1.0
# Linear Labs Inc
# Doug Gammill
# 3/15/22
 
from tkinter import * # handles GUI
from threading import * # handles threading so GUI doesnt freeze during main functions
import tkinter as tk # handles GUI
from PIL import Image, ImageTk # handles GUI Image
from tkinter import filedialog # handles opening Results and Config file paths
import os  # for working with opening files with applications like excel and notepad
import configparser # handles config files
import arduino # requires pyserial, sleep, configparser
import SPD3303XE # requires pyvisa, configparser
from pathlib import Path # handles (if Path(configFilePath).is_file():)
import pathlib
import pandas as pd # handles data frames
from pandas import ExcelWriter # used with saving spread sheets with sheet numbers
import openpyxl
from time import sleep # handles delay
import time # used for adding time stamps
folder = arduino.folder # save path
configFolder=arduino.configFolder # config file path
passFail = 0 # if error, use this index to skip back to main
failureMessage=''
failureMessage2=''
testIndex = 0 # if auto test is on ignore sampling

def readConfig():
    global passFail,speedRampUp,partNum,status,Throttle10,Throttle50,Throttle100,sourceMode,sourceVoltage,sourceCurrent,ch2,minI0,maxI0,minI50,maxI50,minI100,maxI100,minRPM50,maxRPM50,minRPM100,maxRPM100,minV,maxV
    # get partNum params
    configFile = partNum
    configParser = configparser.RawConfigParser()   
    configFilePath = configFolder+'/'+configFile+'.txt'
    print(configFilePath)
    
    if Path(configFilePath).is_file():
        configParser.read(configFilePath)
        
        sourceMode = configParser.get(configFile, 'sourceMode') # 1.series, 2.parallel, or 0.independent
        #print ('sourceMode='+sourceMode)
        sourceVoltage = configParser.get(configFile, 'sourceVoltage') # max 30V
        #print ('sourceVoltage='+sourceVoltage)
        sourceCurrent = configParser.get(configFile, 'sourceCurrent') # max 3.2A
        #print ('sourceCurrent='+sourceCurrent)
        ch2 = configParser.get(configFile, 'ch2') # if the second power supply is need for independent mode
        #print ('ch2='+ch2)
        if sourceMode=="0": # power supply independent mode only
            if ch2=="1": # only if ch2 is needed for independent mode
                sourceVoltage2 = configParser.get(configFile, 'sourceVoltage2') # max 30V
                #print ('sourceVoltage2='+sourceVoltage2)
                sourceCurrent2 = configParser.get(configFile, 'sourceCurrent2') # max 3.2A
                #print ('sourceCurrent2='+sourceCurrent2)

        Throttle10 = configParser.get(configFile, '10%Throttle') # throttle setting for initial power on if key is passFail
        Throttle50 = configParser.get(configFile, '50%Throttle') # throttle setting for half speed testing (0-100)
        #print(Throttle50)
        Throttle100 = configParser.get(configFile, '100%Throttle') # throttle setting for full speed testing (0-100)
        #print(Throttle100)
        speedRampUp = configParser.get(configFile, 'speedRampUp')
        
        minI0 = configParser.get(configFile, 'minI0')
        #print ('minI0='+minI0)
        maxI0 = configParser.get(configFile, 'maxI0')
        #print ('maxI0='+maxI0)
        minI50 = configParser.get(configFile, 'minI50')
        #print ('minI50='+minI50)
        maxI50 = configParser.get(configFile, 'maxI50')
        #print ('maxI50='+maxI50)
        minI100 = configParser.get(configFile, 'minI100')
        #print ('minI100='+minI100)
        maxI100 = configParser.get(configFile, 'maxI100')
        #print ('maxI100='+maxI100)
        minRPM50 = configParser.get(configFile, 'minRPM50')
        #print ('minRPM50='+minRPM50)
        maxRPM50 = configParser.get(configFile, 'maxRPM50')
        #print ('maxRPM50='+maxRPM50)
        minRPM100 = configParser.get(configFile, 'minRPM100')
        #print ('minRPM100='+minRPM100)
        maxRPM100 = configParser.get(configFile, 'maxRPM100')
        #print ('maxRPM100='+maxRPM100)
        minV = configParser.get(configFile, 'minV')
        #print ('minV='+minV)
        maxV = configParser.get(configFile, 'maxV')
        #print ('maxV='+maxV)
        
    else:
        print('ERROR: No Config File Found!')
        status = 'ERROR: No Config File Found!'
        text.config(text=status, bg='red', fg='black')
        passFail=0
        return passFail
    
def criteriaTableSheet():
    global criteriaTable,minI0,maxI0,minI50,maxI50,minI100,maxI100,minRPM50,maxRPM50,minRPM100,maxRPM100,minV,maxV
    criteriaTable=[]
    row=[]
    row.append(float(minI0))
    row.append(float(maxI0))
    row.append(float(minI50))
    row.append(float(maxI50))
    row.append(float(minI100))
    row.append(float(maxI100))
    row.append(float(minI50))
    row.append(float(maxI50))
    row.append(float(minI100))
    row.append(float(maxI100))
    criteriaTable.append(row)
    row = []
    row.append("") # key on rpm left blank
    row.append("")
    row.append(float(minRPM50))
    row.append(float(maxRPM50))
    row.append(float(minRPM100))
    row.append(float(maxRPM100))
    row.append(float(minRPM50))
    row.append(float(maxRPM50))
    row.append(float(minRPM100))
    row.append(float(maxRPM100))
    criteriaTable.append(row)
    row = []
    row.append("")
    row.append("")
    row.append('Forward')
    row.append('Forward')
    row.append('Forward')
    row.append('Forward')
    row.append('Reverse')
    row.append('Reverse')
    row.append('Reverse')
    row.append('Reverse')
    criteriaTable.append(row)
    row = []
    row.append('0.00RPM') # key off and throttle 0% check rpm
    row.append('0.00RPM')
    criteriaTable.append(row)
    row = []
    row.append('0.00RPM') # key off and throttle 10% check rpm
    row.append('0.00RPM')
    criteriaTable.append(row)
    row = []
    row.append('0.00RPM') # key on and throttle 0% check rpm
    row.append('0.00RPM')
    criteriaTable.append(row)
    row = []
    row.append(float(minV))
    row.append(float(maxV))
    criteriaTable.append(row)
    
def dataLog():
    global passFail,criteriaTable,barcode,currentOn,voltageOn,volt3V3,speed0,speed1,speed2,currentFwd50,currentFwd100,currentRev50,currentRev100,speedFwd50,speedFwd100,speedRev50,speedRev100,directionFwd50,directionFwd100,directionRev50,directionRev100,failureMessage,failureMessage2
    table=[]
    row=[]
    row.append(currentOn)
    row.append(currentFwd50)
    row.append(currentFwd100)
    row.append(currentRev50)
    row.append(currentRev100)
    table.append(row)
    row = []
    row.append("") # key on rpm left blank
    row.append(speedFwd50)
    row.append(speedFwd100)
    row.append(speedRev50)
    row.append(speedRev100)
    table.append(row)
    row = []
    row.append("") # key on direction left blank
    row.append(directionFwd50)
    row.append(directionFwd100)
    row.append(directionRev50)
    row.append(directionRev100)
    table.append(row)
    row = []
    row.append(speed0+'RPM') # key off and throttle 0% check rpm
    table.append(row)
    row = []
    row.append(speed1+'RPM') # key off and throttle 10% check rpm
    table.append(row)
    row = []
    row.append(speed2+'RPM') # key on and throttle 0% check rpm
    table.append(row)
    row = []
    row.append(volt3V3)
    table.append(row)
    row = []
    row.append(voltageOn)
    table.append(row)
    row = []
    row.append(failureMessage)
    table.append(row)
    row = []
    row.append(failureMessage2)
    table.append(row)

    criteriaTableSheet()
    
    resultsCols = ['Power On', 'Fwd 50%','Fwd 100%', 'Rev 50%', 'Rev 100%'] # column labels
    resultsIndex=['Current','RPM','Direction','KeyOff/ThrottleOff','KeyOff/Throttle10%','KeyOn/ThrottleOff','3.3V','Voltage Source','Failure1','Failure2']
    dfResults = pd.DataFrame(table, columns=resultsCols, index=resultsIndex) #index=resultsIndex) # place table into a pandas dataframe object
    criteriaCols = ['PowerOnMin', 'PowerOnMax','Fwd50Min', 'Fwd50Max', 'Fwd100Min', 'Fwd100Max','Rev50Min', 'Rev50Max', 'Rev100Min', 'Rev100Max'] # column labels
    criteriaIndex=['Current','RPM','Direction','KeyOff/ThrottleOff','KeyOff/Throttle10%','KeyOn/ThrottleOff','3.3V']
    dfCriteria = pd.DataFrame(criteriaTable, columns=criteriaCols, index=criteriaIndex) #index=resultsIndex) # place table into a pandas dataframe object
    timestr = time.strftime("(%Y%m%d-%H%M%S)") # add date time stamp and save location
    if passFail==1:
        file = barcode+timestr                                                          # file name with date time stamp
    elif passFail==0:
        file = 'Failure-'+barcode+timestr
    extension = '.xlsx'                                                             # file extension
    fullPath = pathlib.Path(os.path.join(folder, file + extension))                 # the full file path
    writer = pd.ExcelWriter(path = fullPath, engine='xlsxwriter',engine_kwargs={'options': {'strings_to_formulas': False}})
    dfResults.to_excel(writer, sheet_name='Results')
    dfCriteria.to_excel(writer, sheet_name='Criteria')
    writer.save()                                                                        

def openResults():
    filename = filedialog.askopenfilename(initialdir=folder, title="Controller Test Results",filetypes=(("xlsx files", "*.xlsx"),("all files", "*.*")))
    filename = '"'+filename+'"'
    if len(filename) >=3:
        path = str('start '+ "excel " + filename)
        os.system(path)
        
def openConfig():
    configFile = filedialog.askopenfilename(initialdir=configFolder, title="Controller Config Files",filetypes=(("txt files", "*.txt"),("all files", "*.*")))
    configFile = '"'+configFile+'"'
    if len(configFile) >=3:
        path = str('start '+ "notepad " + configFile)
        os.system(path)
        
def failure():
    global failureMessage,failureMessage2
    fail = tk.Tk()
    fail.title("Failure!!!")
    fail.rowconfigure(3, minsize=50, weight=1)       #about window row#, size, wieght
    fail.columnconfigure(2, minsize=100, weight=1)    #main window col#, size, wieght
    fail.geometry('610x110')
    fail.wm_iconbitmap('icon.ico')
    fail.config(bg='red')

    def reset():
        text.config(fg="black",bg='#3399ff',width=25,font=16, text='Please Enter Barcode Bellow')
        fail.destroy()
        

    failLabel = tk.Label(fail, fg="black",bg='red',width=50, font=("Adobe",16), text=failureMessage)
    failLabel.grid(row=0, columnspan=1)
    
    failLabel2 = tk.Label(fail, fg="black",bg="red",width=50, font=("Adobe",16), text=failureMessage2)
    failLabel2.grid(row=1, columnspan=1)
    
    btn_ok = tk.Button(fail, font=("Adobe",16),width=10, text="OK", command=reset)
    btn_ok.grid(row=2, columnspan=1)
      
    fail.mainloop()

def usbFailure():
    global failureMessage,failureMessage2
    failUSB = tk.Tk()
    failUSB.title("Failure!!!")
    failUSB.rowconfigure(4, minsize=50, weight=1)       #about window row#, size, wieght
    failUSB.columnconfigure(2, minsize=100, weight=1)    #main window col#, size, wieght
    failUSB.geometry('610x140')
    failUSB.wm_iconbitmap('icon.ico')
    failUSB.config(bg='red')
    failLabel = tk.Label(failUSB, fg="black",bg='red',width=50, font=("Adobe",16), text=failureMessage)
    failLabel.grid(row=0, columnspan=1)
    
    failLabel2 = tk.Label(failUSB, fg="black",bg="red",width=50, font=("Adobe",16), text=failureMessage2)
    failLabel2.grid(row=1, columnspan=1)
    
    failLabel3 = tk.Label(failUSB, fg="black",bg="red",width=50, font=("Adobe",16), text="Check USB Connection and restart GUI")
    failLabel3.grid(row=2, columnspan=1)
    text.config(text='USB Failed, Please restart GUI', bg = 'red')

    def destroy():
        failUSB.destroy()
        gui.destroy()

    btn_ok = tk.Button(failUSB, font=("Adobe",16),width=10, text="OK", command=destroy)
    btn_ok.grid(row=3, columnspan=1)
    failUSB.mainloop()
    
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
    Controller Tester GUI
    Author: Doug Gammill
    Date: 3/15/2022
    Copyright (c) 2022
    Linear Labs, Inc.
    Tests Motor Controllers at board level or final assembly.
    Full function testing.
    Current drawl, inputs, outputs, speed, and direction.
    General Test Procedure:
    1. Turn on Controller Tester, and SPD3303X-E (power supply).
    2. Ensure all USB cables for each device are connected to the PC
    3. Ensure Linear Labs Controller Tester computer application (gui) has indicated USB coms are good with each device.
    4. Connect the desired part to the test fixture. Make sure to use the correct cable adapters for the part(s).
    5. Scan the barcode located on the boards or on the final assembly using the barcode scanner.
    6. Confirm part number selected is correct
    7. Confirm that there are no failure(s) for the part by reading the label outputs.
    8. Check the excel output file if desired by clicking the 'Results' button on the GUI.
    '''
    text_box = Text(window,height=23,width=95, font=("Adobe",16))
    text_box.pack(expand=True)
    text_box.insert('end', message)
    text_box.config(state='disabled')
    window.mainloop()
    
def connectArduino():
    global passFail,failureMessage
    arduino.connectArduino() # connects to arduino through arduino module
    if arduino.passFail==1:
        passFail=1
        failureMessage="Controller Tester USB Failed Connection"
        usb1.config(bg='red')
    else:
        usb1.config(bg='purple')
        
def connectPowerSupply():
    global passFail,failureMessage2
    SPD3303XE.connectPowerSupply()# connects to SPD3303XE through SPD3303XE module
    if SPD3303XE.passFail==1:
        usb2.config(bg='red')
        passFail=1
        failureMessage2="Power Supply USB Failed Connection"
    else:
        usb2.config(bg='purple')
        

def startPowerSupply():
    global passFail,minI0,maxI0,sourceMode,img1,currentOn,voltageOn,failureMessage,failureMessage2
    if sourceMode=='ser':
        SPD3303XE.serMode()
    if sourceMode=='par':
        SPD3303XE.parMode()
    if sourceMode=='ind':
        SPD3303XE.indMode()
    SPD3303XE.ch1RampVolt(sourceVoltage, sourceCurrent) # ramps power suppy and auto shut-off if overcurrent
    pSupplyMessage=SPD3303XE.result
    if pSupplyMessage=='Good':
        currentOn=SPD3303XE.current
        voltage1=SPD3303XE.voltageCh1 # measures actual voltage ch1
        voltage2=SPD3303XE.voltageCh2 # measures actual voltage ch2
        totalVoltage=float(voltage1)+float(voltage2)
        totalVoltage='{:2.2f}'.format(totalVoltage)
        voltageOn=str(totalVoltage)
        print(currentOn+'A')
        current=float(currentOn) # current reading at full power
        currentMin=float(minI0) # pass fail criteria
        currentMax=float(maxI0) # pass fail criteria
        if (current <= currentMax and current >= currentMin):
            img1=Label(gui, borderwidth=0, image=renderCheck)
            img1.grid(row=4, column=1)
        if (current > currentMax):
            failureMessage='HighCurrent, '+ currentOn+'A'
            text.config(text=failureMessage, bg='red', fg='black')
            img1=Label(gui, borderwidth=0, image=renderX)
            img1.grid(row=4, column=1)
            passFail=0
        if (current < currentMin):
            failureMessage='LowCurrent, '+ currentOn+'A'
            text.config(text=failureMessage, bg='red', fg='black')
            img1=Label(gui, borderwidth=0, image=renderX)
            img1.grid(row=4, column=1)
            passFail=0
    if pSupplyMessage=='OverCurrent':
        currentOn=SPD3303XE.current
        voltage1=SPD3303XE.voltageCh1 # measures actual voltage ch1
        voltage2=SPD3303XE.voltageCh2 # measures actual voltage ch2
        totalVoltage=float(voltage1)+float(voltage2)
        totalVoltage='{:2.2f}'.format(totalVoltage)
        voltageOn=str(totalVoltage)
        failureMessage=pSupplyMessage+', '+currentOn+'A, '+voltageOn+'V'
        failureMessage2='Voltage rampup failed, possible short' 
        text.config(text=failureMessage, bg='red', fg='black')
        img1 = Label(gui, borderwidth=0, image=renderX)
        img1.grid(row=4, column=1)
        passFail=0
        
def checkKeyThrottle3V3():
    global passFail,Throttle10,minV,maxV,img2,img3,img4,img5,img6,speed0,speed1,speed2,volt3V3,failureMessage, failureMessage2
    minV=float(minV)
    maxV=float(maxV)
    arduino.command('keys:0')# make sure key is set to off
    arduino.command('spee:0')# make sure speed is set to 0
    arduino.command('frwd:') # make sure frwd
    arduino.command('spee?') # initially check speed *if no speed then no direction
    speed0=arduino.result
    print(speed0+'RPM')

    if speed0 == '0.00':
        arduino.command('spee:'+Throttle10) # set speed to check key
        sleep(.5)
        arduino.command('spee?')
        speed1=arduino.result
        print(speed1+'RPM')
    else:
        failureMessage='Failure: Key & Throttle'
        failureMessage2='RPM detected when none expected'
        text.config(text=failureMessage, bg='red', fg='black')
        img4 = Label(gui, borderwidth=0, image=renderX)
        img4.grid(row=7, column=1)
        img5 = Label(gui, borderwidth=0, image=renderX)
        img5.grid(row=8, column=1)
        passFail=0
    
    if passFail==1:
        # check Throttle
        if speed1 == '0.00':
            arduino.command('spee:0') # set speed back to 0
            arduino.command('keys:1') # set key on to check throttle and leave on for further testing
            sleep(.5)
            arduino.command('spee?') # initially check speed *if no speed then no direction
            speed2=arduino.result
            print(speed2+'RPM')
        else:
            failureMessage='Failure: Key'
            failureMessage2='Key logic stuck'
            text.config(text=failureMessage, bg='red', fg='black')
            img4 = Label(gui, borderwidth=0, image=renderX)
            img4.grid(row=7, column=1)
            passFail=0
            
    if passFail==1:
        if speed2 == '0.00': # throttle
            img2=Label(gui, borderwidth=0, image=renderCheck)
            img2.grid(row=5, column=1)
            img3=Label(gui, borderwidth=0, image=renderCheck)
            img3.grid(row=6, column=1)
            img4=Label(gui, borderwidth=0, image=renderCheck)
            img4.grid(row=7, column=1)
            img5=Label(gui, borderwidth=0, image=renderCheck)
            img5.grid(row=8, column=1)
            arduino.command('volt?')
            volt3V3=arduino.result
            print(volt3V3+'V')
            volt3=float(volt3V3)
        else:
            failureMessage='Failure: Throttle'
            failureMessage2='Throttle voltage not held low'
            text.config(text=failureMessage, bg='red', fg='black')
            img5 = Label(gui, borderwidth=0, image=renderX)
            img5.grid(row=8, column=1)
            passFail=0
    if passFail==1:
        if (volt3 <= maxV) and (volt3 >= minV): # check 3V3 pGood
            img6=Label(gui, borderwidth=0, image=renderCheck)
            img6.grid(row=9, column=1)

        elif (volt3 > maxV):
            failureMessage='Fail: 3.3V High, '+ volt3V3+'V'
            text.config(text=failureMessage, bg='red', fg='black')
            img6=Label(gui, borderwidth=0, image=renderX)
            img6.grid(row=9, column=1)
            passFail=0
      
        elif (volt3 < minV):
            failureMessage='Fail: 3.3V Low, '+ volt3V3+'V'
            text.config(text=failureMessage, bg='red', fg='black')
            img6=Label(gui, borderwidth=0, image=renderX)
            img6.grid(row=9, column=1)
            passFail=0
                    
def checkFwd50():
    global passFail,Throttle50,minI50,maxI50,minRPM50,maxRPM50,img7,img8,img9,currentFwd50,speedFwd50,directionFwd50,failureMessage,failureMessage2
    minI50=float(minI50)
    maxI50=float(maxI50)
    minRPM50=float(minRPM50)
    maxRPM50=float(maxRPM50)
    arduino.command('spee:'+Throttle50) # set throttle back to Zero
    sleep(3)
    
    SPD3303XE.ch1MeasureCurrent()
    currentFwd50=SPD3303XE.result
    print(currentFwd50+'A')
    current=float(currentFwd50)

    if (current <= maxI50) and (current >= minI50):
        img7=Label(gui, borderwidth=0, image=renderCheck)
        img7.grid(row=4, column=2)
        
    elif (current > maxI50):
        failureMessage='Current High, '+ currentFwd50+'A'
        text.config(text=failureMessage, bg='red', fg='black')
        img7=Label(gui, borderwidth=0, image=renderX)
        img7.grid(row=4, column=2)
        passFail=0
        
    elif (current < minI50):
        failureMessage='Current Low, '+ currentFwd50+'A'
        text.config(text=failureMessage, bg='red', fg='black')
        img7=Label(gui, borderwidth=0, image=renderX)
        img7.grid(row=4, column=2)
        passFail=0
        
    arduino.command('spee?') # initially check speed *if no speed then no direction
    speedFwd50=arduino.result
    print(speedFwd50+'RPM')
    speed=float(speedFwd50)

    if (speed <= maxRPM50) and (speed >= minRPM50):
        img8=Label(gui, borderwidth=0, image=renderCheck)
        img8.grid(row=5, column=2)
    
    elif (speed > maxRPM50):
        failureMessage2='Speed High, '+ speedFwd50+'RPM'
        text.config(text=failureMessage2, bg='red', fg='black')
        img8=Label(gui, borderwidth=0, image=renderX)
        img8.grid(row=5, column=2)
        passFail=0
        
    elif (speed < minRPM50):
        failureMessage2='Speed Low, '+ speedFwd50+'RPM'
        text.config(text=failureMessage2, bg='red', fg='black')
        img8=Label(gui, borderwidth=0, image=renderX)
        img8.grid(row=5, column=2)
        passFail=0
    if passFail==1:
        arduino.command('dire?') # initially check speed *if no speed then no direction
        directionFwd50=arduino.result
        directionFwd50=str(directionFwd50)
        print(directionFwd50)
        if directionFwd50 == 'Forward':
            img9=Label(gui, borderwidth=0, image=renderCheck)
            img9.grid(row=6, column=2)
        else:
            failureMessage='Failure: Direction='+ directionFwd50
            text.config(text=failureMessage, bg='red', fg='black')
            img9=Label(gui, borderwidth=0, image=renderX)
            img9.grid(row=6, column=2)
            passFail=0
            
def checkFwd100():
    global passFail,Throttle100,minI100,maxI100,minRPM100,maxRPM100,img10,img11,img12,currentFwd100,speedFwd100,directionFwd100,failureMessage,failureMessage2
    minI100=float(minI100)
    maxI100=float(maxI100)
    minRPM100=float(minRPM100)
    maxRPM100=float(maxRPM100)
    arduino.command('spee:'+Throttle100) # set throttle back to Zero
    sleep(3)
    SPD3303XE.ch1MeasureCurrent()
    currentFwd100=SPD3303XE.result
    print(currentFwd100+'A')
    current=float(currentFwd100)
    if (current <= maxI100) and (current >= minI100):
        img10=Label(gui, borderwidth=0, image=renderCheck)
        img10.grid(row=4, column=3)
        
    elif (current > maxI100):
        failureMessage='Current High, '+ currentFwd100+'A'
        text.config(text=failureMessage, bg='red', fg='black')
        img10=Label(gui, borderwidth=0, image=renderX)
        img10.grid(row=4, column=3)
        passFail=0
        
    elif (current < minI100):
        failureMessage='Current Low, '+ currentFwd100+'A'
        text.config(text=failureMessage, bg='red', fg='black')
        img10=Label(gui, borderwidth=0, image=renderX)
        img10.grid(row=4, column=3)
        passFail=0

    arduino.command('spee?') # initially check speed *if no speed then no direction
    speedFwd100=arduino.result
    print(speedFwd100+'RPM')
    speed=float(speedFwd100)
    
    if (speed <= maxRPM100) and (speed >= minRPM100):
        img11=Label(gui, borderwidth=0, image=renderCheck)
        img11.grid(row=5, column=3)
    
    elif (speed > maxRPM100):
        failureMessage2='Speed High, '+ speedFwd100+'RPM'
        text.config(text=failureMessage2, bg='red', fg='black')
        img11=Label(gui, borderwidth=0, image=renderX)
        img11.grid(row=5, column=3)
        passFail=0
        
    elif (speed < minRPM100):
        failureMessage2='Speed Low, '+ speedFwd100+'RPM'
        text.config(text=failureMessage2, bg='red', fg='black')
        img11=Label(gui, borderwidth=0, image=renderX)
        img11.grid(row=5, column=3)
        passFail=0
    if passFail==1:    
        arduino.command('dire?') # initially check speed *if no speed then no direction
        directionFwd100=arduino.result
        directionFwd100=str(directionFwd100)
        print(directionFwd100)
        if directionFwd100 == 'Forward':
            img12=Label(gui, borderwidth=0, image=renderCheck)
            img12.grid(row=6, column=3)
        else:
            failureMessage='Failure: Direction='+directionFwd100
            text.config(text=failureMessage, bg='red', fg='black')
            img12=Label(gui, borderwidth=0, image=renderX)
            img12.grid(row=6, column=3)
            passFail=0

def checkRev50():
    global passFail,Throttle50,minI50,maxI50,minRPM50,maxRPM50,img13,img14,img15,currentRev50,speedRev50,directionRev50,failureMessage,failureMessage2
    minI50=float(minI50)
    maxI50=float(maxI50)
    minRPM50=float(minRPM50)
    maxRPM50=float(maxRPM50)
    arduino.command('spee:'+Throttle50) # set throttle back to Zero
    sleep(3)
    SPD3303XE.ch1MeasureCurrent()
    currentRev50=SPD3303XE.result
    print(currentRev50+'A')
    current=float(currentRev50)
    if (current <= maxI50) and (current >= minI50):
        img13=Label(gui, borderwidth=0, image=renderCheck)
        img13.grid(row=4, column=4)
        
    elif (current > maxI50):
        failureMessage='Current High, '+ currentRev50+'A'
        text.config(text=failureMessage, bg='red', fg='black')
        img13=Label(gui, borderwidth=0, image=renderX)
        img13.grid(row=4, column=4)
        passFail=0
        
    elif (current < minI50):
        failureMessage='Current Low, '+ currentRev50+'A'
        text.config(text=failureMessage, bg='red', fg='black')
        img13=Label(gui, borderwidth=0, image=renderX)
        img13.grid(row=4, column=4)
        passFail=0
    
    arduino.command('spee?') # initially check speed *if no speed then no direction
    speedRev50=arduino.result
    print(speedRev50+'RPM')
    speed=float(speedRev50)

    if (speed <= maxRPM50) and (speed >= minRPM50):
        img14=Label(gui, borderwidth=0, image=renderCheck)
        img14.grid(row=5, column=4)

    elif (speed> maxRPM50):
        failureMessage2='Speed High, '+speedRev50+'RPM'
        text.config(text=failureMessage2, bg='red', fg='black')
        img14=Label(gui, borderwidth=0, image=renderX)
        img14.grid(row=5, column=4)
        passFail=0
        
    elif (speed < minRPM50):
        failureMessage2='Speed Low, '+ speedRev50+'RPM'
        text.config(text=failureMessage2, bg='red', fg='black')
        img14=Label(gui, borderwidth=0, image=renderX)
        img14.grid(row=5, column=4)
        passFail=0
        
    if passFail==1:   
        arduino.command('dire?') # initially check speed *if no speed then no direction
        directionRev50=arduino.result
        directionRev50=str(directionRev50)
        print(directionRev50)
        if directionRev50 == 'Reverse':
            img15=Label(gui, borderwidth=0, image=renderCheck)
            img15.grid(row=6, column=4)
        else:
            failureMessage='Failure: Direction=' +directionRev50
            text.config(text=failureMessage, bg='red', fg='black')
            img15=Label(gui, borderwidth=0, image=renderX)
            img15.grid(row=6, column=4)
            passFail=0
        
def checkRev100():
    global passFail,Throttle100,minI100,maxI100,minRPM100,maxRPM100,img16,img17,img18,currentRev100,speedRev100,directionRev100,failureMessage,failureMessage2
    minI100=float(minI100)
    maxI100=float(maxI100)
    minRPM100=float(minRPM100)
    maxRPM100=float(maxRPM100)
    arduino.command('spee:'+Throttle100) # set throttle back to Zero
    sleep(3)
    SPD3303XE.ch1MeasureCurrent()
    currentRev100=SPD3303XE.result
    print(currentRev100+'A')
    current=float(currentRev100)
    if (current <= maxI100) and (current >= minI100):
        img16=Label(gui, borderwidth=0, image=renderCheck)
        img16.grid(row=4, column=5)
        
    elif (current > maxI100):
        failureMessage='Current High, '+ currentRev100+'A'
        text.config(text=failureMessage, bg='red', fg='black')
        img16=Label(gui, borderwidth=0, image=renderX)
        img16.grid(row=4, column=5)
        passFail=0
        
    elif (current < minI100):
        failureMessage='Current Low, '+ currentRev100+'A'
        text.config(text=failureMessage, bg='red', fg='black')
        img16=Label(gui, borderwidth=0, image=renderX)
        img16.grid(row=4, column=5)
        passFail=0
 
    arduino.command('spee?') # initially check speed *if no speed then no direction
    speedRev100=arduino.result
    print(speedRev100+'RPM')
    speed=float(speedRev100)
    
    if (speed <= maxRPM100) and (speed >= minRPM100):
        img17=Label(gui, borderwidth=0, image=renderCheck)
        img17.grid(row=5, column=5)
    
    elif (speed > maxRPM100):
        failureMessage2='Speed High, '+ speedRev100+'RPM'
        text.config(text=failureMessage2, bg='red', fg='black')
        img17=Label(gui, borderwidth=0, image=renderX)
        img17.grid(row=5, column=5)
        passFail=0
        
    elif (speed < minRPM100):
        failureMessage2='Speed Low, '+ speedRev100+'RPM'
        text.config(text=failureMessage2, bg='red', fg='black')
        img17=Label(gui, borderwidth=0, image=renderX)
        img17.grid(row=5, column=5)
        passFail=0
        
    if passFail==1:       
        arduino.command('dire?') 
        directionRev100=arduino.result
        directionRev100=str(directionRev100)
        print(directionRev100)
        if directionRev100 == 'Reverse':
            img18=Label(gui, borderwidth=0, image=renderCheck)
            img18.grid(row=6, column=5)
        else:
            failureMessage='Failure: Direction='+directionRev100
            text.config(text=failureMessage, bg='red', fg='black')
            img18=Label(gui, borderwidth=0, image=renderX)
            img18.grid(row=6, column=5)
            passFail=0
        
def checkSample():
    global testIndex
    if testIndex==0:
        arduino.command('print') # send command to arduino
        arduinoMessage=arduino.result # read response from arduino
        text.config(text=arduinoMessage, bg='blue', fg='white')
    else:
        text.config(text="please wait for automated test to complete", bg='blue', fg='white')
    
def checkAutoMode(): # check if arduinoAutoMode=1
    global passFail, status
    arduino.command('mode?')
    arduinoMessage=arduino.result
    if arduinoMessage=='1': # check if arduinoAutoMode=1
        text.config(fg="black",bg='yellow',width=25,font=16, text=status) # if correct mode, do nothing but update status
    else:
        print('ERROR: Set Manual Switch to Auto & Please Scan Again.')
        status='Error: Set Manual Switch to Auto & Please Scan Again.'
        text.config(fg="black",bg='red',width=25,font=16, text=status)
        barcode_var.set('')
        passFail=0
        return passFail
    
def getBarcodeInfo(): # event is used for gui entry .bind <return>
    global barcode, partNum, sn, passFail, status
    try:
        barcode=barcode_var.get()
        print(barcode)                                                
        if len(barcode.split('-')) == 4: # check if the barcode is the correct length/format
            first, second, third, sn = barcode.split('-') # put barcode into list of strings
            partNum=first+'-'+second+'-'+third
            status='Testing: '+partNum
            text.config(fg="black",bg='Yellow',width=25,font=16, text=status)
            barcode_var.set('')
        else:
            raise ValueError # if wrong format, ask to scan again
    except ValueError:
        print('ERROR: Invalid barcode! Please scan again.')
        status='Error: Invalid Barcode! Please Scan Again.'
        text.config(fg="black",bg='red',width=25,font=16, text=status)
        barcode_var.set('')
        passFail=0
        return passFail
    

# Driver code 
#if __name__ == "__main__":
# create a GUI window
gui = Tk()
for i in range(10):  ###rows = 10
    gui.columnconfigure(i, weight=1, minsize=100)
    gui.rowconfigure(i, weight=1, minsize=60)

    for j in range(0, 5): ###column = 6
        frame = tk.Frame(
            master=gui,
            relief=tk.RAISED,
            borderwidth=1
        )

# set the background colour of GUI window
gui.configure(background="Black")

# set the title of GUI window
gui.title("Controller Tester")
gui.wm_iconbitmap('icon.ico')

text_var = tk.StringVar()
text=tk.Label(gui, font=(12), relief="ridge", text='Setting Up USB, Please Wait', borderwidth=10)
text.grid(row=1, columnspan=6, ipadx=100)
text.update()

# set the configuration of GUI window
gui.geometry("600x700")
gui.resizable(width=True, height=True)

def resetGui():
    global img1,img2,img3,img4,img5,img6,img7,img8,img9,img10,img11,img12,img13,img14,img15,img16,img17,img18,currentOn,voltageOn,volt3V3,speed0,speed1,speed2,currentFwd50,currentFwd100,currentRev50,currentRev100,speedFwd50,speedFwd100,speedRev50,speedRev100,directionFwd50,directionFwd100,directionRev50,directionRev100,failureMessage,failureMessage2,status
    
    img1.destroy()
    img2.destroy()
    img3.destroy()
    img4.destroy()
    img5.destroy()
    img6.destroy()
    img7.destroy()
    img8.destroy()
    img9.destroy()
    img10.destroy()
    img11.destroy()
    img12.destroy()
    img13.destroy()
    img14.destroy()
    img15.destroy()
    img16.destroy()
    img17.destroy()
    img18.destroy()
    currentOn=''
    currentFwd50=''
    currentFwd100=''
    currentRev50=''
    currentRev100=''
    speedFwd50=''
    speedFwd100=''
    speedRev50=''
    speedRev100=''
    directionFwd50=''
    directionFwd100=''
    directionRev50=''
    directionRev100=''
    voltageOn=''
    volt3V3=''
    speed0=''
    speed1=''
    speed2=''
    failureMessage=''
    failureMessage2=''
    status=''
    
def threading(event): # threading used to execute main functions and allow GUI main loop to not freeze
    t1=Thread(target=mainFunctions)
    t1.start()   

def mainFunctions(): # main multi threaded functions
    global passFail, testIndex, failureMessage,failureMessage2,status,speedRampUp
    passFail=1
    testIndex = 1
    resetGui()
    getBarcodeInfo()
    if passFail==1:
        checkAutoMode() # check to make sure tester is in the correct operating mode
    if passFail==1:
        arduino.command('mode:1') #tells arduino to not go into manual mode during test
        readConfig() # read variables from config file
        arduino.command('ramp:'+speedRampUp)
    if passFail==1:
        startPowerSupply() # ramps up voltage to check for shorts
    if passFail==1:
        checkKeyThrottle3V3()
    if passFail==1:
        checkFwd50()
    if passFail==1:
        checkFwd100()
    if passFail==1:
        arduino.command('spee:0')
        sleep(3) # allow motor to ramp down
        arduino.command('rvrs:')
        checkRev50()
    if passFail==1:
        checkRev100()
        status=''
    arduino.command('spee:0')
    arduino.command('keys:0')
    SPD3303XE.ch1Off()
    arduino.command('ramp:30') # sets arduino speed ramp back to default
    arduino.command('mode:0') # tells arduino its ok to go into manual mode now
    if passFail==1:
        if status=='':
            dataLog()
    if passFail==1:
        text.config(text='Test Passed Please Enter Barcode Bellow', bg = '#3399ff')
    elif passFail==0:
        if failureMessage !='' or failureMessage2 !='':
            failure()
            dataLog()
    testIndex = 0
    return

barcode_var = tk.StringVar() 
expression_field = tk.Entry(gui, font=(12), relief="groove", textvariable=barcode_var, borderwidth=10)
expression_field.grid(row=2, column=0, columnspan=6, ipadx=100)
expression_field.bind('<Return>',threading)
expression_field.icursor('end')
expression_field.update()


about= Button(gui, text='About', font='12', fg='black', bg='#3399ff', borderwidth=10, command=about, height=2, width=16)
about.grid(row=0, column=0)
about.update()

results= Button(gui, text='Results', font='12', fg='black', bg='#3399ff', borderwidth=10,command=openResults, height=2, width=16)
results.grid(row=0, column=1)
results.update()

config= Button(gui, text='Config', font='12', fg='black', bg='#3399ff', borderwidth=10,command=openConfig,height=2, width=16)
config.grid(row=0, column=2)
config.update()

usb1=tk.Label(gui, text="Test.USB", height=3, width=16, font='12', fg='black', bg='white', relief="groove", borderwidth=2)
usb1.grid(row=0, column=3)
usb1.update()
usb2=tk.Label(gui, text="PWR.USB", height=3, width=16, font='12', fg='black', bg='white', relief="groove", borderwidth=2)
usb2.grid(row=0, column=4)
usb2.update()

sample= Button(gui, text='Sample', font='12', fg='black', bg='#3399ff', borderwidth=10,command=checkSample,height=2, width=16)
sample.grid(row=0, column=5)
sample.update()

test=tk.Label(gui, text="Test:", height=3, width=16, font="Verdana 12 underline", fg='white', bg='blue', relief="groove")
test.grid(row=3, column=0)
test.update()
powerOn=tk.Label(gui, text="Fwd On", height=3, width=16, font="Verdana 12 underline", fg='white', bg='blue', relief="groove")
powerOn.grid(row=3, column=1)
powerOn.update()
quarterSpeed=tk.Label(gui, text="Fwd 50%", height=3, width=16, font="Verdana 12 underline", fg='white', bg='blue', relief="groove")
quarterSpeed.grid(row=3, column=2)
quarterSpeed.update()
halfSpeed=tk.Label(gui, text="Fwd 100%", height=3, width=16, font="Verdana 12 underline", fg='white', bg='blue', relief="groove")
halfSpeed.grid(row=3, column=3)
halfSpeed.update()
fullSpeed=tk.Label(gui, text="Rev 50%", height=3, width=16, font="Verdana 12 underline", fg='white', bg='blue', relief="groove")
fullSpeed.grid(row=3, column=4)
fullSpeed.update()
reverse=tk.Label(gui, text="Rev 100%", height=3, width=16, font="Verdana 12 underline", fg='white', bg='blue', relief="groove")
reverse.grid(row=3, column=5)
reverse.update()
current=tk.Label(gui, text="Amps", height=3, width=16, font='12', fg='black', bg='#3399ff', relief="groove")
current.grid(row=4, column=0)
current.update()
forward=tk.Label(gui, text="Speed", height=3, width=16, font='12', fg='black', bg='#3399ff', relief="groove")
forward.grid(row=5, column=0)
forward.update()
speed = tk.Label(gui, text="Direction", height=3, width=16, font='12', fg='black', bg='#3399ff', relief="groove")
speed.grid(row=6, column=0)
speed.update()
key = tk.Label(gui, text="Key", height=3, width=16, font='12', fg='black', bg='#3399ff', relief="groove")
key.grid(row=7, column=0)
key.update()
throttle = tk.Label(gui, text="Throttle", height=3, width=16, font='12', fg='black', bg='#3399ff', relief="groove")
throttle.grid(row=8, column=0)
throttle.update()
pGood = tk.Label(gui, text="3.3V", height=3, width=16, font='12', fg='black', bg='#3399ff', relief="groove")
pGood.grid(row=9, column=0)
pGood.update()

####IMG####
load= Image.open("logo4.ppm")
render = ImageTk.PhotoImage(load)
img = Label(gui, borderwidth=0, image=render)
img.grid(row=10, columnspan=6)
img.update()

load= Image.open("motorIcon.png")
render2 = ImageTk.PhotoImage(load)

img1=Label(gui, borderwidth=0, image=render2)
img1.grid(row=4, column=1)
img2=Label(gui, borderwidth=0, image=render2)
img2.grid(row=5, column=1)
img3=Label(gui, borderwidth=0, image=render2)
img3.grid(row=6, column=1)
img4=Label(gui, borderwidth=0, image=render2)
img4.grid(row=7, column=1)
img5=Label(gui, borderwidth=0, image=render2)
img5.grid(row=8, column=1)
img6=Label(gui, borderwidth=0, image=render2)
img6.grid(row=9, column=1)
img7=Label(gui, borderwidth=0, image=render2)
img7.grid(row=4, column=2)
img8=Label(gui, borderwidth=0, image=render2)
img8.grid(row=5, column=2)
img9=Label(gui, borderwidth=0, image=render2)
img9.grid(row=6, column=2)
img10=Label(gui, borderwidth=0, image=render2)
img10.grid(row=4, column=3)
img11=Label(gui, borderwidth=0, image=render2)
img11.grid(row=5, column=3)
img12=Label(gui, borderwidth=0, image=render2)
img12.grid(row=6, column=3)
img13=Label(gui, borderwidth=0, image=render2)
img13.grid(row=4, column=4)
img14=Label(gui, borderwidth=0, image=render2)
img14.grid(row=5, column=4)
img15=Label(gui, borderwidth=0, image=render2)
img15.grid(row=6, column=4)
img16=Label(gui, borderwidth=0, image=render2)
img16.grid(row=4, column=5)
img17=Label(gui, borderwidth=0, image=render2)
img17.grid(row=5, column=5)
img18=Label(gui, borderwidth=0, image=render2)
img18.grid(row=6, column=5)


load= Image.open("Red-X.ppm")
renderX = ImageTk.PhotoImage(load)

load= Image.open("Blue-Check1.ppm")
renderCheck = ImageTk.PhotoImage(load)

connectArduino()
connectPowerSupply()
if passFail==1:
    usbFailure()
else:
    text.config(text='Please Enter Barcode Bellow', bg = '#3399ff')

gui.mainloop() # start the GUI
