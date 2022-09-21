# SDS1104XE 
# Linear Labs Inc
# Doug Gammill
# 3/28/22

import pyvisa # handles usb equipment like power supplies and o-scopes
import configparser # handles config files
from time import sleep # handles delay

configParser = configparser.RawConfigParser() # config
configFilePath = '//CTGTECH-LLDC01.linearlabs.local/Production/Production Data/Back EMF Config Files/folderConfig.txt'
configParser.read(configFilePath)
folder = configParser.get('folderPath', 'savePath')
configFolder = configParser.get('folderPath', 'configFolder')
idResponse1 = configParser.get('folderPath', 'idResponse1')
idResponse2 = configParser.get('folderPath', 'idResponse2')
comPortScope1 = configParser.get('folderPath', 'comPortScope1')
comPortScope2 = configParser.get('folderPath', 'comPortScope2')
rm = pyvisa.ResourceManager()
my_instrument1 = rm.open_resource(comPortScope1)
my_instrument2 = rm.open_resource(comPortScope2)

def connectOScope():
    global rm, my_instrument1, my_instrument2
    x = my_instrument1.query('*idn?')
    x = x.strip()
    y = my_instrument2.query('*idn?')
    y = y.strip()

    if x == idResponse1:
        print("Scope #1 Connected")
    else:
        print("Scope #1 Failed")
        print(x)
    if y == idResponse2:
        print("Scope #2 Connected")
    else:
        print("Scope #2 Failed")
        print(y)
    


def getWFfromScope(Scope,Ch):
    # This fuction will request the scope to output waveform of the requested channels 
    # Function takes a VISA object and a string for the channel.
    # channel should be of the format 'C1'. This must be a string. 
    # Function outputa a list with two cols. Time [sec] and Volts [V]. The first entry
    # on the list is col headers 'Time' and 'Volts'
    # See SDS 1104X-E manual.
    
    Scope.write("chdr off")
    vdiv = Scope.query(Ch+":vdiv?")
    ofst = Scope.query(Ch+":ofst?")
    tdiv = Scope.query("tdiv?")
    sara = Scope.query("sara?")
    sara = float(sara)
    Scope.timeout = 2000 #default value is 2000(2s)
    Scope.write(Ch+":wf? dat2")
    recv = list(Scope.read_raw())[15:]
    recv.pop()
    #recv.pop()
    volt_value = []
    for data in recv:
        if data > 127:
            data = data - 255
        else:
            pass
        volt_value.append(data)
    time_value = []

    for idx in range(0,len(volt_value)):
        volt_value[idx] = volt_value[idx]/25*float(vdiv)-float(ofst)
        time_data = -(float(tdiv)*14/2)+idx*(1/sara)
        time_value.append(time_data)
    #print('getWFfromScope done')
    sleep(.2)
    return (time_value,volt_value)

def measurePhase(Scope,ch1,ch2):
    # This fuction will request the scope to output Phase between the 
    # requested channels. Function takes a VISA object and two strings represting
    # the channels. eg. for channel 1 and 2 pass 'c1' & c2. It must be of string type
    # This fuction returns float of phase angle in degs as a 
    # See SDS 1104X-E manual. 
    
    Scope.write("chdr off")
    res = Scope.query(ch1+"-"+ch2+":MEAD? PHA")
    res = float(res[4:-1])
    sleep(.2)
    #print('measurePhase done')
    return res

def measurePkPkandRMS(Scope,ch):
    # This fuction will request the scope to output Pk-Pk and RMS of the 
    # requested channel. Function takes a VISA object and a string represting
    # the channel. eg. for channel 1 pass 'c1'. It must be of string type
    # This function returns a list of the from [RMS, pk-pk] of type float with units in Volts
    # See SDS 1104X-E manual. 
    Scope.write("chdr off")
    
    rms = Scope.query(ch+":PAVA? RMS")
    if rms!= 'RMS,****\n':
        rms = float(rms[4:-1])
    else:
        rms=0.0
    
    pkpk = Scope.query(ch+":PAVA? PKPK")
    if pkpk!= 'PKPK,****\n':
        pkpk = float(pkpk[5:-1])
    else:
        pkpk=0.0
    sleep(.2)
    #print('measurePkPkandRMS Done')
    return [rms, pkpk]

def measureFreq(Scope,ch):
    # This fuction will request the scope to output the frequency of the 
    # requested channel. Function takes a VISA object and a string represting
    # the channel. eg. for channel 1 pass 'c1'. It must be of string type
    # This function returns a list of the from [RMS, pk-pk] of type float with units in Volts
    # See SDS 1104X-E manual. 
    Scope.write("chdr off")
    freq = Scope.query(ch+":PAVA? FREQ")
    if freq != 'FREQ,****\n':
        freq = float(freq[5:-1])
    else:
        freq=0.0
    sleep(.2)
    return freq

def measureDutycycle(Scope,ch):
    # This fuction will request the scope to output duty cycle of the 
    # requested channel. Function takes a VISA object and a string represting
    # the channel. eg. for channel 1 pass 'c1'. It must be of string type
    # This function returns a list of the from [RMS, pk-pk] of type float with units in Volts
    # See SDS 1104X-E manual. 
    Scope.write("chdr off")
    duty = Scope.query(ch+":PAVA? DUTY")
    if duty!= 'DUTY,****\n':
        duty = float(duty[5:-1])
    else:
        duty=0.0
    
    #print('measureDutycycle Done')
    sleep(.5)
    return duty


    
