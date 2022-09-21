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

def connectOScope():
    global rm, passFail1,passFail2,my_instrument1,my_instrument2

    try:
        my_instrument1 = rm.open_resource(comPortScope1)
        x = my_instrument1.query('*idn?')
        x = x.strip()
        if x == idResponse1:
            print("Scope #1 Connected")
            passFail1=0
        else:
            print("Scope #1 Failed")
            print(x)
            passFail1=1
    except:
        print("Scope #1 Failed")
        passFail1=1

    try:
        my_instrument2 = rm.open_resource(comPortScope2)
        y = my_instrument2.query('*idn?')
        y = y.strip()
        if y == idResponse2:
            print("Scope #2 Connected")
            passFail2=0
        else:
            print("Scope #2 Failed")
            print(y)
            passFail2=1
    except:
        print("Scope #2 Failed")
        passFail2=1

def autoSetup(Scope):
    Scope.write("ASET")

def setupScope1(Scope,triggerLevel1,triggerCoupling1,triggerMode,triggerSelect1,channelOffset1,voltageDivision1,channelUnits1,timeDivision1,memDepth,x10Probe):
    #### Memorory Depth
    Scope.write("MSIZ " + memDepth) # memory depth, if set too high samplling could take a long time
    #### Time Division
    Scope.write("TDIV " + timeDivision1) # Time Division
    #### Trigger Mode
    Scope.write("TRMD " + triggerMode) # trigger mode
    #### Trigger Params
    Scope.write(triggerSelect1) # trigger Select
    Scope.write(triggerLevel1) # trigger level
    Scope.write(triggerCoupling1) # trigger Coupling
    
    ####CH2
    Scope.write("C2:TRA ON") # Channel Trace
    Scope.write("C2:OFST +" + channelOffset1) # Channel Offset
    Scope.write("C2:VDIV " + voltageDivision1) # Voltage Division mV,V
    Scope.write("C2:UNIT " + channelUnits1) # Channel Units V,A
    Scope.write("C2:ATTN " + x10Probe) # Channel Attenuation x1 or x10
    Scope.write("C2:CPL D1M ")  # Channel Coupling DC 1MOhm
    
    ####CH3
    Scope.write("C3:TRA ON") # Channel Trace
    Scope.write("C3:OFST 0V") # Channel Offset
    Scope.write("C3:VDIV " + voltageDivision1) # Voltage Division mV,V
    Scope.write("C3:UNIT " + channelUnits1) # Channel Units V,A
    Scope.write("C3:ATTN " + x10Probe) # Channel Attenuation x1 or x10
    Scope.write("C3:CPL D1M ")  # Channel Coupling DC 1MOhm

    ####Ch4
    Scope.write("C4:TRA ON") # Channel Trace
    Scope.write("C4:OFST -" + channelOffset1) # Channel Offset
    Scope.write("C4:VDIV " + voltageDivision1) # Voltage Division mV,V
    Scope.write("C4:UNIT " + channelUnits1) # Channel Units V,A
    Scope.write("C4:ATTN " + x10Probe) # Channel Attenuation x1 of x10
    Scope.write("C4:CPL D1M ")  # Channel Coupling DC 1MOhm

def setupScope1Channel1(Scope,voltageDivision2,channelUnits2,x10Probe):
    #### CH1 Scope1 (HALL TO PHASE ALIGNMENT)
    Scope.write("C1:TRA ON") # Channel Trace
    Scope.write("C1:OFST 0V") # Channel Offset
    Scope.write("C1:VDIV " + voltageDivision2) # Voltage Division
    Scope.write("C1:UNIT " + channelUnits2) # Channel Units V,A
    Scope.write("C1:ATTN " + x10Probe) # Channel Attenuation x1 of x10
    Scope.write("C1:CPL D1M ")  # Channel Coupling DC 1MOhm
    
def turnOffScope1Channel1(Scope):
    Scope.write("C1:TRA OFF") # Channel Trace

def setupScope2(Scope,triggerLevel2,triggerCoupling2,triggerMode,triggerSelect2,channelOffset2,voltageDivision2,channelUnits2,timeDivision2,memDepth,x10Probe):
    #### Memorory Depth
    Scope.write("MSIV " + memDepth) # memory depth, if set too high samplling could take a long time
    #### Time Division
    Scope.write("TDIV " + timeDivision2) # Time Division
    #### Trigger Mode
    Scope.write("TRMD " + triggerMode) # trigger mode
    #### Trigger Params
    Scope.write(triggerSelect2) # trigger Select
    Scope.write(triggerLevel2) # trigger level
    Scope.write(triggerCoupling2) # trigger Coupling
    
    ####CH1
    Scope.write("C1:TRA ON") # Channel Trace
    Scope.write("C1:OFST +" + channelOffset2) # Channel Offset
    Scope.write("C1:VDIV " + voltageDivision2) # Voltage Division
    Scope.write("C1:UNIT " + channelUnits2) # Channel Units V,A
    Scope.write("C1:ATTN " + x10Probe) # Channel Attenuation x1 of x10
    Scope.write("C1:CPL D1M ")  # Channel Coupling DC 1MOhm
    ####CH2
    Scope.write("C2:TRA ON") # Channel Trace
    Scope.write("C2:OFST 0V") # Channel Offset
    Scope.write("C2:VDIV " + voltageDivision2) # Voltage Division
    Scope.write("C2:UNIT " + channelUnits2) # Channel Units V,A
    Scope.write("C2:ATTN " + x10Probe) # Channel Attenuation x1 of x10
    Scope.write("C2:CPL D1M ") # Channel Coupling DC 1MOhm
    ####CH3
    Scope.write("C3:TRA ON") # Channel Trace
    Scope.write("C3:OFST -" + channelOffset2) # Channel Offset
    Scope.write("C3:VDIV " + voltageDivision2) # Voltage Division
    Scope.write("C3:UNIT " + channelUnits2) # Channel Units V,A
    Scope.write("C3:ATTN " + x10Probe) # Channel Attenuation x1 of x10
    Scope.write("C3:CPL D1M ") # Channel Coupling DC 1MOhm
    ####CH4
    Scope.write("C4:TRA OFF") # Channel Trace
    

def OPC(Scope):
    Scope.write("*OPC")

def saveScreen(Scope,fullPath2):
    Scope.chunk_size = 20*1024*1024 #default value is 20*1024(20k bytes)
    Scope.timeout = 30000 #default value is 2000(2s)
    Scope.write("SCDP")
    result_str = Scope.read_raw()
    f = open(fullPath2,'wb')
    f.write(result_str)
    f.flush()
    f.close()
    
    
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
    if res!= 'PHA,****\n':
        res = float(res[4:-1])
    else:
        res=0.0
    sleep(.2)
    return res

def measureVoltage(Scope,ch):
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
        
    ampl = Scope.query(ch+":PAVA? AMPL")
    if ampl!= 'AMPL,****\n':
        ampl = float(ampl[5:-1])
    else:
        ampl=0.0
        
    sleep(.2)
    return [rms, ampl]

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
