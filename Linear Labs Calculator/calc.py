# Python program to create a simple GUI
# calculator using Tkinter
 
# import everything from tkinter module
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk #handles Image
 
# globally declare the expression variable
expression = ""
 
 
# Function to update expression
# in the text entry box
def press(num):
    # point out the global expression variable
    global expression

    # concatenation of string

    num=str(num)
    
    expression = expression + num
    equation.set(expression)

def numFormat():
        global total
        
        total = float(total)
        numberFormat = '{:.8f}'
        total = numberFormat.format(total)
        total = str(total)
        total = total.rstrip('.0')

     


def ifPi():
    global expression
    tags = ['1π', '2π', '3π', '4π', '5π', '6π', '7π', '8π', '9π', '0π']
    labels = ['π1', 'π2', 'π3', 'π4', 'π5', 'π6', 'π7', 'π8', 'π9', 'π0']
    failures = ['1π1', '2π2', '3π3', '4π4', '5π5', '6π6', '7π7', '8π8', '9π9', '0π0']

    for failure in failures :
       if failure in expression:
           return False

Type "h
    for label in labels:
       if label in expression:            
            return False
            
    for tag in tags:
       if tag in expression:
           return False
        
    if 'π' in expression:
        print(expression)
        expression = expression.replace('π', '3.141592653589793')


            


 
# Function to evaluate the final expression
def equalpress():
    # Try and except statement is used
    # for handling the errors like zero
    # division error etc.
 
    # Put that code inside the try block
    # which may generate the error
    try:
 
        global expression, total
 
        # eval function evaluate the expression
        # and str function convert the result
        # into string

        ifPi()
        total = str(eval(expression))
        numFormat()
        equation.set(total)
        expression = ""
 
    # if error is generate then handle
    # by the except block
    except:
 
        equation.set("error")
        expression = ""

 
def FCconversion():
    try:
        global expression, total
        ifPi()        
        total = str(eval(expression)-32)
        total = str(eval(total)*5)
        total = str(eval(total)/9)
        numFormat()
        equation.set(total+"°C")
        expression = ""
    except:
        equation.set("error")
        expression = ""

def CFconversion():
    try:
        global expression, total
        ifPi()
        total = str(eval(expression)*9)
        total = str(eval(total)/5)
        total = str(eval(total)+32)
        numFormat()
        equation.set(total+"°F")
        expression = ""
    except:
        equation.set("error")
        expression = ""

def mminConversion():
    try:
        global expression, total
        ifPi()
        total = str(eval(expression)/25.4)
        numFormat()
        equation.set(total+"in")
        expression = ""
    except:
        equation.set("error")
        expression = ""

def inmmConversion():
    try:
        global expression, total
        ifPi()
        total = str(eval(expression)*25.4)
        numFormat()
        equation.set(total+"mm")
        expression = ""
    except:
        equation.set("error")
        expression = ""


def mikmConversion():
    try:
        global expression, total
        ifPi()
        total = str(eval(expression)*1.609344)
        numFormat()
        equation.set(total+"km")
        expression = ""
    except:
        equation.set("error")
        expression = ""

def kmmiConversion():
    try:
        global expression, total
        ifPi()
        total = str(eval(expression)*0.621371)
        numFormat()
        equation.set(total+"mi")
        expression = ""
    except:
        equation.set("error")
        expression = ""

# Function to clear the contents
# of text entry box
def clear():
    global expression
    expression = ""
    equation.set("")
 
 
# Driver code
if __name__ == "__main__":
    # create a GUI window
    gui = Tk()

    for i in range(6):  ###rows = 6
        gui.columnconfigure(i, weight=1, minsize=75)
        gui.rowconfigure(i, weight=1, minsize=50)

        for j in range(0, 4): ###column=5
            frame = tk.Frame(
                master=gui,
                relief=tk.RAISED,
                borderwidth=1
                
            )
            #frame.grid(row=i, column=j, padx=5, pady=5)

            #label = tk.Label(master=frame, text=f"Row {i}\nColumn {j}")
            #label.pack(padx=5, pady=5)
 
    # set the background colour of GUI window
    gui.configure(background="#292929")
 
    # set the title of GUI window
    gui.title("Linear Labs Calculator")

    gui.wm_iconbitmap('icon.ico')
 
    # set the configuration of GUI window
    gui.geometry("300x500")
    gui.resizable(width=False, height=False)
 
    # StringVar() is the variable class
    # we create an instance of this class
    equation = StringVar()
 
    # create the text entry box for
    # showing the expression .
    expression_field = tk.Entry(gui, font=("Adobe",22), textvariable=equation)
 
    # grid method is used for placing
    # the widgets at respective positions
    # in table like structure .
    expression_field.grid(row=0, columnspan=4)#, ipadx=70)
 
    # create a Buttons and place at a particular
    # location inside the root window .
    # when user press the button, the command or
    # function affiliated to that button is executed .
    button1 = Button(gui, text=' 1 ', font='16', fg='black', bg='#3399ff',
                    command=lambda: press(1), height=3, width=8)
    button1.grid(row=1, column=0)
 
    button2 = Button(gui, text=' 2 ', font='16', fg='black', bg='#3399ff',
                    command=lambda: press(2), height=3, width=8)
    button2.grid(row=1, column=1)
 
    button3 = Button(gui, text=' 3 ', font='16', fg='black', bg='#3399ff',
                    command=lambda: press(3), height=3, width=8)
    button3.grid(row=1, column=2)
 
    button4 = Button(gui, text=' 4 ', font='16', fg='black', bg='#3399ff',
                    command=lambda: press(4), height=3, width=8)
    button4.grid(row=2, column=0)
 
    button5 = Button(gui, text=' 5 ', font='16', fg='black', bg='#3399ff',
                    command=lambda: press(5), height=3, width=8)
    button5.grid(row=2, column=1)
 
    button6 = Button(gui, text=' 6 ', font='16', fg='black', bg='#3399ff',
                    command=lambda: press(6), height=3, width=8)
    button6.grid(row=2, column=2)
 
    button7 = Button(gui, text=' 7 ', font='16', fg='black', bg='#3399ff',
                    command=lambda: press(7), height=3, width=8)
    button7.grid(row=3, column=0)
 
    button8 = Button(gui, text=' 8 ', font='16', fg='black', bg='#3399ff',
                    command=lambda: press(8), height=3, width=8)
    button8.grid(row=3, column=1)
 
    button9 = Button(gui, text=' 9 ', font='16', fg='black', bg='#3399ff',
                    command=lambda: press(9), height=3, width=8)
    button9.grid(row=3, column=2)
 
    button0 = Button(gui, text=' 0 ', font='16', fg='black', bg='#3399ff',
                    command=lambda: press(0), height=3, width=8)
    button0.grid(row=4, column=0)
 
    plus = Button(gui, text=' + ', font='16', fg='black', bg='#3399ff',
                command=lambda: press("+"), height=3, width=8)
    plus.grid(row=1, column=3)
 
    minus = Button(gui, text=' - ', font='16', fg='black', bg='#3399ff',
                command=lambda: press("-"), height=3, width=8)
    minus.grid(row=2, column=3)
 
    multiply = Button(gui, text=' * ', font='16', fg='black', bg='#3399ff',
                    command=lambda: press("*"), height=3, width=8)
    multiply.grid(row=3, column=3)
 
    divide = Button(gui, text=' / ', font='16', fg='black', bg='#3399ff',
                    command=lambda: press("/"), height=3, width=8)
    divide.grid(row=4, column=3)
 
    equal = Button(gui, text=' = ', font='16', fg='black', bg='#3399ff',
                command=equalpress, height=3, width=8)
    equal.grid(row=4, column=2)
 
    clear = Button(gui, text='Clear', font='16', fg='black', bg='#3399ff',
                command=clear, height=3, width=8)
    clear.grid(row=4, column='1')
 
    Decimal= Button(gui, text='.', font='16', fg='black', bg='#3399ff',
                    command=lambda: press('.'), height=3, width=8)
    Decimal.grid(row=5, column=0)

    FCconv= Button(gui, text='°F to °C ', font='16', fg='black', bg='#3399ff',
                    command=FCconversion, height=3, width=8)
    FCconv.grid(row=5, column=2)

    FCconv= Button(gui, text='°C to °F ', font='16', fg='black', bg='#3399ff',
                    command=CFconversion, height=3, width=8)
    FCconv.grid(row=5, column=3)

    Pi= Button(gui, text='π', font='16', fg='black', bg='#3399ff',
                    command=lambda: press('π'), height=3, width=8)
    Pi.grid(row=5, column=1)

    inTOmm= Button(gui, text='in to mm', font='16', fg='black', bg='#3399ff',
                    command=inmmConversion, height=3, width=8)
    inTOmm.grid(row=6, column=0)

    mmTOin= Button(gui, text='mm to in', font='16', fg='black', bg='#3399ff',
                    command=mminConversion, height=3, width=8)
    mmTOin.grid(row=6, column=1)

    miTOkm= Button(gui, text='mi to km', font='16', fg='black', bg='#3399ff',
                    command=mikmConversion, height=3, width=8)
    miTOkm.grid(row=6, column=2)

    kmTOmi= Button(gui, text='km to mi', font='16', fg='black', bg='#3399ff',
                    command=kmmiConversion, height=3, width=8)
    kmTOmi.grid(row=6, column=3)
    
    ####IMG####
    load= Image.open("logo4.ppm")
    render = ImageTk.PhotoImage(load)
    img = Label(gui, image=render)
    img.grid(row=7, columnspan=4)
    
    # start the GUI#
    gui.mainloop()
