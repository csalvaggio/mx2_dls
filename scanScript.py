import threading
from copy import copy
import os
import numpy as np
import sys

import getArgParser
import downwellingGPS as dGPS
import downwellingFlame as scan
import downwellingWriter as wrt

from gpiozero import LED

parser = getArgParser.getArgParser()

args = parser.parse_args()

integrationTime = args.intTime
numberOfScans = args.numberOfScans
correct_dark_counts = args.correct_dark_counts
correct_nonlinearity = args.correct_nonlinearity
save = args.saveScan  
scansToAverage = args.scansToAverage
prefix = args.prefix

interface = scan.OceanOpticsScannerInterface.getInterfaceFirstSpec()


wavelengths = interface.spec.wavelengths()

if(args.dark):
    # calculate dark current 5 scans 5 secs each
    darkCurTime = 5000000
    darkScans = 5

    darkCurrent = interface.darkCurrentScan(darkScans, darkCurTime)
    

    writer = threading.Thread(target = wrt.specWriter,
                              args=(wavelengths, darkCurrent,
                                    darkCurTime/1000000))

else:
    writer = threading.Thread(target = wrt.specWriter,
                              args=(wavelengths,
                                    np.ones(wavelengths.size())
                                    -1))


dGPS.gpsTick.acquire()
clk = threading.Thread(target = dGPS.gpsClock)

print("starting gps read")
clk.start()
print("starting writer thread")
writer.start()

print("acquiring gps")
dGPS.gpsTick.wait()
print(dGPS.currentTime.getTime())

dirPath = "/home/pi/Desktop/downwelling/"+prefix+"_"+\
    dGPS.currentTime.getTime()+"/"

print("making dir")
os.mkdir(dirPath)
os.mkdir(dirPath+"/Dark/")

print("sending dark to queue")
wrt.writerQueue.put(wrt.specData(darkCurrent, copy(interface.metadata),
                                 dirPath+"/Dark/"))


# LED(4).on() # pin 7


# run synced for numberOfScans with autoexposure
if(integrationTime < 0):
    for i in range(numberOfScans):

        dGPS.gpsTick.wait()
        print("calculating auto exposure")

        interface.calcAutoExp()

        dGPS.gpsTick.wait()
        print("scanning")

        scan = interface.scan()

        wrt.writerQueue.put(wrt.specData(scan, copy(interface.metadata),
                                     dirPath))

# run with specified exposure for numberOfScans
else:
    print("set integration time")
    interface.setIntTime(args.intTime)
    for i in range(numberOfScans):
        dGPS.gpsTick.wait()
        print("scanning")
        scan = interface.scan()
        wrt.writerQueue.put(wrt.specData(scan, copy(interface.metadata),
                                         dirPath))


#LED(4).off() # pin 7

# stopping all threads
wrt.writerQueue.put(None)
    
dGPS.gpsTick.release()

print("stopping")
dGPS.endSig.set()

wrt.writerQueue.join()
writer.join()

print("waiting for clk")
clk.join()
