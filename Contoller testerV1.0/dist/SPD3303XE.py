# SPD3303X-E Power Supply Module
# Linear Labs Inc
# Doug Gammill
# 3/15/22

import pyvisa # handles usb equipment like power supplies and o-scopes
import configparser # handles config files
from time import sleep

configParser = configparser.RawConfigParser() # config
configFilePath = '//CTGTECH-LLDC01.linearlabs.local/Production/Production Data/Controller Config Files/folderConfig.txt'
configParser.read(configFilePath)
idResponse = configParser.get('folderPath', 'idResponseSPD3303X-E')
comPort = configParser.get('folderPath', 'comPortSPD3303X-E')
rm = pyvisa.ResourceManager()
my_instrument = rm.open_resource(comPort)

def connectPowerSupply():
    global rm, my_instrument
    x = my_instrument.query('*idn?')
    x=x.strip()

    if x == idResponse:
        print("SPD3303X-E Power Supply connected")
    else:
        print(x)
    
def ch1On():
    global rm, my_instrument
    my_instrument.write('OUTP CH1,ON') #### turn on CH1 returns "13"
    
def ch1Off():
    global rm, my_instrument
    my_instrument.write('OUTP CH1,OFF') #### turn off CH1 returns "14"

def ch2On():
    global rm, my_instrument
    my_instrument.write('OUTP CH2,ON') #### turn on CH2

def ch2Off():
    global rm, my_instrument
    my_instrument.write('OUTP CH2,OFF') #### turn on CH2

def indMode(): #### turn on independent Operation Mode returns "14"
    global rm, my_instrument
    my_instrument.write('OUTP:TRACK 0') 

def serMode(): #### turn on series Operation mode returns "14"
    global rm, my_instrument
    my_instrument.write('OUTP:TRACK 1')

def parMode(): #### turn on parallel Operation mode returns "14"
    global rm, my_instrument
    my_instrument.write('OUTP:TRACK 2')

def ch1CurrentSetting(): #### queries CH1 or series current max setting returns amps
    global rm, my_instrument
    my_instrument.query('CH1:CURR?')

def ch2CurrentSetting(): #### queries CH2 or series current max setting returns amps
    global rm, my_instrument
    my_instrument.query('CH2:CURR?')

def ch1MeasureCurrent(): #### measures CH1 or series current output returns amps
    global rm, my_instrument, result
    my_instrument.query('MEAS:CURR? CH1')
    result = my_instrument.query('MEAS:CURR? CH1')
    result = result.strip()
    return result

def ch2MeasureCurrent(): #### measures CH2 or series current output returns amps
    global rm, my_instrument
    my_instrument.query('MEAS:CURR? CH2')

def ch1VoltageSetting(): #### queries CH1 or series voltage max setting returns volts
    global rm, my_instrument
    my_instrument.query('CH1:VOLT?')

def ch2VoltageSetting(): #### queries CH2 or series voltage max setting returns volts
    global rm, my_instrument
    my_instrument.query('CH2:VOLT?')

def ch1MeasureVoltage(): #### measures CH1 or series voltage output returns volts
    global rm, my_instrument, result
    my_instrument.query('MEAS:VOLT? CH1')
    result = my_instrument.query('MEAS:VOLT? CH1')
    result = result.strip()
    return result

def ch2MeasureVoltage(): #### measures CH2 or series voltage output returns volts
    global rm, my_instrument
    my_instrument.query('MEAS:VOLT? CH2')

def ch1SetCurr(sourceCurrent): #### sets CH1 or series current
    global rm, my_instrument
    my_instrument.write('CH1:CURR '+sourceCurrent)

def ch2SetCurr(sourceCurrent2): #### sets CH2 or series current
    global rm, my_instrument
    my_instrument.write('CH2:CURR '+sourceCurrent2)

#def ch1SetVolt(sourceVoltage): #### sets CH1 or series voltage returns 13
    #global rm, my_instrument
    #my_instrument.write('CH1:VOLT '+sourceVoltage)

def ch2SetVolt(sourceVoltage2): #### sets CH2 or series voltage returns 13
    global rm, my_instrument
    my_instrument.write('CH2:VOLT '+sourceVoltage2)

def ch1RampVolt(sourceVoltage, sourceCurrent): #### ramps up CH1 or series voltage and shuts off if max current is reached
    global rm, my_instrument, result, current, voltageCh1, voltageCh2
    i=0.0
    my_instrument.write('CH1:VOLT 0')
    my_instrument.write('CH1:CURR '+sourceCurrent)
    sourceVoltage=float(sourceVoltage)
    sourceCurrent=float(sourceCurrent)
    my_instrument.write('OUTP CH1,ON')
    while i <= sourceVoltage:
        my_instrument.write('CH1:VOLT '+str(i))
        current=my_instrument.query('MEAS:CURR? CH1')
        current=current.strip()
        currentMeas=float(current)
        if currentMeas==sourceCurrent:
            sleep(.5)
            voltageCh1=my_instrument.query('MEAS:VOLT? CH1')
            voltageCh1=voltageCh1.strip()
            voltageCh2=my_instrument.query('MEAS:VOLT? CH2')
            voltageCh2=voltageCh2.strip()
            my_instrument.write('OUTP CH1,OFF')
            result = 'OverCurrent'
            return result, current, voltageCh1, voltageCh2
        i+=0.2
    sleep(2)
    current=my_instrument.query('MEAS:CURR? CH1')
    current=current.strip()
    voltageCh1=my_instrument.query('MEAS:VOLT? CH1')
    voltageCh1=voltageCh1.strip()
    voltageCh2=my_instrument.query('MEAS:VOLT? CH2')
    voltageCh2=voltageCh2.strip()
    result='Good'
    return result,current,voltageCh1, voltageCh2
    
