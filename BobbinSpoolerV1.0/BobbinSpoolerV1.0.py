import configTemplate # handles config files, requires configParser
import arduinoSpooler # requires pyserial, sleep
import arduinoWireEncoder # requires pyserial, sleep
#import arduinoPressureSensors # requires pyserial, sleep
from tkinter import * # handles GUI
from tkinter import scrolledtext # handles gui scrolling text box
from threading import * # handles threading so GUI doesnt freeze during main functions
import tkinter as tk # handles GUI
from PIL import Image, ImageTk # handles GUI Image
from tkinter import filedialog # handles opening Results and Config file paths
import os  # for working with opening files with applications like excel and notepad
from time import sleep # handles delay
configFolder=configTemplate.configFolder # config file path local
macroPath=configTemplate.macroPath # where macros are stored on network
comOK = 0
testIndex = 0
message=''
recordIndex=0

def openLocalConfig():
    os.startfile(configFolder) #local folderConfig (has *idn? and macro path info)
    
def openMacros():
    os.startfile(macroPath)
def openManual():
    os.startfile('Manual.pdf')

def connectArduinoSpooler():
    global passFail,failureMessage,usbPort
    arduinoSpooler.connectArduino() # connects to arduino through arduino module
    if arduinoSpooler.passFail==1:
        passFail=1
        failureMessage="Bobbin Spooler USB Failed Connection"
        usb.config(fg='white', bg='red')
        return
    else:
        usb.config(fg='white', bg='purple',text= 'USB:'+ arduinoSpooler.usbPort)
        return

def about():
    window = tk.Tk()
    window.title("About")
    window.rowconfigure(0, minsize=400, weight=1) # about window row#, size, wieght
    window.wm_iconbitmap('icon.ico')
    window.geometry('1200x600')
    window.config(bg='#3399ff')
    message ='''
    --About the program--
    Bobbin Winder GUI
    Linear Labs, Inc.
    Author: Doug Gammill
    Date: 8/24/2022
    Copyright (c) 2022
    Aids in Spooling Wire.
    Can be used stand alone or with a computer GUI.
    
    1. Ensure USB cables are connected to the PC.
    2. Ensure Linear Labs Bobbin Spooler (gui) has indicated USB coms are good with devices.
    '''
    text_box = Text(window,height=23,width=95, font=("Adobe",16))
    text_box.pack(expand=True)
    text_box.insert('end', message)
    text_box.config(state='disabled')
    window.mainloop()

    
# Driver code 
#if __name__ == "__main__":
# create a GUI window
gui = Tk()
for i in range(15):  ###rows = 15
    gui.columnconfigure(i, weight=1, minsize=110)
    gui.rowconfigure(i, weight=1, minsize=10)

    for j in range(0, 7): ###column = 7
        frame = tk.Frame(master=gui,relief=tk.RAISED,borderwidth=2)
        
gui.configure(background="Black") # set the background colour of GUI window
gui.title("Bobbin Spooler") # set the title of GUI window
gui.wm_iconbitmap('icon.ico')
# set the configuration of GUI window
gui.geometry("768x600") # width by length
gui.resizable(width=True, height=True)

menubar = Menu(gui, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')
help = Menu(menubar, tearoff=0)  
help.add_command(label="About", command=about)
help.add_command(label="Local Config", command=openLocalConfig)
help.add_command(label="Macros", command=openMacros)
help.add_command(label="User Manual", command=openManual)
menubar.add_cascade(label="Options", menu=help)
gui.config(menu=menubar)

#text_var = tk.StringVar()
text=tk.Label(gui,font='12',width=40,relief='ridge',text='Setting Up USB, Please Wait',borderwidth=5)
text.grid(row=0, columnspan=4, ipadx=25)
text.update()

usbSpooler=tk.Label(gui,font='12',width=12,relief='ridge',text="Spooler",fg='black',bg='white',borderwidth=5)
usbSpooler.grid(row=0, column=4)
usbSpooler.update()

usbEncoder=tk.Label(gui,font='12',width=12,relief='ridge',text="Encoder",fg='black',bg='white',borderwidth=5)
usbEncoder.grid(row=0, column=5)
usbEncoder.update()

usbPressure=tk.Label(gui,font='12',width=12,relief='ridge',text="Sensors",fg='black',bg='white',borderwidth=5)
usbPressure.grid(row=0, column=6)
usbPressure.update()

####column 0
def zero():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:0,0')
    if recordIndex==1:
        message = '0,0'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def rpm():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:1,0')
    if recordIndex==1:
        message = '1,0'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def auto():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:2,0')
    if recordIndex==1:
        message = '2,0'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def breakBut():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:3,0')
    if recordIndex==1:
        message = '3,0'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def jump():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:4,0')
    if recordIndex==1:
        message = '4,0'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
####column 1
def selData():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:0,1')
    if recordIndex==1:
        message = '0,1'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def dirLevel():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:1,1')
    if recordIndex==1:
        message = '1,1'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def dirShaft():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:2,1')
    if recordIndex==1:
        message = '2,1'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def bothBreak():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:3,1')
    if recordIndex==1:
        message = '3,1'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def back():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:4,1')
    if recordIndex==1:
        message = '4,1'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
####column 2
def startStep():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:0,2')
    if recordIndex==1:
        message = '0,2'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def endStep():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:1,2')
    if recordIndex==1:
        message = '1,2'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def autoZero():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:2,2')
    if recordIndex==1:
        message = '2,2'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def autoStart():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:3,2')
    if recordIndex==1:
        message = '3,2'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def resume():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:4,2')
    if recordIndex==1:
        message = '4,2'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
####column 3
def sevenBut():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:0,3')
    if recordIndex==1:
        message = '0,3'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def fourBut():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:1,3')
    if recordIndex==1:
        message = '1,3'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def oneBut():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:2,3')
    if recordIndex==1:
        message = '2,3'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def zeroBut():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:3,3')
    if recordIndex==1:
        message = '3,3'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def stop():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:4,3')
    if recordIndex==1:
        message = '4,3'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
####column 4
def eightBut():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:0,4')
    if recordIndex==1:
        message = '0,4'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def fiveBut():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:1,4')
    if recordIndex==1:
        message = '1,4'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def twoBut():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:2,4')
    if recordIndex==1:
        message = '2,4'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def clear():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:3,4')
    if recordIndex==1:
        message = '3,4'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def start():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:4,4')
    if recordIndex==1:
        message = '4,4'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
####column 5
def nineBut():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:0,5')
    if recordIndex==1:
        message = '0,5'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def sixBut():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:1,5')
    if recordIndex==1:
        message = '1,5'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def threeBut():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:2,5')
    if recordIndex==1:
        message = '2,5'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def copy():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:3,5')
    if recordIndex==1:
        message = '3,5'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def left():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:4,5')
    if recordIndex==1:
        message = '4,5'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
####column 6
def setStep():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:0,6')
    if recordIndex==1:
        message = '0,6'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def setQty():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:1,6')
    if recordIndex==1:
        message = '1,6'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def dash():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:2,6')
    if recordIndex==1:
        message = '2,6'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def ent():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:3,6')
    if recordIndex==1:
        message = '3,6'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return
def right():
    global mac,recordIndex,text_area
    arduinoSpooler.command('push:4,6')
    if recordIndex==1:
        message = '4,6'
        text_area.insert(tk.INSERT, message+':')
        mac.append(message)
        print(mac)
    return

#### column 0
zeroButton= Button(gui,text='Zero',font='12',fg='black',bg='#3399ff',borderwidth=5,command=zero,height=1,width=10)
zeroButton.grid(row=1, column=0)
zeroButton.update()

rpmButton= Button(gui,text='RPM',font='12',fg='black',bg='#3399ff',borderwidth=5,command=rpm,height=1,width=10)
rpmButton.grid(row=2,column=0)
rpmButton.update()

autoButton= Button(gui,text='Auto',font='12',fg='white',bg='blue',borderwidth=5,command=auto,height=1,width=10)
autoButton.grid(row=3, column=0)
autoButton.update()

breakButton= Button(gui,text='Break',font='12',fg='white',bg='blue',borderwidth=5,command=breakBut,height=1,width=10)
breakButton.grid(row=4, column=0)
breakButton.update()

jumpButton= Button(gui,text='Jump',font='12',fg='white',bg='blue',borderwidth=5,command=jump,height=1,width=10)
jumpButton.grid(row=5,column=0)
jumpButton.update()

#### column 1
selDataButton= Button(gui,text='Sel Data',font='12',fg='black',bg='#3399ff',borderwidth=5,command=selData,height=1,width=10)
selDataButton.grid(row=1, column=1)
selDataButton.update()

dirLevelButton= Button(gui,text='Dir Level',font='12',fg='black',bg='#3399ff',borderwidth=5,command=dirLevel,height=1,width=10)
dirLevelButton.grid(row=2,column=1)
dirLevelButton.update()

dirShaftButton= Button(gui,text='Dir Shaft',font='12',fg='black',bg='#3399ff',borderwidth=5,command=dirShaft,height=1,width=10)
dirShaftButton.grid(row=3, column=1)
dirShaftButton.update()

bothBreakButton= Button(gui,text='Both Break',font='12',fg='black',bg='#3399ff',borderwidth=5,command=bothBreak,height=1,width=10)
bothBreakButton.grid(row=4, column=1)
bothBreakButton.update()

backButton= Button(gui,text='Back',font='12',fg='white',bg='blue',borderwidth=5,command=back,height=1,width=10)
backButton.grid(row=5,column=1)
backButton.update()

#### column 2
startStepButton= Button(gui,text='Start Step',font='12',fg='black',bg='#3399ff',borderwidth=5,command=startStep,height=1,width=10)
startStepButton.grid(row=1, column=2)
startStepButton.update()

endStepButton= Button(gui,text='End Step',font='12',fg='black',bg='#3399ff',borderwidth=5,command=endStep,height=1,width=10)
endStepButton.grid(row=2,column=2)
endStepButton.update()

autoZeroButton= Button(gui,text='Auto Zero',font='12',fg='black',bg='#3399ff',borderwidth=5,command=autoZero,height=1,width=10)
autoZeroButton.grid(row=3, column=2)
autoZeroButton.update()

autoStartButton= Button(gui,text='Auto Start',font='12',fg='black',bg='#3399ff',borderwidth=5,command=autoStart,height=1,width=10)
autoStartButton.grid(row=4, column=2)
autoStartButton.update()

resumeButton= Button(gui,text='Resume',font='12',fg='white',bg='blue',borderwidth=5,command=resume,height=1,width=10)
resumeButton.grid(row=5,column=2)
resumeButton.update()

#### column 3
sevenButton= Button(gui,text='7',font='12',fg='black',bg='#3399ff',borderwidth=5,command=sevenBut,height=1,width=10)
sevenButton.grid(row=1, column=3)
sevenButton.update()

fourButton= Button(gui,text='4',font='12',fg='black',bg='#3399ff',borderwidth=5,command=fourBut,height=1,width=10)
fourButton.grid(row=2,column=3)
fourButton.update()

oneButton= Button(gui,text='1',font='12',fg='black',bg='#3399ff',borderwidth=5,command=oneBut,height=1,width=10)
oneButton.grid(row=3, column=3)
oneButton.update()

zeroButton= Button(gui,text='0',font='12',fg='black',bg='#3399ff',borderwidth=5,command=zeroBut,height=1,width=10)
zeroButton.grid(row=4, column=3)
zeroButton.update()

stopButton= Button(gui,text='Stop',font='12',fg='white',bg='blue',borderwidth=5,command=stop,height=1,width=10)
stopButton.grid(row=5,column=3)
stopButton.update()

#### column 4
eightButton= Button(gui,text='8',font='12',fg='black',bg='#3399ff',borderwidth=5,command=eightBut,height=1,width=10)
eightButton.grid(row=1, column=4)
eightButton.update()

fiveButton= Button(gui,text='5',font='12',fg='black',bg='#3399ff',borderwidth=5,command=fiveBut,height=1,width=10)
fiveButton.grid(row=2,column=4)
fiveButton.update()

twoButton= Button(gui,text='2',font='12',fg='black',bg='#3399ff',borderwidth=5,command=twoBut,height=1,width=10)
twoButton.grid(row=3, column=4)
twoButton.update()

clearButton= Button(gui,text='Clear',font='12',fg='black',bg='#3399ff',borderwidth=5,command=clear,height=1,width=10)
clearButton.grid(row=4, column=4)
clearButton.update()

startButton= Button(gui,text='Start',font='12',fg='white',bg='blue',borderwidth=5,command=start,height=1,width=10)
startButton.grid(row=5,column=4)
startButton.update()

#### column 5
nineButton= Button(gui,text='9',font='12',fg='black',bg='#3399ff',borderwidth=5,command=nineBut,height=1,width=10)
nineButton.grid(row=1, column=5)
nineButton.update()

sixButton= Button(gui,text='6',font='12',fg='black',bg='#3399ff',borderwidth=5,command=sixBut,height=1,width=10)
sixButton.grid(row=2,column=5)
sixButton.update()

threeButton= Button(gui,text='3',font='12',fg='black',bg='#3399ff',borderwidth=5,command=threeBut,height=1,width=10)
threeButton.grid(row=3, column=5)
threeButton.update()

copyButton= Button(gui,text='Copy',font='12',fg='black',bg='#3399ff',borderwidth=5,command=copy,height=1,width=10)
copyButton.grid(row=4, column=5)
copyButton.update()

leftButton= Button(gui,text='<',font='12',fg='white',bg='blue',borderwidth=5,command=left,height=1,width=10)
leftButton.grid(row=5,column=5)
leftButton.update()

#### column 6
setStepButton= Button(gui,text='Set Step',font='12',fg='black',bg='#3399ff',borderwidth=5,command=setStep,height=1,width=10)
setStepButton.grid(row=1, column=6)
setStepButton.update()

setQtyButton= Button(gui,text='Set Qty',font='12',fg='black',bg='#3399ff',borderwidth=5,command=setQty,height=1,width=10)
setQtyButton.grid(row=2,column=6)
setQtyButton.update()

dashButton= Button(gui,text='-',font='12',fg='black',bg='#3399ff',borderwidth=5,command=dash,height=1,width=10)
dashButton.grid(row=3, column=6)
dashButton.update()

entButton= Button(gui,text='Enter',font='12',fg='black',bg='#3399ff',borderwidth=5,command=ent,height=1,width=10)
entButton.grid(row=4, column=6)
entButton.update()

rightButton= Button(gui,text='>',font='12',fg='white',bg='blue',borderwidth=5,command=right,height=1,width=10)
rightButton.grid(row=5,column=6)
rightButton.update()

def readMac():
    global data_into_list,OPTIONS,MACROS,macroNumber,mac,macroPath
    my_file = open(macroPath, "r") # opening macros file in access mode  
    data = my_file.read() # reading the file
    data_into_list = data.split('\n')
    while("" in data_into_list) :
        data_into_list.remove("")
    #print(data_into_list)
    my_file.close()
    OPTIONS=[]
    MACROS=[]
    i=0
    for OPTION in data_into_list:
        OPTION = OPTION.split('=')
        macroName = OPTION[0]
        macroFunction = OPTION[1]
        macroName = str(i)+'-'+macroName
        OPTIONS.append(macroName)
        MACROS.append(macroFunction)
        i=i+1
    macroNumber = macroName.split('-')
    macroNumber = macroNumber[0]
    mac=MACROS[int(macroNumber)]
    mac = mac.split(':')
    #print(mac)
    return
readMac()

    
def recordWindow():
    global recordIndex,text_area,mac,macName_var
    recordIndex=1
    mac=[]
    recMac = Toplevel(gui)
    recMac.title("Recording Macro!!!")
    recMac.geometry("452x380")
    recMac.wm_iconbitmap('icon.ico')
    recMac.config(bg='#3399ff')
    text.config(text='Recording Macro', bg = 'yellow')
    text_area = scrolledtext.ScrolledText(recMac,wrap=tk.WORD,width=41,height=10,font=("Times New Roman",15))
    text_area.grid(column = 0, pady = 10, padx = 10)
    text_area.focus()# Placing cursor in the text area
    def destroyWindow(event):
        global macName_var,mac,dropdown,recordIndex
        length=len(mac)-1
        i=0
        macString = ''
        while i < length:
            macString = macString + mac[i]+':'
            i=i+1
        macString = macString + mac[i]
        macName_var=macName_var.get()
        macString = macName_var + '=' + macString + '\n'
        #print(macString)
        my_file = open(macroPath, "a") # opening macros file in read mode
        my_file.write(macString)
        my_file.close()
        recMac.destroy()
        text.config(text='Recording Macro Succeded', bg = 'blue')
        recordIndex=0
        readMac()
        dropdown.destroy()
        dropDownBox()
        return
    def destroyRecWindow():
        global recordIndex
        recMac.destroy()
        text.config(text='Recording Macro Cancelled', bg = 'blue')
        recordIndex=0
        readMac()
    savetext=tk.Label(recMac,font='12',width=40,bg='#3399ff',text='Enter Macro Name To Save:',borderwidth=5)
    savetext.grid(row=2, columnspan=4, ipadx=25)
    savetext.update()
    macName_var = tk.StringVar() 
    expression_field1=tk.Entry(recMac, font=(12), relief="groove", textvariable=macName_var, borderwidth=10)
    expression_field1.bind('<Return>',destroyWindow)
    expression_field1.grid(row=3, column=0, columnspan=6, ipadx=100,pady=5)
    expression_field1.icursor('end')
    expression_field1.focus_set()
    expression_field1.update()
    macName_var.set('')
    cancel_but = tk.Button(recMac,width=20,font='12',text="Cancel",command=destroyRecWindow)
    cancel_but.grid(row=4, column=0, columnspan=6, ipadx=25,pady=5)
    cancel_but.update()
    return

def macroThread():
    global testIndex
    if testIndex==0: # only start if nothing else is running
        t2=Thread(target=playMacro)
        t2.start()
    return

def deleteMacro():
    global MACROS,macroNumber,macroPath,variable
    with open(macroPath, "r+") as f:
        d = f.readlines()
        f.seek(0)
        macroName = variable.get()
        Name = macroName.split('-')
        Name = Name[1]
        lineToDelete = Name+'='+MACROS[int(macroNumber)]+'\n'
        print(lineToDelete)
        for i in d:
            if i != lineToDelete:
                f.write(i)
        f.truncate()
    readMac()
    dropdown.destroy()
    dropDownBox()
    return

def playMacro():
    global mac, testIndex, result
    print(mac)
    usbComs()
    testIndex = 1 # under operation, do nothing else
    for cmd in mac:
        arduinoSpooler.command('push:'+cmd)
    sleep(2)
    arduinoWireEncoder.command('dire?')
    result = arduinoWireEncoder.result
    while result != 'direction, No Movement':
        sleep(2)
        arduinoWireEncoder.command('dire?')
        result = arduinoWireEncoder.result
    testIndex = 0
    return

macButton= Button(gui,text='Play Macro',font='12',fg='white',bg='blue',borderwidth=5,command=macroThread,height=1,width=10)
macButton.grid(row=6,column=4)
macButton.update()

recButton= Button(gui,text='Rec Macro',font='12',fg='white',bg='blue',borderwidth=5,command=recordWindow,height=1,width=10)
recButton.grid(row=6,column=5)
recButton.update()

delButton= Button(gui,text='Del Macro',font='12',fg='white',bg='blue',borderwidth=5,command=deleteMacro,height=1,width=10)
delButton.grid(row=6,column=6)
delButton.update()

def display_selected(macroName):
    global mac,variable,macroNumber,MACROS
    macroName = variable.get()
    macroNumber = macroName.split('-')
    macroNumber = macroNumber[0]
    mac=MACROS[int(macroNumber)]
    mac = mac.split(':')
    print(mac)

#for OPTIONS in data_into_list
def dropDownBox():
    global dropdown,variable
    variable = StringVar() # setting variable for Integers
    variable.set(OPTIONS[0]) #### use this to set an option as the identifier
    dropdown = OptionMenu(gui,variable,*OPTIONS,command=display_selected) # creating widget
    dropdown.config(width=42,borderwidth=3,relief='ridge',font='12')
    dropdown.grid(row=6, column=0, columnspan=4)
    dropdown.update()
dropDownBox()

####IMG####
load= Image.open("logo4.ppm")
render = ImageTk.PhotoImage(load)
img = Label(gui, borderwidth=0, image=render)
img.grid(row=15,columnspan=7)
img.update()

def checkUSB():
    global comOK,testIndex, passFailArduinoSpooler, passFailEncoder
    if comOK == 1 and testIndex == 0: # comOK=1 means at some point USB was good and index=0 means not currently testing
        text.config(fg="black",bg='orange',text='Checking USB')
        try:
            #### Check Spooler
            arduinoSpooler.checkArduino()
            passFailArduinoSpooler=arduinoSpooler.passFail
            if passFailArduinoSpooler == 1:
                    usbSpooler.config(fg="black",bg='red',text='Connect USB')
                    comOK = 0  # fail
            #### Check Encoder
            arduinoWireEncoder.checkArduino()
            passFailEncoder=arduinoWireEncoder.passFail
            if passFailEncoder == 1:
                    usbEncoder.config(fg="black",bg='red',text='Connect USB')
                    comOK = 0  # fail
                    
            #### Total USB Connection Status
            if  passFailArduinoSpooler == 0 and passFailEncoder == 0:
                text.config(fg="black",bg='#3399ff',text='USB Connected')
            else:
                text.config(bg='red', fg='black', text='Connect USB')
     
        except:
            comOK=0
            print("something went wrong")
            text.config(fg="black",bg='red',text='Connect USB')
    return

def connectUSB():
    global comOK,testIndex, passFailArduinoSpooler,passFailEncoder
    while comOK == 0 and testIndex == 0: # comOK=1 means at some point USB was good and testIndex=0 means not currently testing
        #### Connect Spooler
        arduinoSpooler.connectArduino()
        passFailArduinoSpooler = arduinoSpooler.passFail
        if passFailArduinoSpooler==1: # 1 = failure
            usbSpooler.config(bg='red',fg='black', text='Connect USB')
        else:
            usbSpooler.config(bg='purple',fg='white', text='Spooler')

        #### Connect Encoder
        arduinoWireEncoder.connectArduino()
        passFailEncoder = arduinoWireEncoder.passFail
        if passFailEncoder==1: # 1 = failure
            usbEncoder.config(bg='red',fg='black', text='Connect USB')
        else:
            usbEncoder.config(bg='purple',fg='white', text='Encoder')

        #### total USB connection status    
        if passFailArduinoSpooler == 0 and passFailEncoder == 0:
            comOK = 1
        else:
            text.config(bg='red', fg='black', text='Connect USB')
    return

def usbComs():
    checkUSB()
    connectUSB()
    checkUSB()
    return

def usbThread():
    t1=Thread(target=usbComs)
    t1.start()
    return

usbThread()

gui.mainloop() # start the GUI
