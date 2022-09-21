# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:41:00  2022

@author: nsharma
"""

'''
This Script creates MS Excel files containing Production Serial Numbers of the Rotors, Stators and the Motor Assemblies produced on a day.
'''

import os
import pandas as pd
import glob
import time, msvcrt, sys
from datetime import date

'''
Prompt the user for what date to generate 'Summary of Serial Numbers produced', but timing out after 10 seconds and use Today to generate report
'''
today = date.today()

def readInput( caption, default, timeout = 8):

    start_time = time.time()
    sys.stdout.write('%s(%s):'%(caption, 'Today: ' + default))
    sys.stdout.flush()
    input = ''
    while True:
        if msvcrt.kbhit():
            byte_arr = msvcrt.getche()
            if ord(byte_arr) == 13: # enter_key
                break
            elif ord(byte_arr) >= 32: #space_char
                input += "".join(map(chr,byte_arr))
        if len(input) == 0 and (time.time() - start_time) > timeout:
            # print("timing out, will generate serial numbers list for Today.")
            break

    print('')  # needed to move to next line
    if len(input) > 0:
        return input
    else:
        return default

ProdDate = readInput('Enter the Production Date (mmddyyyy): ', today.strftime("%m%d%Y")) 


'''
Define the Directory where summary excel files will be stored
'''
OutPath = '\\\ctgtech-lldc01\\LL Production Data\\Daily Summary Reports\\' ### Define the Directory where summary excel files will be stored

'''
Section #1: Rotors
'''
dir_name_Rotor = r'\\ctgtech-lldc01\LL Production Data\Rotor Test Results/'
list_of_rfiles = filter( os.path.isfile, glob.glob(dir_name_Rotor + '*.xlsx') )
list_of_rfiles = sorted( list_of_rfiles, key = os.path.getmtime,reverse=True)
df = pd.DataFrame()
rf = pd.DataFrame()
for file_path in list_of_rfiles:
    fname = os.path.basename(file_path)
    fname = fname.rsplit('-V',1)
    fdate = time.strftime(  '%m%d%Y', time.gmtime(os.path.getmtime(file_path)))
    
    rf = pd.DataFrame(fname)
    rf = rf.drop(1)
    if fdate == ProdDate:
        fdatePrint = time.strftime(  '%b %d, %Y', time.gmtime(os.path.getmtime(file_path)))
        rf['Date'] = fdatePrint
        rf.rename({0: 'Rotor Serial Number', 'Date': 'Date'}, axis=1, inplace=True)
        df = df.append(rf)

file = 'Summary - Rotor Serial Numbers - ' + ProdDate + '.xlsx'
df = df.drop_duplicates(subset=['Rotor Serial Number'], keep='first') #Removes Duplicte Entries and keeps the entry with the last timestamp
if len(df) !=0:
    df.insert(0, '#', range(1, 1 + len(df)))                
    df.to_excel(os.path.join(OutPath, file), index=False)
  
else: 
    # sdf['0'] = 'No Stators Produced on '+ ProdDate
    df.insert(0, 'No Rotors Produced on '+ ProdDate, 'No Rotors Produced on '+ ProdDate)    
    df.to_excel(os.path.join(OutPath, file), index=False)
  

'''
Section #2: Stators
'''

dir_name_Stator = r'\\ctgtech-lldc01\LL Production Data\Stator Test Results/'
list_of_sfiles = filter( os.path.isfile, glob.glob(dir_name_Stator + '*.xlsx') )
list_of_sfiles = sorted( list_of_sfiles, key = os.path.getmtime,reverse=True)
sdf = pd.DataFrame()
sf = pd.DataFrame()
 
for sfile_path in list_of_sfiles:
    sfname = os.path.basename(sfile_path)
    sfname = sfname.rsplit('(',1)
    del sfname[-1]
    if sfname[0:4] !='Fail':
        if sfname[0:1] != '~':
            if sfname[0:6] !='Summary':
                sfdate = time.strftime(  '%m%d%Y', time.gmtime(os.path.getmtime(sfile_path)))
                sf = pd.DataFrame(sfname)
     
                if sfdate == ProdDate:
                    sfdatePrint = time.strftime(  '%b %d, %Y', time.gmtime(os.path.getmtime(sfile_path)))
                    sf['Date'] = sfdatePrint
                    sf.rename({0: 'Stator Serial Number', 'Date': 'Date'}, axis=1, inplace=True)
                    sdf = sdf.append(sf)
sdf = sdf.drop_duplicates(subset=['Stator Serial Number'], keep='first') #Removes Duplicte Entries and keeps the entry with the last timestamp
file = 'Summary - Stator Serial Numbers - ' + ProdDate + '.xlsx'
if len(sdf) !=0:
    sdf.insert(0, '#', range(1, 1 + len(sdf)))
    df.to_excel(os.path.join(OutPath, file), index=False)                

else: 

    sdf.insert(0, 'No Stators Produced on '+ ProdDate, 'No Stators Produced on '+ ProdDate)    
    df.to_excel(os.path.join(OutPath, file), index=False)


'''
Section #3: Back EMF Testing / Motor Assembly
'''

dir_name_BEMF = r'\\ctgtech-lldc01\LL Production Data\Back EMF Test Results/'
list_of_mfiles = filter( os.path.isfile, glob.glob(dir_name_BEMF + '*.xlsx') )
list_of_mfiles = sorted( list_of_mfiles, key = os.path.getmtime,reverse=True)
mdf = pd.DataFrame()
mf = pd.DataFrame()

for mfile_path in list_of_mfiles:
    mfname = os.path.basename(mfile_path)
    mfname = mfname.rsplit('(',1)
    del mfname[-1]
    if mfname[0:4] !='Fail':
        if mfname[0:1] != '~':
            if mfname[0:6] !='Summary':
                mfdate = time.strftime(  '%m%d%Y', time.gmtime(os.path.getmtime(mfile_path)))
                mf = pd.DataFrame(mfname)
                    
                if mfdate == ProdDate:
                    mfdatePrint = time.strftime(  '%b %d, %Y', time.gmtime(os.path.getmtime(mfile_path)))
                    mf['Date'] = mfdatePrint
                    mfTimePrint = time.strftime('%H:%M:%S: %Z', time.gmtime(os.path.getmtime(mfile_path)))
                    mf.rename({0: 'Motor Assembly Serial Number', 'Date': 'Date'}, axis=1, inplace=True)
                    mdf = mdf.append(mf)

mdf = mdf.drop_duplicates(subset=['Motor Assembly Serial Number'], keep='first') #Removes Duplicte Entries and keeps the entry with the last timestamp
file = 'Summary - Motor Assembly Serial Numbers - ' + ProdDate + '.xlsx'
if len(mdf) !=0:
    mdf.insert(0, '#', range(1, 1 + len(mdf)))                
    df.to_excel(os.path.join(OutPath, file), index=False)
else: 
    mdf.insert(0, 'No Motor Assemblies Produced on '+ ProdDate, 'No Motor Assemblies Produced on '+ ProdDate)    
    df.to_excel(os.path.join(OutPath, file), index=False)



