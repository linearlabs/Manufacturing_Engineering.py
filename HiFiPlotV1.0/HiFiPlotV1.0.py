import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

var = pd.read_excel("Z:\Rotor Test Results\HiFiM10-000135-002-xxxx-V1.xlsx")
#print(var)

x = list(var['index'])
y = list(var['sensor 1 value'])

def divide_chunks(l, n):
    for i in range(0, len(l), n):# looping till length l
        yield l[i:i + n]
# How many elements each
# list should have
n = 277
j = 0
magnetSamples = list(divide_chunks(y, n))
maxValue = max(magnetSamples[0])
position = magnetSamples[0].index(maxValue)
lastPos = position
for j in range(0, 52, 1):
    maxValue = max(magnetSamples[j])
    position = magnetSamples[j].index(maxValue)
    positionOff = lastPos - position
    degreesOff = positionOff / 40 # 40 steps per degree
    #print(str(j)+'. Max, '+ str(maxValue)+ ', Index, ' + str(position) + ', PosDif, ' + str(degreesOff)+ ' Degrees Off')
    print(str(j)+'. '+ str(degreesOff)+ ' Degrees Off')
    j=j+1
    lastPos = position

plt.figure(figsize=(10,10))
plt.style.use('seaborn')
plt.plot(x,y)
plt.title("M10-000135-002-xxxx")
plt.xticks(np.arange(min(x), max(x)+1, 277)) # set tick marks (1.0 or 277x52=14404)
plt.show()
