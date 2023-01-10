import arduino # requires pyserial, sleep, configparser
import tkinter as tk # handles GUI
from tkinter import * # handles GUI
from tkinter import filedialog # handles opening Results and Config file paths
from tkinter import ttk # handles Combobox
from time import sleep # handles delay
#import os  # for working with opening files with applications like excel and notepad
from threading import * # handles threading so GUI doesnt freeze during main functions
configFolder=arduino.configFolder # config file path
passFail = 0 # if error, use this index to skip back to main
index = 0

# def openConfig():
#     os.startfile('folderConfig.txt')

def connectArduino():
    global passFail,failureMessage,usbPort
    arduino.connectArduino() # connects to arduino through arduino module
    if arduino.passFail==1:
        passFail=1
        failureMessage="Stator Winder Tester USB Failed Connection"
        usb.config(fg='white', bg='red')
        return
    else:
        usb.config(fg='white', bg='purple',text= 'USB OK')
        return

    
def startA():
    global turn
    arduino.command('strt:a')
    return

def startB():
    global turn
    arduino.command('strt:B')
    return

def startC():
    global turn
    arduino.command('strt:c')
    return
def resetLbls():
    label88.config(bg="white",text='')
    label8.config(bg="white",text='')
    label77.config(bg="white",text='')
    label7.config(bg="white",text='')
    label66.config(bg="white",text='')
    label6.config(bg="white",text='')
    label55.config(bg="white",text='')
    label5.config(bg="white",text='')
    label44.config(bg="white",text='')
    label4.config(bg="white",text='')
    label33.config(bg="white",text='')
    label3.config(bg="white",text='')
    label22.config(bg="white",text='')
    label2.config(bg="white",text='')
    label11.config(bg="white",text='')
    label1.config(bg="white",text='')
    label88a.config(bg="white",text='')
    label8a.config(bg="white",text='')
    label77a.config(bg="white",text='')
    label7a.config(bg="white",text='')
    label66a.config(bg="white",text='')
    label6a.config(bg="white",text='')
    label55a.config(bg="white",text='')
    label5a.config(bg="white",text='')
    label44a.config(bg="white",text='')
    label4a.config(bg="white",text='')
    label33a.config(bg="white",text='')
    label3a.config(bg="white",text='')
    label22a.config(bg="white",text='')
    label2a.config(bg="white",text='')
    label11a.config(bg="white",text='')
    label1a.config(bg="white",text='')

def resetImg():
    global img1a,img2a,img3a,img4a,img5a,img6a,img7a,img8a,img9a,img10a,img11a,img12a,img13a,img14a,img15a,img16a,img1b,img2b,img3b,img4b,img5b,img6b,img7b,img8b,img9b,img10b,img11b,img12b,img13b,img14b,img15b,img16b,img1c,img2c,img3c,img4c,img5c,img6c,img7c,img8c,img9c,img10c,img11c,img12c,img13c,img14c,img15c,img16c    
    img1a.grid_forget()
    img2a.grid_forget()
    img3a.grid_forget()
    img4a.grid_forget()
    img5a.grid_forget()
    img6a.grid_forget()
    img7a.grid_forget()
    img8a.grid_forget()
    img9a.grid_forget()
    img10a.grid_forget()
    img11a.grid_forget()
    img12a.grid_forget()
    img13a.grid_forget()
    img14a.grid_forget()
    img15a.grid_forget()
    img16a.grid_forget()
    img1b.grid_forget()
    img2b.grid_forget()
    img3b.grid_forget()
    img4b.grid_forget()
    img5b.grid_forget()
    img6b.grid_forget()
    img7b.grid_forget()
    img8b.grid_forget()
    img9b.grid_forget()
    img10b.grid_forget()
    img11b.grid_forget()
    img12b.grid_forget()
    img13b.grid_forget()
    img14b.grid_forget()
    img15b.grid_forget()
    img16b.grid_forget()
    img1c.grid_forget()
    img2c.grid_forget()
    img3c.grid_forget()
    img4c.grid_forget()
    img5c.grid_forget()
    img6c.grid_forget()
    img7c.grid_forget()
    img8c.grid_forget()
    img9c.grid_forget()
    img10c.grid_forget()
    img11c.grid_forget()
    img12c.grid_forget()
    img13c.grid_forget()
    img14c.grid_forget()
    img15c.grid_forget()
    img16c.grid_forget()
            
def labels(section,phase,currentTurn):
    if phase == 'a1' or phase == 'B1' or phase == 'c1':
        if currentTurn == 1.0:
            resetImg()
            label88.config(fg='black', bg='white', text=section[15])
            label8.config(fg='black', bg='white', text=section[14])
            label77.config(fg='black', bg='white', text=section[13])
            label7.config(fg='black', bg='white', text=section[12])
            label66.config(fg='black', bg='white', text=section[11])
            label6.config(fg='black', bg='white', text=section[10])
            label55.config(fg='black', bg='white', text=section[9])
            label5.config(fg='black', bg='white', text=section[8])
            label44.config(fg='black', bg='white', text=section[7])
            label4.config(fg='black', bg='white', text=section[6])
            label33.config(fg='black', bg='white', text=section[5])
            label3.config(fg='black', bg='white', text=section[4])
            label22.config(fg='black', bg='white', text=section[3])
            label2.config(fg='black', bg='white', text=section[2])
            label11.config(fg='black', bg='white', text=section[1])
            label1.config(fg='black', bg='#3399ff', text=section[0])

            label88a.config(fg='black', bg='white', text='')
            label77a.config(fg='black', bg='white', text='')
            label66a.config(fg='black', bg='white', text='')
            label55a.config(fg='black', bg='white', text='')
            label44a.config(fg='black', bg='white', text='')
            label33a.config(fg='black', bg='white', text='')
            label22a.config(fg='black', bg='white', text='')
            label11a.config(fg='black', bg='white', text='')

            label8a.config(fg='black', bg='white', text='')
            label7a.config(fg='black', bg='white', text='')
            label6a.config(fg='black', bg='white', text='')
            label5a.config(fg='black', bg='white', text='')
            label4a.config(fg='black', bg='white', text='')
            label3a.config(fg='black', bg='white', text='')
            label2a.config(fg='black', bg='white', text='')
            label1a.config(fg='black', bg='white', text=currentTurn)
        
        elif currentTurn > 0:
            label1a.config(fg='black', bg='white', text=currentTurn)
            
        elif currentTurn == 0:
            text.config(text='Stator is moving on next step', bg = 'orange')
            
    elif phase == 'A1' or phase == 'b1' or phase == 'C1':
        if currentTurn > 0:
            label1a.config(bg='#3399ff')
            label11.config(bg='#3399ff')
            label11a.config(fg='black', bg='white', text=currentTurn)
            if phase == 'A1':
                img1a.grid(row=18, column=2)
            if phase == 'b1':
                img1b.grid(row=18, column=3)
            if phase == 'C1':
                img1c.grid(row=18, column=4)
        else:
            text.config(text='Stator is moving on next step', bg = 'orange')
            
    elif phase == 'a2' or phase == 'B2' or phase == 'c2':
        if currentTurn > 0:
            label11a.config(bg='#3399ff')
            label2.config(bg='#3399ff')
            label2a.config(fg='black', bg='white', text=currentTurn)
            if phase == 'a2':
                img2a.grid(row=17, column=2)
            if phase == 'B2':
                img2b.grid(row=17, column=3)
            if phase == 'c2':
                img2c.grid(row=17, column=4)
        else:
            text.config(text='Stator is moving on next step', bg = 'orange')
    elif phase == 'A2' or phase == 'b2' or phase == 'C2':
        if currentTurn > 0:
            label2a.config(bg='#3399ff')
            label22.config(bg='#3399ff')
            label22a.config(fg='black', bg='white', text=currentTurn)
            if phase == 'A2':
                img3a.grid(row=16, column=2)
            if phase == 'b2':
                img3b.grid(row=16, column=3)
            if phase == 'C2':
                img3c.grid(row=16, column=4)
        else:
            text.config(text='Stator is moving on next step', bg = 'orange')
    elif phase == 'A3' or phase == 'b3' or phase == 'C3':
        if currentTurn > 0:
            label22a.config(bg='#3399ff')
            label3.config(bg='#3399ff')
            label3a.config(fg='black', bg='white', text=currentTurn)
            if phase == 'A3':
                img4a.grid(row=15, column=2)
            if phase == 'b3':
                img4b.grid(row=15, column=3)
            if phase == 'C3':
                img4c.grid(row=15, column=4)
        else:
            text.config(text='Stator is moving on next step', bg = 'orange')
    elif phase == 'a3' or phase == 'B3' or phase == 'c3':
        if currentTurn > 0:
            label3a.config(bg='#3399ff')
            label33.config(bg='#3399ff')
            label33a.config(fg='black', bg='white', text=currentTurn)
            if phase == 'a3':
                img5a.grid(row=14, column=2)
            if phase == 'B3':
                img5b.grid(row=14, column=3)
            if phase == 'c3':
                img5c.grid(row=14, column=4)
        else:
            text.config(text='Stator is moving on next step', bg = 'orange')
    elif phase == 'A4' or phase == 'b4' or phase == 'C4':
        if currentTurn > 0:
            label33a.config(bg='#3399ff')
            label4.config(bg='#3399ff')
            label4a.config(fg='black', bg='white', text=currentTurn)
            if phase == 'A4':
                img6a.grid(row=13, column=2)
            if phase == 'b4':
                img6b.grid(row=13, column=3)
            if phase == 'C4':
                img6c.grid(row=13, column=4)
        else:
            text.config(text='Stator is moving on next step', bg = 'orange')
    elif phase == 'a4' or phase == 'B4' or phase == 'c4':
        if currentTurn > 0:
            label4a.config(bg='#3399ff')
            label44.config(bg='#3399ff')
            label44a.config(fg='black', bg='white', text=currentTurn)
            if phase == 'a4':
                img7a.grid(row=12, column=2)
            if phase == 'B4':
                img7b.grid(row=12, column=3)
            if phase == 'c4':
                img7c.grid(row=12, column=4)
        else:
            text.config(text='Stator is moving on next step', bg = 'orange')
    elif phase == 'a5' or phase == 'B5' or phase == 'c5':
        if currentTurn > 0:
            label44a.config(bg='#3399ff')
            label5.config(bg='#3399ff')
            label5a.config(fg='black', bg='white', text=currentTurn)
            if phase == 'a5':
                img8a.grid(row=11, column=2)
            if phase == 'B5':
                img8b.grid(row=11, column=3)
            if phase == 'c5':
                img8c.grid(row=11, column=4)
        else:
            text.config(text='Stator is moving on next step', bg = 'orange')
    elif phase == 'A5' or phase == 'b5' or phase == 'C5':
        if currentTurn > 0:
            label5a.config(bg='#3399ff')
            label55.config(bg='#3399ff')
            label55a.config(fg='black', bg='white', text=currentTurn)
            if phase == 'A5':
                img9a.grid(row=10, column=2)
            if phase == 'b5':
                img9b.grid(row=10, column=3)
            if phase == 'C5':
                img9c.grid(row=10, column=4)
        else:
            text.config(text='Stator is moving on next step', bg = 'orange')
    elif phase == 'a6' or phase == 'B6' or phase == 'c6':
        if currentTurn > 0:
            label55a.config(bg='#3399ff')
            label6.config(bg='#3399ff')
            label6a.config(fg='black', bg='white', text=currentTurn)
            if phase == 'a6':
                img10a.grid(row=9, column=2)
            if phase == 'B6':
                img10b.grid(row=9, column=3)
            if phase == 'c6':
                img10c.grid(row=9, column=4)
        else:
            text.config(text='Stator is moving on next step', bg = 'orange')
    elif phase == 'A6' or phase == 'b6' or phase == 'C6':
        if currentTurn > 0:
            label6a.config(bg='#3399ff')
            label66.config(bg='#3399ff')
            label66a.config(fg='black', bg='white', text=currentTurn)
            if phase == 'A6':
                img11a.grid(row=8, column=2)
            if phase == 'b6':
                img11b.grid(row=8, column=3)
            if phase == 'C6':
                img11c.grid(row=8, column=4)
        else:
            text.config(text='Stator is moving on next step', bg = 'orange')
    elif phase == 'A7' or phase == 'b7' or phase == 'C7':
        if currentTurn > 0:
            label66a.config(bg='#3399ff')
            label7.config(bg='#3399ff')
            label7a.config(fg='black', bg='white', text=currentTurn)
            if phase == 'A7':
                img12a.grid(row=7, column=2)
            if phase == 'b7':
                img12b.grid(row=7, column=3)
            if phase == 'C7':
                img12c.grid(row=7, column=4)
        else:
            text.config(text='Stator is moving on next step', bg = 'orange')
    elif phase == 'a7' or phase == 'B7' or phase == 'c7':
        if currentTurn > 0:
            label7a.config(bg='#3399ff')
            label77.config(bg='#3399ff')
            label77a.config(fg='black', bg='white', text=currentTurn)
            if phase == 'a7':
                img13a.grid(row=6, column=2)
            if phase == 'B7':
                img13b.grid(row=6, column=3)
            if phase == 'c7':
                img13c.grid(row=6, column=4)
        else:
            text.config(text='Stator is moving on next step', bg = 'orange')
    elif phase == 'A8' or phase == 'b8' or phase == 'C8':
        if currentTurn > 0:
            label77a.config(bg='#3399ff')
            label8.config(bg='#3399ff')
            label8a.config(fg='black', bg='white', text=currentTurn)
            if phase == 'A8':
                img14a.grid(row=5, column=2)
            if phase == 'b8':
                img14b.grid(row=5, column=3)
            if phase == 'C8':
                img14c.grid(row=5, column=4)
        else:
            text.config(text='Stator is moving on next step', bg = 'orange')
    elif phase == 'a8' or phase == 'B8' or phase == 'c8':
        if currentTurn > 0:
            label8a.config(bg='#3399ff')
            label88.config(bg='#3399ff')
            label88a.config(fg='black', bg='white', text=currentTurn)
            if phase == 'a8':
                img15a.grid(row=4, column=2)
            if phase == 'B8':
                img15b.grid(row=4, column=3)
            if phase == 'c8':
                img15c.grid(row=4, column=4)
        else:
            text.config(text='Stator is moving on next step', bg = 'orange')
            
##            img16a.grid(row=3, column=2)
##
##            img16b.grid(row=3, column=3)
##
##            img16c.grid(row=3, column=4)

def usbFailure():
    global failureMessage
    failUSB = tk.Tk()
    failUSB.title("Failure!!!")
    failUSB.rowconfigure(4, minsize=50, weight=1)       #about window row#, size, wieght
    failUSB.columnconfigure(2, minsize=100, weight=1)    #main window col#, size, wieght
    failUSB.geometry('610x140')
    #failUSB.wm_iconbitmap('LLC-LOGO.xbm')
    failUSB.config(bg='red')
    failLabel = tk.Label(failUSB, fg="black",bg='red',width=50, font=("Adobe",16), text=failureMessage)
    failLabel.grid(row=0, columnspan=1)
    
    failLabel3 = tk.Label(failUSB, fg="black",bg="red",width=50, font=("Adobe",16), text="Check USB Connection and restart GUI")
    failLabel3.grid(row=1, columnspan=1)
    text.config(text='USB Failed, Please restart GUI', bg = 'red')

    def destroy():
        failUSB.destroy()
        gui.destroy()

    btn_ok = tk.Button(failUSB, font=("Adobe",16),width=10, text="OK", command=destroy)
    btn_ok.grid(row=3, columnspan=1)
    failUSB.mainloop()

def reset():
    arduino.command('reset')
        
def about():
    window = tk.Tk()
    window.title("About")
    window.rowconfigure(0, minsize=400, weight=1) # about window row#, size, wieght
    #window.wm_iconbitmap('LLC-LOGO.xbm')
    window.geometry('1200x600')
    window.config(bg='#3399ff')
    message ='''
    --About the program--
    Stator Winder GUI
    Linear Labs, Inc.
    Author: Doug Gammill
    Date: 8/23/2022
    Copyright (c) 2022
    Aids in Winding Stators.
    Can be used stand alone or with a computer GUI.
    
    1. At any time press Estop to disengage stepper braking or movement.
    2. Ensure USB cable is connected to the PC.
    3. Ensure Linear Labs Stator Winder (gui) has indicated USB coms are good with device.
    4. Press encoder knob to offset stator pole manually.
    5. Hold UP button while rotating encoder knob to offset stator turn manually.
    6. Press encoder knob a second time to exit manual offset mode.
    6. Set number of turns per pole with GUI drop down box or enclosure up and down buttons.
    7. Reset everything by pressing up and down buttons at same time, also found in options.
    8. Press one of the phase A, B or C buttons to start winding.
    9. Momentary press the foot pedal to rotate stator half a turn.
    10. X rotational axis rotates half a turn with each press of foot pedal.
    11. Y rotational axis moves to next pole just before next pole wire is slotted.
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
for i in range(19):  ###rows = 17
    gui.columnconfigure(i, weight=1, minsize=110)
    gui.rowconfigure(i, weight=1, minsize=10)

    for j in range(0, 5): ###column = 7
        frame = tk.Frame(master=gui,relief=tk.RAISED,borderwidth=2)
        
gui.configure(background="Black") # set the background colour of GUI window
gui.title("Stator Winder") # set the title of GUI window
#gui.wm_iconbitmap('LLC-LOGO.xbm')
# set the configuration of GUI window
gui.geometry("552x700") # width by length
gui.resizable(width=True, height=True)

# menubar = Menu(gui, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')
# help = Menu(menubar, tearoff=0)  
# help.add_command(label="About", command=about)
# help.add_command(label="Config", command=openConfig)
# help.add_command(label="Reset", command=reset)
# menubar.add_cascade(label="Options", menu=help)
# gui.config(menu=menubar)

#text_var = tk.StringVar()
text=tk.Label(gui,font='10',width=40,relief='ridge',text='Setting Up USB, Please Wait',borderwidth=5)
text.grid(row=0, columnspan=4, ipadx=25)
text.update()

usb=tk.Label(gui,font='10',width=12,relief='ridge',text="USB",fg='black',bg='white',borderwidth=5)
usb.grid(row=0, column=4)
usb.update()

def display_selected(turns):
    global turn
    turns = current_value.get()
    turn=turns
    arduino.command('turn:'+str(turns))

label = tk.Label(fg="black",bg='#3399ff',relief='ridge',height=1,width=10,font='10',text='Turns:',borderwidth=8)
label.grid(row=2, column=0)
label.update()

OPTIONS = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
current_value= IntVar() # setting current_value for Integers
current_value.set('0') #### use this to set an option as the identifier
# dropdown = OptionMenu(gui,current_value,*OPTIONS,command=display_selected) # creating widget
# dropdown.config(width=5,borderwidth=3,relief='ridge')
# dropdown.grid(row=2, column=1)
# dropdown.update()
# slider = Scale(gui,from_=0,to=40,orient='horizontal',variable=current_value,command=display_selected)
# slider.config(width=6,borderwidth=1,relief='ridge')
# slider.grid(row=2, column=0, columnspan=2)
# slider.update()
dropdown = ttk.Combobox(gui, textvariable=current_value, font="Arial 18")
dropdown['values'] = (OPTIONS)# get first 3 letters of every month name
dropdown['state'] = 'readonly'# prevent typing a value
dropdown.bind("<<ComboboxSelected>>", display_selected)
dropdown.grid(row=2, column=1)
dropdown.update()

startAbutton= Button(gui,text='Start A',font='10',fg='black',bg='#81FF33',borderwidth=5,command=startA,height=1,width=10)
startAbutton.grid(row=2, column=2)
startAbutton.update()

startBbutton= Button(gui,text='Start B',font='10',fg='black',bg='#3379FF',borderwidth=5,command=startB,height=1,width=10)
startBbutton.grid(row=2,column=3)
startBbutton.update()

startCbutton= Button(gui,text='Start C',font='10',fg='black',bg='#FFFF33',borderwidth=5,command=startC,height=1,width=10)
startCbutton.grid(row=2, column=4)
startCbutton.update()

#### text labels
label88 = tk.Label(fg="black",bg='white',width=25,font='10', text='')
label88.grid(row=3, column=0,pady=5)
label88.update()

label8 = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label8.grid(row=4, column=0)
label8.update()

label77 = tk.Label(fg="black",bg='white',width=25,font=12, text='')
label77.grid(row=5, column=0)
label77.update()

label7 = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label7.grid(row=6, column=0)
label7.update()

label66 = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label66.grid(row=7, column=0)
label66.update()

label6 = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label6.grid(row=8, column=0)
label6.update()

label55 = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label55.grid(row=9, column=0)
label55.update()

label5 = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label5.grid(row=10, column=0)
label5.update()

label44 = tk.Label(fg="black",bg='white',width=25,font=12, text='')
label44.grid(row=11, column=0)
label44.update()

label4 = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label4.grid(row=12, column=0)
label4.update()

label33 = tk.Label(fg="black",bg='white',width=25,font=12, text='')
label33.grid(row=13, column=0)
label33.update()

label3 = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label3.grid(row=14, column=0)
label3.update()

label22 = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label22.grid(row=15, column=0)
label22.update()

label2 = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label2.grid(row=16, column=0)
label2.update()

label11 = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label11.grid(row=17, column=0)
label11.update()

label1 = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label1.grid(row=18, column=0)
label1.update()

label88a = tk.Label(fg="black",bg='white',width=25,font=12, text='')
label88a.grid(row=3, column=1)
label88a.update()

label8a = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label8a.grid(row=4, column=1)
label8a.update()

label77a = tk.Label(fg="black",bg='white',width=25,font=12, text='')
label77a.grid(row=5, column=1)
label77a.update()

label7a = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label7a.grid(row=6, column=1)
label7a.update()

label66a = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label66a.grid(row=7, column=1)
label66a.update()

label6a = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label6a.grid(row=8, column=1)
label6a.update()

label55a = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label55a.grid(row=9, column=1)
label55a.update()

label5a = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label5a.grid(row=10, column=1)
label5a.update()

label44a = tk.Label(fg="black",bg='white',width=25,font=12, text='')
label44a.grid(row=11, column=1)
label44a.update()

label4a = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label4a.grid(row=12, column=1)
label4a.update()

label33a = tk.Label(fg="black",bg='white',width=25,font=12, text='')
label33a.grid(row=13, column=1)
label33a.update()

label3a = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label3a.grid(row=14, column=1)
label3a.update()

label22a = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label22a.grid(row=15, column=1)
label22a.update()

label2a = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label2a.grid(row=16, column=1)
label2a.update()

label11a = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label11a.grid(row=17, column=1)
label11a.update()

label1a = tk.Label(fg="black",bg="white",width=25,font=12, text='')
label1a.grid(row=18, column=1)
label1a.update()

#load= Image.open("Blue-Check1.ppm")
#load=load.resize((25,25), Image.Resampling.LANCZOS) # w,h ANTIALIAS removes stucturing around image
#load=load.resize((25,25),resample=Image.BICUBIC)
renderCheck = PhotoImage(file='/home/winder/Desktop/StatorWinderV2.2/Blue-Check1.png')
    
img1a=Label(gui, borderwidth=0, image=renderCheck)
img1a.grid(row=18, column=2)
img2a=Label(gui, borderwidth=0, image=renderCheck)
img2a.grid(row=17, column=2)
img3a=Label(gui, borderwidth=0, image=renderCheck)
img3a.grid(row=16, column=2)
img4a=Label(gui, borderwidth=0, image=renderCheck)
img4a.grid(row=15, column=2)
img5a=Label(gui, borderwidth=0, image=renderCheck)
img5a.grid(row=14, column=2)
img6a=Label(gui, borderwidth=0, image=renderCheck)
img6a.grid(row=13, column=2)
img7a=Label(gui, borderwidth=0, image=renderCheck)
img7a.grid(row=12, column=2)
img8a=Label(gui, borderwidth=0, image=renderCheck)
img8a.grid(row=11, column=2)
img9a=Label(gui, borderwidth=0, image=renderCheck)
img9a.grid(row=10, column=2)
img10a=Label(gui, borderwidth=0, image=renderCheck)
img10a.grid(row=9, column=2)
img11a=Label(gui, borderwidth=0, image=renderCheck)
img11a.grid(row=8, column=2)
img12a=Label(gui, borderwidth=0, image=renderCheck)
img12a.grid(row=7, column=2)
img13a=Label(gui, borderwidth=0, image=renderCheck)
img13a.grid(row=6, column=2)
img14a=Label(gui, borderwidth=0, image=renderCheck)
img14a.grid(row=5, column=2)
img15a=Label(gui, borderwidth=0, image=renderCheck)
img15a.grid(row=4, column=2)
img16a=Label(gui, borderwidth=0, image=renderCheck)
img16a.grid(row=3, column=2)

img1b=Label(gui, borderwidth=0, image=renderCheck)
img1b.grid(row=18, column=3)
img2b=Label(gui, borderwidth=0, image=renderCheck)
img2b.grid(row=17, column=3)
img3b=Label(gui, borderwidth=0, image=renderCheck)
img3b.grid(row=16, column=3)
img4b=Label(gui, borderwidth=0, image=renderCheck)
img4b.grid(row=15, column=3)
img5b=Label(gui, borderwidth=0, image=renderCheck)
img5b.grid(row=14, column=3)
img6b=Label(gui, borderwidth=0, image=renderCheck)
img6b.grid(row=13, column=3)
img7b=Label(gui, borderwidth=0, image=renderCheck)
img7b.grid(row=12, column=3)
img8b=Label(gui, borderwidth=0, image=renderCheck)
img8b.grid(row=11, column=3)
img9b=Label(gui, borderwidth=0, image=renderCheck)
img9b.grid(row=10, column=3)
img10b=Label(gui, borderwidth=0, image=renderCheck)
img10b.grid(row=9, column=3)
img11b=Label(gui, borderwidth=0, image=renderCheck)
img11b.grid(row=8, column=3)
img12b=Label(gui, borderwidth=0, image=renderCheck)
img12b.grid(row=7, column=3)
img13b=Label(gui, borderwidth=0, image=renderCheck)
img13b.grid(row=6, column=3)
img14b=Label(gui, borderwidth=0, image=renderCheck)
img14b.grid(row=5, column=3)
img15b=Label(gui, borderwidth=0, image=renderCheck)
img15b.grid(row=4, column=3)
img16b=Label(gui, borderwidth=0, image=renderCheck)
img16b.grid(row=3, column=3)

img1c=Label(gui, borderwidth=0, image=renderCheck)
img1c.grid(row=18, column=4)
img2c=Label(gui, borderwidth=0, image=renderCheck)
img2c.grid(row=17, column=4)
img3c=Label(gui, borderwidth=0, image=renderCheck)
img3c.grid(row=16, column=4)
img4c=Label(gui, borderwidth=0, image=renderCheck)
img4c.grid(row=15, column=4)
img5c=Label(gui, borderwidth=0, image=renderCheck)
img5c.grid(row=14, column=4)
img6c=Label(gui, borderwidth=0, image=renderCheck)
img6c.grid(row=13, column=4)
img7c=Label(gui, borderwidth=0, image=renderCheck)
img7c.grid(row=12, column=4)
img8c=Label(gui, borderwidth=0, image=renderCheck)
img8c.grid(row=11, column=4)
img9c=Label(gui, borderwidth=0, image=renderCheck)
img9c.grid(row=10, column=4)
img10c=Label(gui, borderwidth=0, image=renderCheck)
img10c.grid(row=9, column=4)
img11c=Label(gui, borderwidth=0, image=renderCheck)
img11c.grid(row=8, column=4)
img12c=Label(gui, borderwidth=0, image=renderCheck)
img12c.grid(row=7, column=4)
img13c=Label(gui, borderwidth=0, image=renderCheck)
img13c.grid(row=6, column=4)
img14c=Label(gui, borderwidth=0, image=renderCheck)
img14c.grid(row=5, column=4)
img15c=Label(gui, borderwidth=0, image=renderCheck)
img15c.grid(row=4, column=4)
img16c=Label(gui, borderwidth=0, image=renderCheck)
img16c.grid(row=3, column=4)

####IMG####
render = PhotoImage(file='/home/winder/Desktop/StatorWinderV2.2/logo4.ppm')

img = Label(gui, borderwidth=0, image=render)
img.grid(row=19,columnspan=5)
img.update()

def readMessage():
    global phase,currentTurn,turn,img16a,img16b,img16c
    varText=''
    while True:
        message = arduino.readMessage()
        #try:
        if message != '':
            print(message)
            response = message.split(',')
            phase = response[0]
            #print(phase)
            currentTurn = float(response[1])
            #print(currentTurn)
            phaseA = ['a1','A1','a2','A2','A3','a3','A4','a4','a5','A5','a6','A6','A7','a7','A8','a8']
            phaseB = ['B1','b1','B2','b2','b3','B3','b4','B4','B5','b5','B6','b6','b7','B7','b8','B8']
            phaseC = ['c1','C1','c2','C2','C3','c3','C4','c4','c5','C5','c6','C6','C7','c7','C8','c8']

            if phase in phaseA:
                varText='Phase A Started, '
                text.config(fg='black', bg='yellow', text=varText+ str(turn) +' Turns Per Pole')
                labels(phaseA,phase,currentTurn) 
            elif phase in phaseB:
                varText='Phase B Started, '
                text.config(fg='black', bg='yellow', text=varText+ str(turn) +' Turns Per Pole')
                labels(phaseB,phase,currentTurn)
            elif phase in phaseC:
                varText='Phase C Started, '
                text.config(fg='black', bg='yellow', text=varText+ str(turn) +' Turns Per Pole')
                labels(phaseC,phase,currentTurn)
                
            elif phase == 'enYstate':
                if currentTurn == 1:
                    text.config(fg='white', bg='red', text='Offset Engaged')
                else:
                    if varText == '':
                        text.config(text='Please Set Turns and Then Start Phase',fg='black',bg = '#3399ff')
                    else:
                        text.config(fg='black', bg='yellow', text=varText+ str(turn) +' Turns Per Pole')
            elif phase == 'Turn':
                if currentTurn == 0:
                    text.config(fg='white', bg='red', text='Turns need to be set')
                else:
                    dropdown.config(current_value.set(int(currentTurn)))
                    turn = int(currentTurn)
            elif phase == 'ESTOP':
                if currentTurn == 1:
                    text.config(fg='white', bg='red', text='Estop Engaged')
                else:
                    if varText == '':
                        text.config(text='Please Set Turns and Then Start Phase',fg='black',bg = '#3399ff')
                    else:
                        text.config(fg='black', bg='yellow', text=varText+ str(turn) +' Turns Per Pole')
            elif phase == 'Pass':
                if currentTurn == 1:
                    print(phase)
                    label88a.config(bg='#3399ff')
                    img16a.grid(row=3, column=2)
                    img16b.grid(row=3, column=3)
                    img16c.grid(row=3, column=4)
                    text.config(text='Done! Set Turns and Then Start Phase',fg='black',bg = '#3399ff')
                    index = 0
            elif phase == 'reset':
                if currentTurn == 1:
                    resetImg()
                    resetLbls()
                    dropdown.config(current_value.set(0))
                    turn = 0
                    text.config(text='Please set turns and then start phase', bg = '#3399ff')
                else:
                    text.config(text='Please reset to start new phase', bg = 'orange')
        #except:
            #print('Exception occured')
            #print(message)

def connectUSB():
    connectArduino()
    if passFail==1:
        usbFailure()
    else:
        text.config(text='Please Set Turns and Then Start Phase', bg = '#3399ff')
        readMessage()
    return

t1=Thread(target=connectUSB)
t1.start()

gui.mainloop() # start the GUI
