import seabreeze.spectrometers as sb
from datetime import datetime


class OceanOpticsMetadata():
    '''

    title::
      OceanOpticsMetadata

    description::
      Class to handle metadata for ocean optics scanner

    '''

    def __init__(self):
        self._spec = "unknown"
        self._serialNumber = "unknown"
        self._time = "unknown"
        self._intTime = "unknown"
        self._numBands = "unknown"
        self._minWavelength = "unknown"
        self._maxWavelength = "unknown"
        self._darkCorrection = False
        self._nonlinearityCorrection = False
        self._scansToAverage = 1

    @classmethod
    def initializeWithSpec(cls, spectrometer):
        """
        create a metadata object for a given spectrometer
        """
        newObj = cls()

        newObj._spec = spectrometer
        newObj.serialNumber = spectrometer.serial_number
        wavelengths = spectrometer.wavelengths()

        newObj.numBands = len(wavelengths)
        newObj.minWavelength = wavelengths[0]
        newObj.maxWavelength = wavelengths[-1]

        newObj.scansToAverage = 1
        
        return newObj

    @property
    def serialNumber(self):
        return self._serialNumber

    @serialNumber.setter
    def serialNumber(self, sNumber):
        self._serialNumber = sNumber

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, newTime):
        self._time = newTime


    @property
    def intTime(self):
        return self._intTime

    @intTime.setter
    def intTime(self, ms):
        self._intTime = ms

    @property
    def numBands(self):
        return self._numBands

    @numBands.setter
    def numBands(self, bands):
        self._numBands = bands

    @property
    def minWavelength(self):
        return self._minWavelength

    @minWavelength.setter
    def minWavelength(self, wavelength):
        self._minWavelength = wavelength

    @property
    def maxWavelength(self):
        return self._maxWavelength

    @maxWavelength.setter
    def maxWavelength(self, wavelength):
        self._maxWavelength = wavelength

    @property
    def darkCorrection(self):
        return self._darkCorrection

    @darkCorrection.setter
    def darkCorrection(self, darkBool):
        self._darkCorrection = darkBool

    @property
    def nonlinearityCorrection(self):
        return self._nonlinearityCorrection

    @nonlinearityCorrection.setter
    def nonlinearityCorrection(self, linearBool):
        self._nonlinearityCorrection = linearBool

    @property
    def scansToAverage(self):
        return self._scansToAverage

    @scansToAverage.setter
    def scansToAverage(self, numScans):
        self._scansToAverage = numScans


    def __repr__(self):
        msg = ""
        msg += "Spectrometer: {}\n".format(self._spec)
        msg += "Time: {}\n".format(self.time)
        msg += "Integration Time: {0:11.6e} us\n".format(self.intTime)
        msg += "Electric Dark Correction Enabled: {}\n".format(self.darkCorrection)
        msg += "Nonlinearity Correction Enabled: {}\n".format(self.nonlinearityCorrection)

        return msg
