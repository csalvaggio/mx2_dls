import seabreeze.spectrometers as sb
from datetime import datetime
import getpass
import numpy as np
import time
import sys

import oceanOpticsMetadata as md

from downwellingGPS import currentTime

class OceanOpticsScannerInterface(object):
    '''

    title::
      OceanOpticsScannerInterface

    description::
      Wrapper class for seabreeze spectrometer object implementing 
      useful methods for writing out scan data. 

    '''

    def __init__(self):
        self._spec = "unknown"
        self._currentScan = "unknown"
        self._metadata = "unknown"

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self,spectrometer):
        self._spec = spectrometer

    @property
    def currentValues(self):
        return self._currentScan

    @currentValues.setter
    def currentValues(self, vals):
        self._currentScan = vals

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        self._metadata = metadata


    @classmethod
    def getInterfaceFirstSpec(cls):
        """
        create an interface object for the first listed spectrometer
        """
        newInter = cls()

        newInter.spec = sb.Spectrometer.from_serial_number()

        newInter.currentValues = newInter.spec.intensities(False, False)

        newInter.metadata = md.OceanOpticsMetadata.initializeWithSpec(newInter.spec)

        return newInter

    @classmethod
    def getInterface(cls, spectrometer):
        """
        create an interface object for a given spectrometer
        """
        newInter = cls()

        newInter.spec = spectrometer

        newInter.currentValues = newInter.spec.intensities(False, False)

        newInter.metadata = md.OceanOpticsMetadata.initializeWithSpec(newInter.spec)

        return newInter

    
    def setIntTime(self, integrationTime):
        """
        Set the integration time for the spectrometer
        """
        self._spec.integration_time_micros(integrationTime)

        self._metadata.intTime = integrationTime
        

    def updateValues(self):
        """
        get current spectrometer reading
        """

        self._currentValues = self._spec.intensities(
            self._metadata.darkCorrection,
            self._metadata.nonlinearityCorrection)
       
       
    def scan(self, darkCorrection = False, nonlinearityCorrection = False):
        self._metadata.scansToAverage = 1
        self._metadata.time = currentTime.getTime()

        self._metadata.darkCorrection = darkCorrection
        self._metadata.nonlinearityCorrection = nonlinearityCorrection

        self._currentScan = self._spec.intensities(darkCorrection,
                                                nonlinearityCorrection)
        
        return self._currentScan

    
    def darkCurrentScan(self, numOfScans, intTime):

        self._metadata.scansToAverage = numOfScans
        
        self.setIntTime(intTime)

        dark = np.zeros(self._spec.wavelengths().size)

        for i in range(numOfScans):
            dark += self._spec.intensities(False, False)

        dark = dark/numOfScans

        return dark


                

    def plotSpectrum(self):

        import matplotlib.pyplot as plt

        plt.figure(spectrum)

        plt.xlabel('Wavelength  (nm)')
        plt.ylabel('Intensity')

        plt.plot(self._spec.wavelengths, self._currentValues)

        plt.show()


    def calcAutoExp(self):
        """
        Finds and sets an integration time where the max pixel value
        is between 60% and 95% percent of the maximum value a pixel 
        can have.  Modifies  in a range of 1 ms to .75 s.  
        """

        maxExp = 750000
        minExp = 1000

        curTime = 2*minExp
        
        self.setIntTime(curTime)
        timeElapsed = curTime
        self.updateValues()
        
        while(np.max(self._currentValues[16:]) >= (2**16)*.95 or
              np.max(self._currentValues[16:]) <= (2**16)*.6 or
              timeElapsed >= maxExp*.75):           

            
            if(np.max(self._currentValues[16:]) >= (2**16)*.95):
               curTime = curTime*.9
               curTime = curTime-(curTime%1000)
                
                
            elif(np.max(self._currentValues[16:]) <= (2**16)*.6):
               curTime = curTime*2
               curTime = curTime-(curTime%1000)
                
            if(curTime < minExp):
                self.setIntTime(int(minExp))
                break
               

            if(curTime > maxExp*.6):
                self.setIntTime(int(maxExp))
                break

            self.setIntTime(int(curTime))
            self.updateValues()
            timeElapsed += curTime

        return self._metadata.intTime
        
