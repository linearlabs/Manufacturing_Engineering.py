from threading import * # handles threading so GUI doesnt freeze during main functions
import websocket # pip install websocket-client
from tkinter import * # handles GUI
import tkinter as tk # handles GUI
from tkinter import filedialog # handles opening Results and Config file paths
from PIL import Image, ImageTk # handles GUI Image
import os  # for working with opening files with applications like excel and notepad
import configparser # handles config files
from time import sleep

configParser = configparser.RawConfigParser() # config
configFile = 'Config.txt'
configParser.read(configFile)
pumpIP = configParser.get('Config', 'pumpIP')
pumpSpeed = configParser.get('Config', 'pumpSpeed')
pumpSteps = configParser.get('Config', 'pumpSteps')
pumpHalfStep = configParser.get('Config', 'pumpHalfStep')
rotTableIP = configParser.get('Config', 'rotTableIP')
rotTableSpeed = configParser.get('Config', 'rotTableSpeed')
rotTableSteps = configParser.get('Config', 'rotTableSteps')
rotTableHalfStep = configParser.get('Config', 'rotTableHalfStep')
enableEncoders = configParser.get('Config', 'enableEncoders')
resetEncoders = configParser.get('Config', 'resetEncoders')
manualSpeed = configParser.get('Config', 'manualSpeed')
primeSpeed = configParser.get('Config', 'primeSpeed')
primeSteps = configParser.get('Config', 'primeSteps')
deprimeSpeed = configParser.get('Config', 'deprimeSpeed')
deprimeSteps = configParser.get('Config', 'deprimeSteps')
# only set in config
# warning setting both as primary will cause GPIOs to short
# remove GPIO cable if setting both to primary
pumpPrimary = configParser.get('Config', 'pumpPrimary')
rotTablePrimary = configParser.get('Config', 'rotTablePrimary')
devMode = configParser.get('Config', 'devMode')
enableWebserial = 0
manualPump = 0
sleepTime = 0.25
sendParameters1 = 1 # send parameters only the first go or if they changed
sendParameters2 = 1 # send parameters only the first go or if they changed

# Driver code 
#if __name__ == "__main__":
# create a GUI window
gui = Tk()
for i in range(8):  ###rows = 8
    gui.columnconfigure(i, weight=1, minsize=110)
    gui.rowconfigure(i, weight=1, minsize=10)

    for j in range(0, 7): ###column = 7
        frame = tk.Frame(master=gui,relief=tk.RAISED,borderwidth=2)
        
gui.configure(background="Black") # set the background colour of GUI window
gui.title("Project Sticky Fingers") # set the title of GUI window
gui.wm_iconbitmap('icon.ico')
# set the configuration of GUI window
if devMode == '1':
    guiGeometry = "1000x400"
else:
    guiGeometry = "1000x300"
gui.geometry(guiGeometry) # width by length
gui.resizable(width=True, height=True)

def openLocalConfig():
    os.startfile("Config.txt") #local folderConfig
    
menubar = Menu(gui, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')
help = Menu(menubar, tearoff=0)
help.add_command(label="Local Config", command=openLocalConfig)
menubar.add_cascade(label="Options", menu=help)
gui.config(menu=menubar)

def setPumpIP(event):
    global pumpIP, sendParameters2
    pumpIP=pumpIP_var.get()
    pumpIPText.config(text="Pump IP: "+ pumpIP)
    pumpIP_var.set('')
    sendParameters2 = 1
    return
pumpIP_var = tk.StringVar() 
expression_field = tk.Entry(gui, font=(12), relief="groove", textvariable=pumpIP_var, borderwidth=10)
expression_field.grid(row=1, column=0, columnspan=2)
expression_field.bind('<Return>',setPumpIP)
expression_field.icursor('end')
pumpIP_var.set('')
expression_field.update()
pumpIPText = tk.Label(gui, text="Connecting Pump", height=2, width=40, font='12', fg='black', bg='white', relief="groove")
pumpIPText.grid(row=1, column=2, columnspan=2)
pumpIPText.update()

def setrotTableIP(event):
    global rotTableIP, sendParameters1
    rotTableIP=rotTableIP_var.get()
    rotTableIPText.config(text="Rotary Table IP: "+ rotTableIP)
    rotTableIP_var.set('')
    sendParameters1 = 1
    return
rotTableIP_var = tk.StringVar() 
expression_field5 = tk.Entry(gui, font=(12), relief="groove", textvariable=rotTableIP_var, borderwidth=10)
expression_field5.grid(row=1, column=4, columnspan=2)
expression_field5.bind('<Return>',setrotTableIP)
expression_field5.icursor('end')
rotTableIP_var.set('')
expression_field5.update()
rotTableIPText = tk.Label(gui, text="Connecting Rotary Table", height=2, width=40, font='12', fg='black', bg='white', relief="groove")
rotTableIPText.grid(row=1, column=6, columnspan=2)
rotTableIPText.update()


if devMode == '1':
    def webSerialFunction():
        global enableWebserial
        if enableWebserial == 0:
            ws1.send("wser:1")
            print("rotTable: "+ ws1.recv())
            sleep(sleepTime)
            ws2.send("wser:1")
            print("pump: " + ws2.recv())
            sleep(sleepTime)
            enableWebserial = 1
            webSerialButton.config(text='Disable Webserial')
        else:
            ws1.send("wser:0")
            print("rotTable: "+ ws1.recv())
            sleep(sleepTime)
            ws2.send("wser:0")
            print("pump: " + ws2.recv())
            sleep(sleepTime)
            enableWebserial = 0
            webSerialButton.config(text='Enable Webserial')

    webSerialButton= Button(gui,text='Enable Webserial',font='12',fg='white',bg='dark blue',borderwidth=5,command=webSerialFunction,height=1,width=15)
    webSerialButton.grid(row=8,column=4,columnspan=2)
    webSerialButton.update()
    
    def setPumpSpeed(event):
        global pumpSpeed, sendParameters2
        pumpSpeed=pumpSpeed_var.get()
        pumpSpeedText.config(text="Pump Speed: "+ pumpSpeed)
        pumpSpeed_var.set('')
        sendParameters2 = 1
        return
    pumpSpeed_var = tk.StringVar() 
    expression2_field = tk.Entry(gui, font=(12), relief="groove", textvariable=pumpSpeed_var, borderwidth=10)
    expression2_field.grid(row=2, column=0, columnspan=2)
    expression2_field.bind('<Return>',setPumpSpeed)
    expression2_field.icursor('end')
    pumpSpeed_var.set('')
    expression2_field.update()
    pumpSpeedText = tk.Label(gui, text="Pump Speed: "+ pumpSpeed, height=2, width=40, font='12', fg='black', bg='#3399ff', relief="groove")
    pumpSpeedText.grid(row=2, column=2, columnspan=2)
    pumpSpeedText.update()

    def setManualSpeed(event):
        global manualSpeed, sendParameters2
        manualSpeed=manualSpeed_var.get()
        manualSpeedText.config(text="Manual Speed: "+ manualSpeed)
        manualSpeed_var.set('')
        sendParameters2 = 1
        return
    manualSpeed_var = tk.StringVar() 
    expression11_field = tk.Entry(gui, font=(12), relief="groove", textvariable=manualSpeed_var, borderwidth=10)
    expression11_field.grid(row=8, column=0, columnspan=2)
    expression11_field.bind('<Return>',setManualSpeed)
    expression11_field.icursor('end')
    manualSpeed_var.set('')
    expression11_field.update()
    manualSpeedText = tk.Label(gui, text="Manual Speed: "+ manualSpeed, height=2, width=40, font='12', fg='black', bg='#3399ff', relief="groove")
    manualSpeedText.grid(row=8, column=2, columnspan=2)
    manualSpeedText.update()

    def setPumpSteps(event):
        global pumpSteps, sendParameters2
        pumpSteps=pumpSteps_var.get()
        pumpStepsText.config(text="Pump Steps: "+ pumpSteps)
        pumpSteps_var.set('')
        sendParameters2 = 1
        return
    pumpSteps_var = tk.StringVar() 
    expression3_field = tk.Entry(gui, font=(12), relief="groove", textvariable=pumpSteps_var, borderwidth=10)
    expression3_field.grid(row=3, column=0, columnspan=2)
    expression3_field.bind('<Return>',setPumpSteps)
    expression3_field.icursor('end')
    pumpSteps_var.set('')
    expression3_field.update()
    pumpStepsText = tk.Label(gui, text="Pump Steps: "+ pumpSteps, height=2, width=40, font='12', fg='black', bg='#3399ff', relief="groove")
    pumpStepsText.grid(row=3, column=2, columnspan=2)
    pumpStepsText.update()


    def setPrimeSpeed(event):
        global primeSpeed, sendParameters2
        primeSpeed=primeSpeed_var.get()
        primeSpeedText.config(text="Prime Speed: "+ primeSpeed)
        primeSpeed_var.set('')
        sendParameters2 = 1
        return
    primeSpeed_var = tk.StringVar() 
    expression12_field = tk.Entry(gui, font=(12), relief="groove", textvariable=primeSpeed_var, borderwidth=10)
    expression12_field.grid(row=6, column=0, columnspan=2)
    expression12_field.bind('<Return>',setPrimeSpeed)
    expression12_field.icursor('end')
    primeSpeed_var.set('')
    expression12_field.update()
    primeSpeedText = tk.Label(gui, text="Prime Speed: "+ primeSpeed, height=2, width=40, font='12', fg='black', bg='#3399ff', relief="groove")
    primeSpeedText.grid(row=6, column=2, columnspan=2)
    primeSpeedText.update()

    def setPrimeSteps(event):
        global primeSteps, sendParameters2
        primeSteps=primeSteps_var.get()
        primeStepsText.config(text="Prime Steps: "+ primeSteps)
        primeSteps_var.set('')
        sendParameters2 = 1
        return
    primeSteps_var = tk.StringVar() 
    expression13_field = tk.Entry(gui, font=(12), relief="groove", textvariable=primeSteps_var, borderwidth=10)
    expression13_field.grid(row=6, column=4, columnspan=2)
    expression13_field.bind('<Return>',setPrimeSteps)
    expression13_field.icursor('end')
    primeSteps_var.set('')
    expression13_field.update()
    primeStepsText = tk.Label(gui, text="Prime Steps: "+ primeSteps, height=2, width=40, font='12', fg='black', bg='#3399ff', relief="groove")
    primeStepsText.grid(row=6, column=6, columnspan=2)
    primeStepsText.update()




    def setDeprimeSpeed(event):
        global deprimeSpeed, sendParameters2
        deprimeSpeed=deprimeSpeed_var.get()
        deprimeSpeedText.config(text="Deprime Speed: "+ deprimeSpeed)
        deprimeSpeed_var.set('')
        sendParameters2 = 1
        return
    deprimeSpeed_var = tk.StringVar() 
    expression14_field = tk.Entry(gui, font=(12), relief="groove", textvariable=deprimeSpeed_var, borderwidth=10)
    expression14_field.grid(row=7, column=0, columnspan=2)
    expression14_field.bind('<Return>',setDeprimeSpeed)
    expression14_field.icursor('end')
    deprimeSpeed_var.set('')
    expression14_field.update()
    deprimeSpeedText = tk.Label(gui, text="Deprime Speed: "+ deprimeSpeed, height=2, width=40, font='12', fg='black', bg='#3399ff', relief="groove")
    deprimeSpeedText.grid(row=7, column=2, columnspan=2)
    deprimeSpeedText.update()

    def setDeprimeSteps(event):
        global deprimeSteps, sendParameters2
        deprimeSteps=deprimeSteps_var.get()
        deprimeStepsText.config(text="Deprime Steps: "+ deprimeSteps)
        deprimeSteps_var.set('')
        sendParameters2 = 1
        return
    deprimeSteps_var = tk.StringVar() 
    expression15_field = tk.Entry(gui, font=(12), relief="groove", textvariable=deprimeSteps_var, borderwidth=10)
    expression15_field.grid(row=7, column=4, columnspan=2)
    expression15_field.bind('<Return>',setDeprimeSteps)
    expression15_field.icursor('end')
    deprimeSteps_var.set('')
    expression15_field.update()
    deprimeStepsText = tk.Label(gui, text="Deprime Steps: "+ deprimeSteps, height=2, width=40, font='12', fg='black', bg='#3399ff', relief="groove")
    deprimeStepsText.grid(row=7, column=6, columnspan=2)
    deprimeStepsText.update()

    def setPumpHalfStep(event):
        global pumpHalfStep, sendParameters2
        pumpHalfStep=pumpHalfStep_var.get()
        pumpHalfStepText.config(text="Pump HalfStep: "+ pumpHalfStep)
        pumpHalfStep_var.set('')
        sendParameters2 = 1
        return
    pumpHalfStep_var = tk.StringVar() 
    expression4_field = tk.Entry(gui, font=(12), relief="groove", textvariable=pumpHalfStep_var, borderwidth=10)
    expression4_field.grid(row=4, column=0, columnspan=2)
    expression4_field.bind('<Return>',setPumpHalfStep)
    expression4_field.icursor('end')
    pumpHalfStep_var.set('')
    expression4_field.update()
    pumpHalfStepText = tk.Label(gui, text="Pump HalfStep: "+ pumpHalfStep, height=2, width=40, font='12', fg='black', bg='#3399ff', relief="groove")
    pumpHalfStepText.grid(row=4, column=2, columnspan=2)
    pumpHalfStepText.update()

    def setrotTableSpeed(event):
        global rotTableSpeed, sendParameters1
        rotTableSpeed=rotTableSpeed_var.get()
        rotTableSpeedText.config(text="Rotary Table Speed: "+ rotTableSpeed)
        rotTableSpeed_var.set('')
        sendParameters1 = 1
        return
    rotTableSpeed_var = tk.StringVar() 
    expression6_field = tk.Entry(gui, font=(12), relief="groove", textvariable=rotTableSpeed_var, borderwidth=10)
    expression6_field.grid(row=2, column=4, columnspan=2)
    expression6_field.bind('<Return>',setrotTableSpeed)
    expression6_field.icursor('end')
    rotTableSpeed_var.set('')
    expression6_field.update()
    rotTableSpeedText = tk.Label(gui, text="Rotary Table Speed: "+ rotTableSpeed, height=2, width=40, font='12', fg='black', bg='#3399ff', relief="groove")
    rotTableSpeedText.grid(row=2, column=6, columnspan=2)
    rotTableSpeedText.update()

    def setrotTableSteps(event):
        global rotTableSteps, sendParameters1
        rotTableSteps = rotTableSteps_var.get()
        if rotTableSteps == 'inf':
            rotTableStepsText.config(text="inf disabled on table")
            rotTableSteps1 = 0
        else:
            rotTableStepsText.config(text="Rotary Table Steps: "+ rotTableSteps)
        rotTableSteps_var.set('')
        sendParameters1 = 1
        return
    rotTableSteps_var = tk.StringVar() 
    expression7_field = tk.Entry(gui, font=(12), relief="groove", textvariable=rotTableSteps_var, borderwidth=10)
    expression7_field.grid(row=3, column=4, columnspan=2)
    expression7_field.bind('<Return>',setrotTableSteps)
    expression7_field.icursor('end')
    rotTableSteps_var.set('')
    expression7_field.update()
    rotTableStepsText = tk.Label(gui, text="Rotary Table Steps: "+ rotTableSteps, height=2, width=40, font='12', fg='black', bg='#3399ff', relief="groove")
    rotTableStepsText.grid(row=3, column=6, columnspan=2)
    rotTableStepsText.update()

    def setrotTableHalfStep(event):
        global rotTableHalfStep, sendParameters1
        rotTableHalfStep=rotTableHalfStep_var.get()
        rotTableHalfStepText.config(text="Rotary Table HalfStep: "+ rotTableHalfStep)
        rotTableHalfStep_var.set('')
        sendParameters1 = 1
        return
    rotTableHalfStep_var = tk.StringVar() 
    expression8_field = tk.Entry(gui, font=(12), relief="groove", textvariable=rotTableHalfStep_var, borderwidth=10)
    expression8_field.grid(row=4, column=4, columnspan=2)
    expression8_field.bind('<Return>',setrotTableHalfStep)
    expression8_field.icursor('end')
    rotTableHalfStep_var.set('')
    expression8_field.update()
    rotTableHalfStepText = tk.Label(gui, text="Rotary Table HalfStep: "+ rotTableHalfStep, height=2, width=40, font='12', fg='black', bg='#3399ff', relief="groove")
    rotTableHalfStepText.grid(row=4, column=6, columnspan=2)
    rotTableHalfStepText.update()

    
    def setEncoders(event):
        global enableEncoders, sendParameters1, sendParameters2, tablePosText, pumpPosText
        enableEncoders=enableEncoders_var.get()
        enableEncodersText.config(text="enableEncoders: "+ enableEncoders)
        enableEncoders_var.set('')
        sendParameters1 = 1 # send to both
        sendParameters2 = 1
        if enableEncoders == '0':
            tablePosText.destroy()
            pumpPosText.destroy()
        if enableEncoders == '1':
            encoderPositionText()
        return
    enableEncoders_var = tk.StringVar() 
    expression9_field = tk.Entry(gui, font=(12), relief="groove", textvariable=enableEncoders_var, borderwidth=10)
    expression9_field.grid(row=5, column=0, columnspan=2)
    expression9_field.bind('<Return>',setEncoders)
    expression9_field.icursor('end')
    enableEncoders_var.set('')
    expression9_field.update()
    enableEncodersText = tk.Label(gui, text="enableEncoders: "+ enableEncoders, height=2, width=40, font='12', fg='black', bg='#3399ff', relief="groove")
    enableEncodersText.grid(row=5, column=2, columnspan=2)
    enableEncodersText.update()


    def reEncoders(event):
        global resetEncoders
        resetEncoders=resetEncoders_var.get()
        resetEncodersText.config(text="resetEncoders: "+ resetEncoders)
        resetEncoders_var.set('')
        return
    resetEncoders_var = tk.StringVar() 
    expression10_field = tk.Entry(gui, font=(12), relief="groove", textvariable=resetEncoders_var, borderwidth=10)
    expression10_field.grid(row=5, column=4, columnspan=2)
    expression10_field.bind('<Return>',reEncoders)
    expression10_field.icursor('end')
    resetEncoders_var.set('')
    expression10_field.update()
    resetEncodersText = tk.Label(gui, text="resetEncoders: "+ resetEncoders, height=2, width=40, font='12', fg='black', bg='#3399ff', relief="groove")
    resetEncodersText.grid(row=5, column=6, columnspan=2)
    resetEncodersText.update()
        
def sendParams1():
    global sendParameters1
    # send parameters
    if sendParameters1 == 1 :
        ws1.send("spee: " + rotTableSpeed)
        print('rotTable: ' + ws1.recv())
        sleep(sleepTime)
        ws1.send("half: " + rotTableHalfStep)
        print('rotTable: ' + ws1.recv())
        sleep(sleepTime)
        ws1.send("enen: " + enableEncoders)
        print('rotTable: ' + ws1.recv())
        sleep(sleepTime)
        ws1.send("prim: " + rotTablePrimary)
        print('rotTable: ' + ws1.recv())
        sleep(sleepTime)
        sendParameters1 = 0
def sendParams2():
    global sendParameters2
    # send parameters
    if sendParameters2 == 1 :
        ws2.send("spee: " + pumpSpeed)
        print('Pump: ' + ws2.recv())
        sleep(sleepTime)
        ws2.send("half: " + pumpHalfStep)
        print('Pump: ' + ws2.recv())
        sleep(sleepTime)
        ws2.send("enen: " + enableEncoders)
        print('Pump: ' + ws2.recv())
        sleep(sleepTime)
        ws2.send("prim: " + pumpPrimary)
        print('Pump: ' + ws2.recv())
        sleep(sleepTime)
        ws2.send("prsp: " + primeSpeed)
        print('Pump: ' + ws2.recv())
        sleep(sleepTime)
        ws2.send("prst: " + primeSteps)
        print('Pump: ' + ws2.recv())
        sleep(sleepTime)
        ws2.send("desp: " + deprimeSpeed)
        print('Pump: ' + ws2.recv())
        sleep(sleepTime)
        ws2.send("dest: " + deprimeSteps)
        print('Pump: ' + ws2.recv())
        sleep(sleepTime)
        sendParameters2 = 0

def primePump():
    ws2.send("stpr:") # runs pump priming
    print('Pump: ' + ws2.recv())
    msgRecv2 = ''
    while msgRecv2 != 'priming done':
        msgRecv2 = ws2.recv()
        print("pump: " + msgRecv2)
    #sleep(sleepTime)
    # try to keep delays to a minimum
    
def deprimePump():
    ws2.send("stde:") # runs pump depriming
    print('Pump: ' + ws2.recv())
    msgRecv2 = ''
    while msgRecv2 != 'depriming done':
        msgRecv2 = ws2.recv()
        print("pump: " + msgRecv2)
    sleep(sleepTime)
    
        
def rcv(ws1,ws2): # ws1=rotTable ; ws2=pump
    global pumpPosText, tablePosText, pumpSteps, rotTableSteps
    try :
        if enableEncoders == '1' and resetEncoders == '1':
            tablePosText.config(text='tablePos: 0')
            pumpPosText.config(text='pumpPos: 0')
            ws1.send("reset")
            print('rotTable: ' + ws1.recv())
            sleep(sleepTime)
            ws2.send("reset")
            print('Pump: ' + ws2.recv())
            sleep(sleepTime)
        sendParams1() # only send params if they have changed
        sendParams2()
        ws1.send("zero:0") # sets rotTable stepper current position to 0
        print('rotTable: ' + ws1.recv())
        sleep(sleepTime)
        
        primePump() # will also set current pos to zero

        # send secondary stepper first (waits on primary GPIO sync signal)
        if pumpSteps == "inf":
            ws2.send("gogo:") # pump non-block / non-accel runforever til stop: is called
        else: 
            ws2.send("goto:" + pumpSteps)
        print('Pump: ' + ws2.recv())
        sleep(sleepTime)
        ws1.send("goto:" + rotTableSteps)
        print('rotTable: ' + ws1.recv())
        sleep(sleepTime)
        # wait for rotary table to send done signal
        msgRecv = ws1.recv()
        msgRecv = msgRecv.split(',')
        if msgRecv[0] == 'moving done':
            print("rotTable: " + msgRecv[0])
            print("rotTable: " + msgRecv[1])
            if enableEncoders == '1':
                tablePosText.config(text='tablePos: '+ msgRecv[1])
        msgRecv2 = ws2.recv()
        msgRecv2 = msgRecv2.split(',')
        if msgRecv2[0] == 'moving done':
            print("pump: " + msgRecv2[0])
            print("pump: " + msgRecv2[1])
            if enableEncoders == '1':
                pumpPosText.config(text='pumpPos:' + msgRecv2[1])
        deprimePump()
        # display logo to indicate everything is done    
        ws1.send("logo:")
        print("rotTable: "+ ws1.recv())
        sleep(sleepTime)
        ws2.send("logo:")
        print("pump: " + ws2.recv())
    except:
        try:
            ws2.send("stop:") # pump non-block / non-accel runforever til stop: is called
            print("pump: " + ws2.recv())
            connectSteppers()
        except:
            connectSteppers()
        
def wifiThread():
    t1=Thread(target=rcv(ws1,ws2))
    t1.start() 
    return
def runFunction():
    wifiThread()
    return
runButton= Button(gui,text='Run',font='12',fg='white',bg='blue',borderwidth=5,command=runFunction,height=1,width=10)
runButton.grid(row=0,column=0)
runButton.update()

def saveFunction():
    with open('Config.txt', 'w') as f:
        f.write('[Config]\n')
        f.write('pumpIP = ' + pumpIP + '\n')
        f.write('pumpSpeed = ' + pumpSpeed + '\n')
        f.write('pumpSteps = ' + pumpSteps + '\n')
        f.write('pumpHalfStep = ' + pumpHalfStep + '\n')
        f.write('rotTableIP = ' + rotTableIP + '\n')
        f.write('rotTableSpeed = ' + rotTableSpeed + '\n')
        f.write('rotTableSteps = ' + rotTableSteps + '\n')
        f.write('rotTableHalfStep = ' + rotTableHalfStep + '\n')
        f.write('enableEncoders = ' + enableEncoders + '\n')
        f.write('resetEncoders = ' + resetEncoders + '\n')
        f.write('manualSpeed = ' + manualSpeed + '\n')
        f.write('primeSpeed = ' + primeSpeed + '\n')
        f.write('primeSteps = ' + primeSteps + '\n')
        f.write('deprimeSpeed = ' + deprimeSpeed + '\n')
        f.write('deprimeSteps = ' + deprimeSteps + '\n')
        f.write('# only set in config\n# warning setting both as primary will cause GPIOs to short\n# remove GPIO cable if setting both to primary\n')
        f.write('rotTablePrimary = ' + rotTablePrimary + '\n')
        f.write('pumpPrimary = ' + pumpPrimary + '\n')
        f.write('devMode = ' + devMode + '\n')
    
saveButton= Button(gui,text='Save Config',font='12',fg='white',bg='blue',borderwidth=5,command=saveFunction,height=1,width=10)
saveButton.grid(row=0,column=1)
saveButton.update()

def closeFunction():
    try:
        try: # if rotTable is closed try to close pump
            ws1.send("print")
            ws1.close()
        except:
            pass
        ws2.send("print")
        ws2.close()
        gui.destroy()
    except:
        gui.destroy()
closeButton= Button(gui,text='Close',font='12',fg='white',bg='dark blue',borderwidth=5,command=closeFunction,height=1,width=15)
closeButton.grid(row=0,column=2)
closeButton.update()

def runPump():
    global manualPump, sendParameters2
    try:
        if manualPump == 0:
            ws2.send("spee:" + manualSpeed)
            print("pump: " + ws2.recv())
            sleep(sleepTime)
            ws2.send("manu:1")
            print("pump: " + ws2.recv())
            sleep(sleepTime)
            manualPump = 1
            manualPumpButton.config(text='Stop Pump')
        else:
            ws2.send("stop:")
            print("pump: " + ws2.recv())
            sleep(sleepTime)
            print("pump: " + ws2.recv())
            sleep(sleepTime)
            manualPump = 0
            manualPumpButton.config(text='Manual Pump')
            sendParameters2 = 1 # need to re update update speed after running in manual mode
        
    except:
        connect2()
manualPumpButton= Button(gui,text='Manual Pump',font='12',fg='white',bg='dark blue',borderwidth=5,command=runPump,height=1,width=15)
manualPumpButton.grid(row=0,column=3)
manualPumpButton.update()

def encoderPositionText():
    global tablePosText, pumpPosText, enableEncoders
    if enableEncoders == '1':
        tablePosText = tk.Label(gui, text="pumpPos: 0", height=2, width=30, font='12', fg='white', bg='blue', relief="groove")
        tablePosText.grid(row=0, column=4, columnspan=2)
        tablePosText.update()

        pumpPosText = tk.Label(gui, text="tablePos: 0", height=2, width=30, font='12', fg='white', bg='blue', relief="groove")
        pumpPosText.grid(row=0, column=6, columnspan=2)
        pumpPosText.update()
        
encoderPositionText()
    
####IMG####
load= Image.open("logo4.ppm")
render = ImageTk.PhotoImage(load)
img = Label(gui, borderwidth=0, image=render)
img.grid(row=8, column=6, columnspan=2)
img.update()

def connect1():
    global ws1, rotTableIPText
    try:
        ws1 = websocket.WebSocket()
        ws1.connect("ws://"+ rotTableIP +"/python") # pump
        sendParams1() # send one time only parameters (unless devMode changes them)
        rotTableIPText.config(text="Rotary Table IP: "+ rotTableIP , bg='#3399ff')
    except:
        rotTableIPText.config(text="Rotary Table Failed: "+ rotTableIP, bg='red')
    return
def connect2():
    global ws2, pumpIPText
    try:
        ws2 = websocket.WebSocket()
        ws2.connect("ws://"+ pumpIP +"/python") # rotary table
        sendParams2() # send one time only parameters (unless devMode changes them)
        pumpIPText.config(text="Pump IP: "+ pumpIP, bg='#3399ff')
    except:
        pumpIPText.config(text="Pump Failed: "+ pumpIP, bg='red')
    return

def connectSteppers():
    connect1()
    connect2()
    return
def connectThread():
    t1=Thread(target=connectSteppers)
    t1.start() 
    return
connectThread()

gui.mainloop() # start the GUI
