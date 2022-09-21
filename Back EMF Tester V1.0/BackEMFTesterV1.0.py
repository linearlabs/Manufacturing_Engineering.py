#import pyvisa as visa
#import matplotlib.pyplot as pl
import SDS1104XE # handles Oscope
from tkinter import * # handles GUI
from threading import * # handles threading so GUI doesnt freeze during main functions
import tkinter as tk # handles GUI
from PIL import Image, ImageTk # handles GUI Image
from tkinter import filedialog # handles opening Results and Config file paths
import os  # for working with opening files with applications like excel and notepad
import configparser # handles config files
from pathlib import Path # handles (if Path(configFilePath).is_file():)
import pathlib
import pandas as pd # handles data frames
from pandas import ExcelWriter # used with saving spread sheets with sheet numbers
import openpyxl
from time import sleep # handles delay
import time # used for adding time stamps
import matplotlib.pyplot as plt # used to show and save plots,graphs and charts
configFolder=SDS1104XE.configFolder # config file path
folder = SDS1104XE.folder # save path
passFail = 0 # if error, use this index to skip back to main
saveIndex=0
barcode=''

def readConfig():
    global partNum,configFolder,startSpeedTimeOut,skipFail,speedMin,speedMax,aVrmsMin,aVrmsMax,bVrmsMin,bVrmsMax,cVrmsMin,cVrmsMax,abPhaseMin,abPhaseMax,acPhaseMin,acPhaseMax,bcPhaseMin,bcPhaseMax,aHallPhaseMin,aHallPhaseMax,aHallDutyMin,aHallDutyMax,bHallDutyMin,bHallDutyMax,cHallDutyMin,cHallDutyMax,aHallVoltMin,aHallVoltMax,bHallVoltMin,bHallVoltMax,cHallVoltMin,cHallVoltMax,abHallMin,abHallMax,acHallMin,acHallMax,bcHallMin,bcHallMax
    # get partNum params
    configParser = configparser.RawConfigParser()   
    configFilePath = configFolder+'/'+partNum+'.txt'
    print(configFilePath)
    
    if Path(configFilePath).is_file():
        configParser.read(configFilePath)

        startSpeedTimeOut = configParser.get(partNum, 'startSpeedTimeOut')
        startSpeedTimeOut=int(startSpeedTimeOut)

        skipFail = configParser.get(partNum, 'skipFail')
        skipFail=int(skipFail)
        
        speedMin = configParser.get(partNum, 'speedMin') # hallA minimum speed
        #print ('speedMin='+speedMin )
        speedMin=float(speedMin)
        
        speedMax = configParser.get(partNum, 'speedMax') # hallA max speed
        #print ('speedMax='+speedMax )
        speedMax=float(speedMax)
        
        aVrmsMin = configParser.get(partNum, 'aVrmsMin') # phaseA Vrms minimum
        #print ('aVrmsMin='+aVrmsMin )
        aVrmsMin=float(aVrmsMin)
        
        aVrmsMax = configParser.get(partNum, 'aVrmsMax') # phaseA Vrms maximum 
        #print ('aVrmsMax='+aVrmsMax)
        aVrmsMax=float(aVrmsMax)
        
        bVrmsMin = configParser.get(partNum, 'bVrmsMin') # phaseB Vrms minimum
        #print ('bVrmsMin='+bVrmsMin)
        bVrmsMin=float(bVrmsMin)
        
        bVrmsMax = configParser.get(partNum, 'bVrmsMax') # phaseB Vrms maximum
        #print ('bVrmsMax='+bVrmsMax)
        bVrmsMax=float(bVrmsMax)
        
        cVrmsMin = configParser.get(partNum, 'cVrmsMin') # phaseC Vrms minimum
        #print ('cVrmsMin='+cVrmsMin)
        cVrmsMin=float(cVrmsMin)
        
        cVrmsMax = configParser.get(partNum, 'cVrmsMax') # phaseC Vrms maximum
        #print ('cVrmsMax='+cVrmsMax)
        cVrmsMax=float(cVrmsMax)
        
        abPhaseMin = configParser.get(partNum, 'abPhaseMin') # AB phase to phase offset in degrees min
        #print ('abPhaseMin='+abPhaseMin)
        abPhaseMin=float(abPhaseMin)
        
        abPhaseMax = configParser.get(partNum, 'abPhaseMax') # AB phase to phase offset in degrees max
        #print ('abPhaseMax='+abPhaseMax)
        abPhaseMax=float(abPhaseMax)
        
        acPhaseMin = configParser.get(partNum, 'acPhaseMin') # AC phase to phase offset in degrees min
        #print ('acPhaseMin='+acPhaseMin)
        acPhaseMin=float(acPhaseMin)
        
        acPhaseMax = configParser.get(partNum, 'acPhaseMax') # AC phase to phase offset in degrees max
        #print ('acPhaseMax='+acPhaseMax)
        acPhaseMax=float(acPhaseMax)
        
        bcPhaseMin = configParser.get(partNum, 'bcPhaseMin') # BC phase to phase offset in degrees min
        #print ('bcPhaseMin='+bcPhaseMin)
        bcPhaseMin=float(bcPhaseMin)
        
        bcPhaseMax = configParser.get(partNum, 'bcPhaseMax') # BC phase to phase offset in degrees max
        #print ('bcPhaseMax='+bcPhaseMax)
        bcPhaseMax=float(bcPhaseMax)
        
        aHallPhaseMin = configParser.get(partNum, 'aHallPhaseMin') # hallA to phaseA offset in degrees min
        #print ('aHallPhaseMin='+aHallPhaseMin)
        aHallPhaseMin=float(aHallPhaseMin)
        
        aHallPhaseMax = configParser.get(partNum, 'aHallPhaseMax') # hallA to phaseA offset in degrees max
        #print ('aHallPhaseMax='+aHallPhaseMax)
        aHallPhaseMax=float(aHallPhaseMax)
        
        aHallDutyMin = configParser.get(partNum, 'aHallDutyMin') # hallA duty cycle min
        #print ('aHallDutyMin='+aHallDutyMin)
        aHallDutyMin=float(aHallDutyMin)
        
        aHallDutyMax = configParser.get(partNum, 'aHallDutyMax') # hallA duty cycle max
        #print ('aHallDutyMax='+aHallDutyMax)
        aHallDutyMax=float(aHallDutyMax)
        
        bHallDutyMin = configParser.get(partNum, 'bHallDutyMin') # hallB duty cycle min
        #print ('bHallDutyMin='+bHallDutyMin)
        bHallDutyMin=float(bHallDutyMin)
        
        bHallDutyMax = configParser.get(partNum, 'bHallDutyMax') # hallB duty cycle max
        #print ('bHallDutyMax='+bHallDutyMax)
        bHallDutyMax=float(bHallDutyMax)
        
        cHallDutyMin = configParser.get(partNum, 'cHallDutyMin') # hallC duty cycle min
        #print ('cHallDutyMin='+cHallDutyMin)
        cHallDutyMin=float(cHallDutyMin)
        
        cHallDutyMax = configParser.get(partNum, 'cHallDutyMax') # hallC duty cycle max
        #print ('cHallDutyMax='+cHallDutyMax)
        cHallDutyMax=float(cHallDutyMax)
        
        aHallVoltMin = configParser.get(partNum, 'aHallVoltMin') # hallA Volt min
        #print ('aHallVoltMin='+aHallVoltMin)
        aHallVoltMin=float(aHallVoltMin)
        
        aHallVoltMax = configParser.get(partNum, 'aHallVoltMax') # hallA Volt max
        #print ('aHallVoltMax='+aHallVoltMax)
        aHallVoltMax=float(aHallVoltMax)
        
        bHallVoltMin = configParser.get(partNum, 'bHallVoltMin') # hallB Volt min
        #print ('bHallVoltMin='+bHallVoltMin)
        bHallVoltMin=float(bHallVoltMin)
        
        bHallVoltMax = configParser.get(partNum, 'bHallVoltMax') # hallB Volt max
        #print ('bHallVoltMax='+bHallVoltMax)
        bHallVoltMax=float(bHallVoltMax)
        
        cHallVoltMin = configParser.get(partNum, 'cHallVoltMin') # hallC Volt min
        #print ('cHallVoltMin='+cHallVoltMin)
        cHallVoltMin=float(cHallVoltMin)
        
        cHallVoltMax = configParser.get(partNum, 'cHallVoltMax') # hallC Volt max
        #print ('cHallVoltMax='+cHallVoltMax)
        cHallVoltMax=float(cHallVoltMax)
        
        abHallMin = configParser.get(partNum, 'abHallMin') # AB Hall to Hall offset in degrees min
        #print ('abHallMin='+abHallMin)
        abHallMin=float(abHallMin)
        
        abHallMax = configParser.get(partNum, 'abHallMax') # AB Hall to Hall offset in degrees max
        #print ('abHallMax='+abHallMax)
        abHallMax=float(abHallMax)
        
        acHallMin = configParser.get(partNum, 'acHallMin') # AC Hall to Hall offset in degrees min
        #print ('acHallMin='+acHallMin)
        acHallMin=float(acHallMin)
        
        acHallMax = configParser.get(partNum, 'acHallMax') # AC Hall to Hall offset in degrees max
        #print ('acHallMax='+acHallMax)
        acHallMax=float(acHallMax)
        
        bcHallMin = configParser.get(partNum, 'bcHallMin') # BC Hall to Hall offset in degrees min
        #print ('bcHallMin='+bcHallMin)
        bcHallMin=float(bcHallMin)
        
        bcHallMax = configParser.get(partNum, 'bcHallMax') # BC Hall to Hall offset in degrees max
        #print ('bcHallMax='+bcHallMax)
        bcHallMax=float(bcHallMax)
    else:
        print('ERROR: No Config File Found!')
        status = 'ERROR: No Config File Found!'
        text.config(text=status, bg='red', fg='black')
        passFail=0
        return passFail
    
def connectScopes():
    global Scope1, Scope2
    SDS1104XE.connectOScope()
    Scope1=SDS1104XE.my_instrument1
    Scope2=SDS1104XE.my_instrument2
    usb.config(bg='purple')

def getSpeedScope1(): # start test
    global startSpeedTimeOut,img1,failureMessage,status,rpm,passFail,Scope1,speedMin,speedMax,rpm
    Scope=Scope1
    rpm=0.0
    i=startSpeedTimeOut
    while rpm <= speedMin or rpm >= speedMax: # exit if rpm is in config tolerance
        speed.config(text='Start Speed '+str(i), bg = '#3399ff')
        rpm=round(SDS1104XE.measureFreq(Scope, 'C1')/26*60)
        print("Rotor speed : " + str(rpm) + " RPM") # rpm=freq/(rotorMagnetCount/2)*60sec
        sleep(1)
        i=i-1
        if i==0:
            rpm=round(SDS1104XE.measureFreq(Scope, 'C1')/26*60)
            img1=Label(gui, borderwidth=0, image=renderX)
            img1.grid(row=4, column=2)
            status='Failure: Start Speed Timed Out: '+str(rpm)+ "RPM"
            text.config(text=status, bg='red', fg='black')
            passFail=0
            break
    if passFail==1:   
        sleep(2) # allow motor speed to settle
        rpm=round(SDS1104XE.measureFreq(Scope, 'C1')/26*60)
        print("Rotor speed : " + str(rpm) + " RPM") # rpm=freq/(rotorMagnetCount/2)*60sec
        if rpm >= speedMin and rpm <= speedMax:
            img1=Label(gui, borderwidth=0, image=renderCheck)
            img1.grid(row=4, column=2)
        else:
            img1=Label(gui, borderwidth=0, image=renderX)
            img1.grid(row=4, column=2)
            failureMessage='Failure: Start Speed '+str(rpm)+ "RPM"
            text.config(text=failureMessage, bg='red', fg='black')
            passFail=0
        
def getValuesScope1(): # Phase
    global passFail,failureMessage,failureMessage2,failureMessage3,failureMessage4,failureMessage5,failureMessage6,failureMessage7,img2,img3,img4,img5,img6,img7,img8,Scope1,rmsA,rmsB,rmsC,Ph12,Ph13,Ph23,BemfHallPh,aVrmsMin,aVrmsMax,bVrmsMin,bVrmsMax,cVrmsMin,cVrmsMax,abPhaseMin,abPhaseMax,acPhaseMin,acPhaseMax,bcPhaseMin,bcPhaseMax,aHallPhaseMin,aHallPhaseMax 
    Scope=Scope1
    # Read Hall frequcy and duty cycle
    BackEMF1 = SDS1104XE.measurePkPkandRMS(Scope, 'C2')
    BackEMF2 = SDS1104XE.measurePkPkandRMS(Scope, 'C3')
    BackEMF3 = SDS1104XE.measurePkPkandRMS(Scope, 'C4')

    rmsA=BackEMF1[0]
    rmsB=BackEMF2[0]
    rmsC=BackEMF3[0]
    
    Ph12 = SDS1104XE.measurePhase(Scope, 'C2', 'C3')
    Ph13 = SDS1104XE.measurePhase(Scope, 'C2', 'C4')
    Ph23 = SDS1104XE.measurePhase(Scope, 'C3', 'C4')
    BemfHallPh = SDS1104XE.measurePhase(Scope, 'C1', 'C2')
    
    if rmsA >=aVrmsMin and rmsA<=aVrmsMax:
        img2=Label(gui, borderwidth=0, image=renderCheck)
        img2.grid(row=5, column=2)
    else:
        img2=Label(gui, borderwidth=0, image=renderX)
        img2.grid(row=5, column=2)
        failureMessage='Failure: Phase A Voltage, '+str(rmsA)+'Vrms'
        text.config(text=failureMessage, bg='red', fg='black')
        passFail=0
        
    if rmsB >=bVrmsMin and rmsB<=bVrmsMax:
        img3=Label(gui, borderwidth=0, image=renderCheck)
        img3.grid(row=6, column=2)
    else:
        img3=Label(gui, borderwidth=0, image=renderX)
        img3.grid(row=6, column=2)
        failureMessage2='Failure: Phase B Voltage, '+str(rmsB)+'Vrms'
        text.config(text=failureMessage2, bg='red', fg='black')
        passFail=0

    if rmsC >=cVrmsMin and rmsC<=cVrmsMax:
        img4=Label(gui, borderwidth=0, image=renderCheck)
        img4.grid(row=7, column=2)
    else:
        img4=Label(gui, borderwidth=0, image=renderX)
        img4.grid(row=7, column=2)
        failureMessage3='Failure: Phase C Voltage, '+str(rmsC)+'Vrms'
        text.config(text=failureMessage3, bg='red', fg='black')
        passFail=0

    if Ph12 >=abPhaseMin and Ph12<=abPhaseMax:
        img5=Label(gui, borderwidth=0, image=renderCheck)
        img5.grid(row=8, column=2)
    else:
        img5=Label(gui, borderwidth=0, image=renderX)
        img5.grid(row=8, column=2)
        failureMessage4='Failure: Phase AB Alignment, '+str(Ph12)+'deg'
        text.config(text=failureMessage4, bg='red', fg='black')
        passFail=0
        
    if Ph13 >=acPhaseMin and Ph13<=acPhaseMax:
        img6=Label(gui, borderwidth=0, image=renderCheck)
        img6.grid(row=9, column=2)
    else:
        img6=Label(gui, borderwidth=0, image=renderX)
        img6.grid(row=9, column=2)
        failureMessage5='Failure: Phase AC Alignment, '+str(Ph13)+'deg'
        text.config(text=failureMessage5, bg='red', fg='black')
        passFail=0

    if Ph23 >=bcPhaseMin and Ph23<=bcPhaseMax:
        img7=Label(gui, borderwidth=0, image=renderCheck)
        img7.grid(row=10, column=2)
    else:
        img7=Label(gui, borderwidth=0, image=renderX)
        img7.grid(row=10, column=2)
        failureMessage6='Failure: Phase BC Alignment, '+str(Ph23)+'deg'
        text.config(text=failureMessage6, bg='red', fg='black')
        passFail=0
    
    if BemfHallPh >=aHallPhaseMin and BemfHallPh<=aHallPhaseMax:
        img8=Label(gui, borderwidth=0, image=renderCheck)
        img8.grid(row=11, column=2)
    else:
        img8=Label(gui, borderwidth=0, image=renderX)
        img8.grid(row=11, column=2)
        failureMessage7='Failure: PhaseA HallA Alignment, '+str(BemfHallPh)+'deg'
        text.config(text=failureMessage7, bg='red', fg='black')
        passFail=0

    print('PhaseA RMS : ' + str(BackEMF1[0]) + ' Vrms')
    print('PhaseB RMS : ' + str(BackEMF2[0]) + ' Vrms')
    print('PhaseC RMS : ' + str(BackEMF3[0]) + ' Vrms')
    print('Phase A-B '+ str(Ph12) +' Deg')
    print('Phase A-C '+ str(Ph13) +' Deg')
    print('Phase B-C '+ str(Ph23) +' Deg')
    print('HallA to PhaseA sensor alignment ' + str(BemfHallPh) +' Deg')
    
def getValuesScope2(): # Hall
    global passFail,failureMessage8,failureMessage9,failureMessage10,failureMessage11,failureMessage12,failureMessage13,failureMessage14,failureMessage15,failureMessage16,img9,img10,img11,img12,img13,img14,img15,img16,img17,Scope2,DCA,DCB,DCC,pkA,pkB,pkC,Ha12,Ha13,Ha23,aHallDutyMin,aHallDutyMax,bHallDutyMin,bHallDutyMax,cHallDutyMin,cHallDutyMax,aHallVoltMin,aHallVoltMax,bHallVoltMin,bHallVoltMax,cHallVoltMin,cHallVoltMax,abHallMin,abHallMax,acHallMin,acHallMax,bcHallMin,bcHallMax
    Scope=Scope2

    DCA = SDS1104XE.measureDutycycle(Scope, 'C1')#Duty Cycles
    DCB = SDS1104XE.measureDutycycle(Scope, 'C2')
    DCC = SDS1104XE.measureDutycycle(Scope, 'C3')
    
    aHallPKRMS = SDS1104XE.measurePkPkandRMS(Scope, 'C1')#voltages
    bHallPKRMS = SDS1104XE.measurePkPkandRMS(Scope, 'C2')
    cHallPKRMS = SDS1104XE.measurePkPkandRMS(Scope, 'C3')

    pkA=aHallPKRMS[1]
    pkB=bHallPKRMS[1]
    pkC=cHallPKRMS[1]

    Ha12 = SDS1104XE.measurePhase(Scope, 'C1', 'C2')# degrees
    Ha13 = SDS1104XE.measurePhase(Scope, 'C1', 'C3')
    Ha23 = SDS1104XE.measurePhase(Scope, 'C2', 'C3')
    
    if DCA >=aHallDutyMin and DCA<=aHallDutyMax:
        img9=Label(gui, borderwidth=0, image=renderCheck)
        img9.grid(row=4, column=5)
    else:
        img9=Label(gui, borderwidth=0, image=renderX)
        img9.grid(row=4, column=5)
        failureMessage8='Failure: Hall A Duty Cycle, '+str(DCA)+'%'
        text.config(text=failureMessage8, bg='red', fg='black')
        passFail=0
        
    if DCB >=bHallDutyMin and DCB<=bHallDutyMax:
        img10=Label(gui, borderwidth=0, image=renderCheck)
        img10.grid(row=5, column=5)
    else:
        img10=Label(gui, borderwidth=0, image=renderX)
        img10.grid(row=5, column=5)
        failureMessage9='Failure: Hall B Duty Cycle, '+str(DCB)+'%'
        text.config(text=failureMessage9, bg='red', fg='black')
        passFail=0

    if DCC >=cHallDutyMin and DCC<=cHallDutyMax:
        img11=Label(gui, borderwidth=0, image=renderCheck)
        img11.grid(row=6, column=5)
    else:
        img11=Label(gui, borderwidth=0, image=renderX)
        img11.grid(row=6, column=5)
        failureMessage10='Failure: Hall C Duty Cycle, '+str(DCC)+'%'
        text.config(text=failureMessage10, bg='red', fg='black')
        passFail=0

    if pkA >=aHallVoltMin and pkA<=aHallVoltMax:
        img12=Label(gui, borderwidth=0, image=renderCheck)
        img12.grid(row=7, column=5)
    else:
        img12=Label(gui, borderwidth=0, image=renderX)
        img12.grid(row=7, column=5)
        failureMessage11='Failure: Hall A Voltage, '+str(pkA)+'Vpkpk'
        text.config(text=failureMessage11, bg='red', fg='black')
        passFail=0
        
    if pkB >=bHallVoltMin and pkB<=bHallVoltMax:
        img13=Label(gui, borderwidth=0, image=renderCheck)
        img13.grid(row=8, column=5)
    else:
        img13=Label(gui, borderwidth=0, image=renderX)
        img13.grid(row=8, column=5)
        failureMessage12='Failure: Hall B Voltage, '+str(pkB)+'Vpkpk'
        text.config(text=failureMessage12, bg='red', fg='black')
        passFail=0

    if pkC >=cHallVoltMin and pkC<=cHallVoltMax:
        img14=Label(gui, borderwidth=0, image=renderCheck)
        img14.grid(row=9, column=5)
    else:
        img14=Label(gui, borderwidth=0, image=renderX)
        img14.grid(row=9, column=5)
        failureMessage13='Failure: Hall C Voltage, '+str(pkC)+'Vpkpk'
        text.config(text=failureMessage13, bg='red', fg='black')
        passFail=0
     
    if Ha12 >=abHallMin and Ha12<=abHallMax:
        img15=Label(gui, borderwidth=0, image=renderCheck)
        img15.grid(row=10, column=5)
    else:
        img15=Label(gui, borderwidth=0, image=renderX)
        img15.grid(row=10, column=5)
        failureMessage14='Failure: Hall AB Alignment, '+str(Ha12)+'deg'
        text.config(text=failureMessage14, bg='red', fg='black')
        passFail=0
        
    if Ha13 >=acHallMin and Ha13<=acHallMax:
        img16=Label(gui, borderwidth=0, image=renderCheck)
        img16.grid(row=11, column=5)
    else:
        img16=Label(gui, borderwidth=0, image=renderX)
        img16.grid(row=11, column=5)
        failureMessage15='Failure: Hall AC Alignment, '+str(Ha13)+'deg'
        text.config(text=failureMessage15, bg='red', fg='black')
        passFail=0

    if Ha23 >=bcHallMin and Ha23<=bcHallMax:
        img17=Label(gui, borderwidth=0, image=renderCheck)
        img17.grid(row=12, column=5)
    else:
        img17=Label(gui, borderwidth=0, image=renderX)
        img17.grid(row=12, column=5)
        failureMessage16='Failure: Hall BC Alignment, '+str(Ha23)+'deg'
        text.config(text=failureMessage16, bg='red', fg='black')
        passFail=0

    print("HallA sensor Duty cycle : " +str(DCA)+"%")
    print("HallB sensor Duty cycle : " +str(DCB)+"%")
    print("HallC sensor Duty cycle : " +str(DCC)+"%")
    print("HallA sensor voltage level : "+str(aHallPKRMS[1])+" V")
    print("HallB sensor voltage level : "+str(bHallPKRMS[1])+" V")
    print("HallC sensor voltage level : "+str(cHallPKRMS[1])+" V")
    print('Hall A-B '+ str(Ph12) +' Deg')
    print('Hall A-C '+ str(Ph13) +' Deg')
    print('Hall B-C '+ str(Ph23) +' Deg')

def showPlot():
    global scope1,scope2,partNum
    B_EMF_Wave1 = SDS1104XE.getWFfromScope(Scope1, 'C2') # gets wave for for pyPlot
    B_EMF_Wave2 = SDS1104XE.getWFfromScope(Scope1, 'C3')
    B_EMF_Wave3 = SDS1104XE.getWFfromScope(Scope1, 'C4')
    Hall_Wave1 = SDS1104XE.getWFfromScope(Scope2, 'C1') # gets wave for for pyPlot
    Hall_Wave2 = SDS1104XE.getWFfromScope(Scope2, 'C2')
    Hall_Wave3 = SDS1104XE.getWFfromScope(Scope2, 'C3')

    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle('BackEMF and Hall plots')
    ax1.plot(B_EMF_Wave1[0][1:],B_EMF_Wave1[1][1:],B_EMF_Wave2[0][1:],B_EMF_Wave2[1][1:],B_EMF_Wave3[0][1:],B_EMF_Wave3[1][1:])
    ax2.plot(Hall_Wave1[0][1:],Hall_Wave1[1][1:],Hall_Wave2[0][1:],Hall_Wave2[1][1:],Hall_Wave3[0][1:],Hall_Wave3[1][1:])
    plt.show()

def failureTableSheet():
    global failTable,failureMessage,failureMessage2,failureMessage3,failureMessage4,failureMessage5,failureMessage6,failureMessage7,failureMessage8,failureMessage9,failureMessage10,failureMessage11,failureMessage12,failureMessage13,failureMessage14,failureMessage15,failureMessage16
    failTable=[]
    row=[]
    row.append(failureMessage)
    failTable.append(row)
    row=[]
    row.append(failureMessage2)
    failTable.append(row)
    row=[]
    row.append(failureMessage3)
    failTable.append(row)
    row=[]
    row.append(failureMessage4)
    failTable.append(row)
    row=[]
    row.append(failureMessage5)
    failTable.append(row)
    row=[]
    row.append(failureMessage6)
    failTable.append(row)
    row=[]
    row.append(failureMessage7)
    failTable.append(row)
    row=[]
    row.append(failureMessage8)
    failTable.append(row)
    row=[]
    row.append(failureMessage9)
    failTable.append(row)
    row=[]
    row.append(failureMessage10)
    failTable.append(row)
    row=[]
    row.append(failureMessage11)
    failTable.append(row)
    row=[]
    row.append(failureMessage12)
    failTable.append(row)
    row=[]
    row.append(failureMessage13)
    failTable.append(row)
    row=[]
    row.append(failureMessage14)
    failTable.append(row)
    row=[]
    row.append(failureMessage15)
    failTable.append(row)
    row=[]
    row.append(failureMessage16)
    failTable.append(row)

def dataLog():
    global passFail,failTable,barcode,speedMin,speedMax,aVrmsMin,aVrmsMax,bVrmsMin,bVrmsMax,cVrmsMin,cVrmsMax,abPhaseMin,abPhaseMax,acPhaseMin,acPhaseMax,bcPhaseMin,bcPhaseMax,aHallPhaseMin,aHallPhaseMax,aHallDutyMin,aHallDutyMax,bHallDutyMin,bHallDutyMax,cHallDutyMin,cHallDutyMax,aHallVoltMin,aHallVoltMax,bHallVoltMin,bHallVoltMax,cHallVoltMin,cHallVoltMax,abHallMin,abHallMax,acHallMin,acHallMax,bcHallMin,bcHallMax,rpm,rmsA,rmsB,rmsC,Ph12,Ph13,Ph23,BemfHallPh,DCA,DCB,DCC,pkA,pkB,pkC,Ha12,Ha13,Ha23
    table=[]
    row=[]
    row.append(rpm)
    row.append(speedMin)
    row.append(speedMax)
    table.append(row)
    row = []
    row.append(rmsA)
    row.append(aVrmsMin)
    row.append(aVrmsMax)
    table.append(row)
    row = []
    row.append(rmsB)
    row.append(bVrmsMin)
    row.append(bVrmsMax)
    table.append(row)
    row = []
    row.append(rmsC)
    row.append(cVrmsMin)
    row.append(cVrmsMax)
    table.append(row)
    row = []
    row.append(Ph12)
    row.append(abPhaseMin)
    row.append(abPhaseMax)
    table.append(row)
    row = []
    row.append(Ph13)
    row.append(acPhaseMin)
    row.append(acPhaseMax)
    table.append(row)
    row = []
    row.append(Ph23)
    row.append(bcPhaseMin)
    row.append(bcPhaseMax)
    table.append(row)
    row = []
    row.append(BemfHallPh)
    row.append(aHallPhaseMin)
    row.append(aHallPhaseMax)
    table.append(row)
    row = []
    row.append(DCA)
    row.append(aHallDutyMin)
    row.append(aHallDutyMax)
    table.append(row)
    row = []
    row.append(DCB)
    row.append(bHallDutyMin)
    row.append(bHallDutyMax)
    table.append(row)
    row = []
    row.append(DCC)
    row.append(cHallDutyMin)
    row.append(cHallDutyMax)
    table.append(row)
    row = []
    row.append(pkA)
    row.append(aHallVoltMin)
    row.append(aHallVoltMax)
    table.append(row)
    row = []
    row.append(pkB)
    row.append(bHallVoltMin)
    row.append(bHallVoltMax)
    table.append(row)
    row = []
    row.append(pkC)
    row.append(cHallVoltMin)
    row.append(cHallVoltMax)
    table.append(row)
    row = []
    row.append(Ha12)
    row.append(abHallMin)
    row.append(abHallMax)
    table.append(row)
    row = []
    row.append(Ha13)
    row.append(acHallMin)
    row.append(acHallMax)
    table.append(row)
    row = []
    row.append(Ha23)
    row.append(bcHallMin)
    row.append(bcHallMax)
    table.append(row)

    failureTableSheet()
    
    resultsCols = ['Measured Values', 'Minimum','Maximum'] # column labels
    resultsIndex=['Start RPM','Phase A Vrms','Phase B Vrms','Phase C Vrms','Phase AB Alignment','Phase AC Alignment','Phase BC Alignment','PhaseA HallA Alignment','Hall A Duty%','Hall B Duty%','Hall C Duty%','Hall A Vpkpk','Hall B Vpkpk','Hall C Vpkpk','Hall AB Alignment','Hall AC Alignment','Hall BC Alignment']
    dfResults = pd.DataFrame(table, columns=resultsCols, index=resultsIndex)# place table into a pandas dataframe object
    failureCols = ['Failure Message'] # column labels
    failureIndex=['Message1','Message2','Message3','Message4','Message5','Message6','Message7','Message8','Message9','Message10','Message11','Message12','Message13','Message14','Message15','Message16']
    dfFailures = pd.DataFrame(failTable, columns=failureCols, index=failureIndex) #index=resultsIndex) # place table into a pandas dataframe object
    timestr = time.strftime("(%Y%m%d-%H%M%S)") # add date time stamp and save location
    if passFail==1:
        file = barcode+timestr                                                          # file name with date time stamp
    elif passFail==0:
        file = 'Failure-'+barcode+timestr
    extension = '.xlsx'                                                             # file extension
    fullPath = pathlib.Path(os.path.join(folder, file + extension))                 # the full file path
    writer = pd.ExcelWriter(path = fullPath, engine='xlsxwriter',engine_kwargs={'options': {'strings_to_formulas': False}})
    dfResults.to_excel(writer, sheet_name='Results')
    dfFailures.to_excel(writer, sheet_name='Failure Messages')
    writer.save()
    
def savePlot():
    global scope1,scope2,barcode,saveIndex,img18,passFail
    #print(barcode)
    #print(saveIndex)
    if saveIndex==1:
        B_EMF_Wave1 = SDS1104XE.getWFfromScope(Scope1, 'C2') # gets wave for for pyPlot
        B_EMF_Wave2 = SDS1104XE.getWFfromScope(Scope1, 'C3')
        B_EMF_Wave3 = SDS1104XE.getWFfromScope(Scope1, 'C4')
        Hall_Wave1 = SDS1104XE.getWFfromScope(Scope2, 'C1') # gets wave for for pyPlot
        Hall_Wave2 = SDS1104XE.getWFfromScope(Scope2, 'C2')
        Hall_Wave3 = SDS1104XE.getWFfromScope(Scope2, 'C3')

        fig, (ax1, ax2) = plt.subplots(2)
        fig.suptitle('BackEMF and Hall plots')
        ax1.plot(B_EMF_Wave1[0][1:],B_EMF_Wave1[1][1:],B_EMF_Wave2[0][1:],B_EMF_Wave2[1][1:],B_EMF_Wave3[0][1:],B_EMF_Wave3[1][1:])
        ax2.plot(Hall_Wave1[0][1:],Hall_Wave1[1][1:],Hall_Wave2[0][1:],Hall_Wave2[1][1:],Hall_Wave3[0][1:],Hall_Wave3[1][1:])

        folder = SDS1104XE.folder # save path
        timestr = time.strftime("(%Y%m%d-%H%M%S)")
        file = barcode+timestr
        if passFail==0:
            file='Failure-'+file
        extension='.png'
        fullPath = pathlib.Path(os.path.join(folder, file + extension))
        
        plt.savefig(fullPath, dpi='figure', format=None, metadata=None, bbox_inches=None, pad_inches=0.1, facecolor='auto', edgecolor='auto',backend=None)
        img18=Label(gui, borderwidth=0, image=renderCheck)
        img18.grid(row=12, column=2)
        saveIndex=0 
        plt.show()                      
    gui.after(500,savePlot)
    
def openResults():
    filename = filedialog.askopenfilename(initialdir=folder, title="BackEMF Test Results",filetypes=(("all files", "*.*"),("xlsx files", "*.xlsx"),("image files", "*.png")))
    filename = '"'+filename+'"'
    ext = os.path.splitext(filename)
    ext=ext[1].strip('"')
    print (ext)
    if len(filename) >=3 and ext == '.xlsx' :
        path = str('start '+ "excel " + filename)
        os.system(path)
    if len(filename) >=3 and ext == '.png' :
        path = str(filename)
        os.system(path)
        
def openConfig():
    global configFile
    configFile = filedialog.askopenfilename(initialdir=configFolder, title="BackEMF Config Files",filetypes=(("txt files", "*.txt"),("all files", "*.*")))
    configFile = '"'+configFile+'"'
    if len(configFile) >=3:
        path = str('start '+ "notepad " + configFile)
        os.system(path)
        
def about():
    window = tk.Tk()
    window.title("About")
    window.rowconfigure(0, minsize=400, weight=1)      #about window row#, size, wieght
    window.wm_iconbitmap('icon.ico')
    window.geometry('1200x600')
    window.config(bg='#3399ff')
    message ='''
    --About the program--
    Back EMF Tester GUI
    Author: Doug Gammill
    Date: 3/29/2022
    Copyright (c) 2022
    Linear Labs, Inc.
    Tests Motor Back EMF; final assembly.
    Phase Alignment, Phase Voltage, Hall Alignment, Hall Duty Cycle,
    Hall to Phase Alignment.
    General Test Procedure:
    1. Turn on Scope1 and Scope2.
    2. Ensure all USB cables for each dScope are connected to the PC
    3. Ensure Linear Labs Back EMF computer application (gui) has indicated USB coms are good with each device.
    4. Connect the desired part to the test fixture. Make sure to use the correct cable adapters for the part(s).
    5. Scan the barcode located on the motor using the barcode scanner.
    6. Confirm part number selected is correct.
    7. Turn on drill press to spin motor. 
    8. Confirm that there are no failure(s) for the part by reading the label outputs.
    9. Check the excel output file if desired by clicking the 'Results' button on the GUI.
    '''
    text_box = Text(window,height=23,width=95, font=("Adobe",16))
    text_box.pack(expand=True)
    text_box.insert('end', message)
    text_box.config(state='disabled')
    window.mainloop()
        
def failure():
    global failureMessage,failureMessage2,failureMessage3,failureMessage4,failureMessage5,failureMessage6,failureMessage7,failureMessage8,failureMessage9,failureMessage10,failureMessage11,failureMessage12,failureMessage13,failureMessage14,failureMessage15,failureMessage16
    sleep(3)
    fail = tk.Tk()
    fail.title("Failure!!!")
    fail.rowconfigure(0, minsize=400, weight=1)      #about window row#, size, wieght
    fail.wm_iconbitmap('icon.ico')
    fail.geometry('600x500')
    fail.config(bg='red')
    ####if there is a message insert newline at end
    if failureMessage != '':
        failureMessage=failureMessage+'\n'
    if failureMessage2 != '':
        failureMessage2=failureMessage2+'\n'       
    if failureMessage3 != '':
        failureMessage3=failureMessage3+'\n'       
    if failureMessage4 != '':
        failureMessage4=failureMessage4+'\n'        
    if failureMessage5 != '':
        failureMessage5=failureMessage5+'\n'       
    if failureMessage6 != '':
        failureMessage6=failureMessage6+'\n'       
    if failureMessage7 != '':
        failureMessage7=failureMessage7+'\n'       
    if failureMessage8 != '':
        failureMessage8=failureMessage8+'\n'      
    if failureMessage9 != '':
        failureMessage9=failureMessage9+'\n'      
    if failureMessage10 != '':
        failureMessage10=failureMessage10+'\n'       
    if failureMessage11 != '':
        failureMessage11=failureMessage11+'\n'       
    if failureMessage12 != '':
        failureMessage12=failureMessage12+'\n'      
    if failureMessage13 != '':
        failureMessage13=failureMessage13+'\n'       
    if failureMessage14 != '':
        failureMessage14=failureMessage14+'\n'
    if failureMessage15 != '':
        failureMessage15=failureMessage15+'\n'
        
    message = failureMessage+failureMessage2+failureMessage3+failureMessage4+failureMessage5+failureMessage6+failureMessage7+failureMessage8+failureMessage9+failureMessage10+failureMessage11+failureMessage12+failureMessage13+failureMessage14+failureMessage15+failureMessage16

    text_box = Text(fail,height=18,width=46, font=("Adobe",16))
    text_box.pack(expand=True)
    text_box.insert('end', message)
    text_box.config(state='disabled')

    def reset():
        text.config(fg="black",bg='#3399ff',width=25,font=16, text='Please Enter Barcode Bellow')
        fail.destroy()
        
    btn_ok = tk.Button(fail, font=("Adobe",16),width=10, text="OK", command=reset)
    btn_ok.pack()
      
    fail.mainloop()  
    
def getBarcodeInfo(): # event is used for gui entry .bind <return>
    global barcode, partNum, sn, passFail, status
    try:
        barcode=barcode_var.get()
        print(barcode)                                                
        if len(barcode.split('-')) == 4: # check if the barcode is the correct length/format
            first, second, third, sn = barcode.split('-') # put barcode into list of strings
            partNum=first+'-'+second+'-'+third
            text.config(fg="black",bg='Yellow',width=25,font=16, text='Testing: '+partNum)
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
for i in range(12):  ###rows = 12
    gui.columnconfigure(i, weight=1, minsize=100)
    gui.rowconfigure(i, weight=1, minsize=60)

    for j in range(0, 6): ###column = 7
        frame = tk.Frame(
            master=gui,
            relief=tk.RAISED,
            borderwidth=1
        )

# set the background colour of GUI window
gui.configure(background="Black")

# set the title of GUI window
gui.title("Back EMF Tester")
gui.wm_iconbitmap('icon.ico')

text_var = tk.StringVar()
text=tk.Label(gui, font=(12), relief="ridge", text='Setting Up USB, Please Wait', borderwidth=10)
text.grid(row=1, columnspan=6, ipadx=100)
text.update()

# set the configuration of GUI window
gui.geometry("600x800") # width by length
gui.resizable(width=True, height=True)

def resetGui():
    global img1,img2,img3,img4,img5,img6,img7,img8,img9,img10,img11,img12,img13,img14,img15,img16,img17,img18,failureMessage,failureMessage2,failureMessage3,failureMessage4,failureMessage5,failureMessage6,failureMessage7,failureMessage8,failureMessage9,failureMessage10,failureMessage11,failureMessage12,failureMessage13,failureMessage14,failureMessage15,failureMessage16,status,speedMin,speedMax,aVrmsMin,aVrmsMax,bVrmsMin,bVrmsMax,cVrmsMin,cVrmsMax,abPhaseMin,abPhaseMax,acPhaseMin,acPhaseMax,bcPhaseMin,bcPhaseMax,aHallPhaseMin,aHallPhaseMax,aHallDutyMin,aHallDutyMax,bHallDutyMin,bHallDutyMax,cHallDutyMin,cHallDutyMax,aHallVoltMin,aHallVoltMax,bHallVoltMin,bHallVoltMax,cHallVoltMin,cHallVoltMax,abHallMin,abHallMax,acHallMin,acHallMax,bcHallMin,bcHallMax
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
    speedMin = ''
    speedMax = ''
    aVrmsMin = ''
    aVrmsMax = ''
    bVrmsMin = ''
    bVrmsMax = ''
    cVrmsMin = ''
    cVrmsMax = ''
    abPhaseMin = ''
    abPhaseMax = ''
    acPhaseMin = ''
    acPhaseMax = ''
    bcPhaseMin = ''
    bcPhaseMax = ''
    aHallPhaseMin = ''
    aHallPhaseMax = ''
    aHallDutyMin = ''
    aHallDutyMax = ''
    bHallDutyMin = ''
    bHallDutyMax = ''
    cHallDutyMin = ''
    cHallDutyMax = ''
    aHallVoltMin = ''
    aHallVoltMax = ''
    bHallVoltMin = ''
    bHallVoltMax = ''
    cHallVoltMin = ''
    cHallVoltMax = ''
    abHallMin = ''
    abHallMax = ''
    acHallMin = ''
    acHallMax = ''
    bcHallMin = ''
    bcHallMax = ''
    failureMessage=''
    failureMessage2=''
    failureMessage3=''
    failureMessage4=''
    failureMessage5=''
    failureMessage6=''
    failureMessage7=''
    failureMessage8=''
    failureMessage9=''
    failureMessage10=''
    failureMessage11=''
    failureMessage12=''
    failureMessage13=''
    failureMessage14=''
    failureMessage15=''
    failureMessage16=''
    status=''
    speed.config(text='Start Speed', bg = '#3399ff')

def threading(event): # threading used to execute main functions and allow GUI main loop to not freeze
    t1=Thread(target=mainFunctions)
    t1.start()   

def mainFunctions(): # main multi threaded functions
    global passFail,status,skipFail,saveIndex
    passFail=1
    resetGui()
    getBarcodeInfo()
    if passFail==1:
        readConfig() # read variables from config file
    if passFail==1:
        getSpeedScope1()
    if passFail==1 and skipFail==0: # will perform full test even if failure happens
        getValuesScope1()
        getValuesScope2()
    if passFail==1 and skipFail==1: # will skip scope2 test if set to 1 in configFile
        getValuesScope1()
        if passFail==1:
            getValuesScope2()
    if passFail==1:
        saveIndex=1
        dataLog()
        text.config(text='Test Passed Please Enter Barcode Bellow', bg = '#3399ff')
    if passFail==0 and status=='':
        saveIndex=1
        dataLog()
        failure()      
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

usb=tk.Label(gui, text="USB", height=3, width=16, font='12', fg='black', bg='white', relief="groove", borderwidth=2)
usb.grid(row=0, column=3)
usb.update()

test1=tk.Label(gui, text="Scope1 Test:", height=3, width=20, font="Verdana 12 underline", fg='white', bg='blue', relief="groove")
test1.grid(row=3, column=0, columnspan=2)
test1.update()
phase1=tk.Label(gui, text="Phases", height=3, width=16, font="Verdana 12 underline", fg='white', bg='blue', relief="groove")
phase1.grid(row=3, column=2)
phase1.update()
test2=tk.Label(gui, text="Scope2 Test:", height=3, width=20, font="Verdana 12 underline", fg='white', bg='blue', relief="groove")
test2.grid(row=3, column=3, columnspan=2)
test2.update()
hall2=tk.Label(gui, text="Halls", height=3, width=16, font="Verdana 12 underline", fg='white', bg='blue', relief="groove")
hall2.grid(row=3, column=5)
hall2.update()
speed=tk.Label(gui, text="Start Speed", height=3, width=22, font='12', fg='black', bg='#3399ff', relief="groove")
speed.grid(row=4, column=0, columnspan=2)
speed.update()
VA=tk.Label(gui, text="Phase A Voltage", height=3, width=22, font='12', fg='black', bg='#3399ff', relief="groove")
VA.grid(row=5, column=0, columnspan=2)
VA.update()
VB = tk.Label(gui, text="Phase B Voltage", height=3, width=22, font='12', fg='black', bg='#3399ff', relief="groove")
VB.grid(row=6, column=0, columnspan=2)
VB.update()
VC = tk.Label(gui, text="Phase C Voltage", height=3, width=22, font='12', fg='black', bg='#3399ff', relief="groove")
VC.grid(row=7, column=0, columnspan=2)
VC.update()
PAB = tk.Label(gui, text="Phase AB  Alignment", height=3, width=22, font='12', fg='black', bg='#3399ff', relief="groove")
PAB.grid(row=8, column=0, columnspan=2)
PAB.update()
PAC = tk.Label(gui, text="Phase AC Alignment", height=3, width=22, font='12', fg='black', bg='#3399ff', relief="groove")
PAC.grid(row=9, column=0, columnspan=2)
PAC.update()
PBC = tk.Label(gui, text="Phase BC Alignment", height=3, width=22, font='12', fg='black', bg='#3399ff', relief="groove")
PBC.grid(row=10, column=0, columnspan=2)
PBC.update()
HPA = tk.Label(gui, text="HallA PhaseA Alignment", height=3, width=22, font='12', fg='black', bg='#3399ff', relief="groove")
HPA.grid(row=11, column=0, columnspan=2)
HPA.update()
savPlt = tk.Label(gui, text="Plot Graph", height=3, width=22, font='12', fg='white', bg='blue', relief="groove")
savPlt.grid(row=12, column=0, columnspan=2)
savPlt.update()

DutyA = tk.Label(gui, text="Hall A Duty Cycle", height=3, width=22, font='12', fg='black', bg='#3399ff', relief="groove")
DutyA.grid(row=4, column=3, columnspan=2)
DutyA.update()
DutyB = tk.Label(gui, text="Hall B Duty Cycle", height=3, width=22, font='12', fg='black', bg='#3399ff', relief="groove")
DutyB.grid(row=5, column=3, columnspan=2)
DutyB.update()
DutyC=tk.Label(gui, text="Hall C Duty Cycle", height=3, width=22, font='12', fg='black', bg='#3399ff', relief="groove")
DutyC.grid(row=6, column=3, columnspan=2)
DutyC.update()
HVA=tk.Label(gui, text="Hall A Voltage", height=3, width=22, font='12', fg='black', bg='#3399ff', relief="groove")
HVA.grid(row=7, column=3, columnspan=2)
HVA.update()
HVB = tk.Label(gui, text="Hall B Voltage", height=3, width=22, font='12', fg='black', bg='#3399ff', relief="groove")
HVB.grid(row=8, column=3, columnspan=2)
HVB.update()
HVC = tk.Label(gui, text="Hall C Voltage", height=3, width=22, font='12', fg='black', bg='#3399ff', relief="groove")
HVC.grid(row=9, column=3, columnspan=2)
HVC.update()
HAB = tk.Label(gui, text="Hall AB Alignment", height=3, width=22, font='12', fg='black', bg='#3399ff', relief="groove")
HAB.grid(row=10, column=3, columnspan=2)
HAB.update()
HAC = tk.Label(gui, text="Hall AC Alignment", height=3, width=22, font='12', fg='black', bg='#3399ff', relief="groove")
HAC.grid(row=11, column=3, columnspan=2)
HAC.update()
HBC = tk.Label(gui, text="Hall BC Alignment", height=3, width=22, font='12', fg='black', bg='#3399ff', relief="groove")
HBC.grid(row=12, column=3, columnspan=2)
HBC.update()

####IMG####
load= Image.open("logo4.ppm")
render = ImageTk.PhotoImage(load)
img = Label(gui, borderwidth=0, image=render)
img.grid(row=0, column=4, columnspan=2)
img.update()

load= Image.open("motorIcon.png")
render2 = ImageTk.PhotoImage(load)

img1=Label(gui, borderwidth=0, image=render2)
img1.grid(row=4, column=2)
img2=Label(gui, borderwidth=0, image=render2)
img2.grid(row=5, column=2)
img3=Label(gui, borderwidth=0, image=render2)
img3.grid(row=6, column=2)
img4=Label(gui, borderwidth=0, image=render2)
img4.grid(row=7, column=2)
img5=Label(gui, borderwidth=0, image=render2)
img5.grid(row=8, column=2)
img6=Label(gui, borderwidth=0, image=render2)
img6.grid(row=9, column=2)
img7=Label(gui, borderwidth=0, image=render2)
img7.grid(row=10, column=2)
img8=Label(gui, borderwidth=0, image=render2)
img8.grid(row=11, column=2)
img9=Label(gui, borderwidth=0, image=render2)
img9.grid(row=4, column=5)
img10=Label(gui, borderwidth=0, image=render2)
img10.grid(row=5, column=5)
img11=Label(gui, borderwidth=0, image=render2)
img11.grid(row=6, column=5)
img12=Label(gui, borderwidth=0, image=render2)
img12.grid(row=7, column=5)
img13=Label(gui, borderwidth=0, image=render2)
img13.grid(row=8, column=5)
img14=Label(gui, borderwidth=0, image=render2)
img14.grid(row=9, column=5)
img15=Label(gui, borderwidth=0, image=render2)
img15.grid(row=10, column=5)
img16=Label(gui, borderwidth=0, image=render2)
img16.grid(row=11, column=5)
img17=Label(gui, borderwidth=0, image=render2)
img17.grid(row=12, column=5)
img18=Label(gui, borderwidth=0, image=render2)
img18.grid(row=12, column=2)

load= Image.open("Red-X.ppm")
renderX = ImageTk.PhotoImage(load)
load= Image.open("Blue-Check1.ppm")
renderCheck = ImageTk.PhotoImage(load)
connectScopes()
text.config(text='Please Enter Barcode Bellow', bg = '#3399ff')

gui.after(100, savePlot)

gui.mainloop() # start the GUI
