import threading
import getpass
import Queue
import numpy as np

writerQueue = Queue.Queue()

class specData:
    """
    Class to be sent to the queue containing the needed 
    info to write out
    """

    def __init__(self, scan, metadata, path):
        # spectral scan, metadata object, dir path 
        self.scan = scan
        self.metadata = metadata
        self.path = path


def specWriter(writerWavelengths, writerDarkCount, darkCountTime):

    while True:

        spectrum = writerQueue.get()

        if spectrum is None:
            writerQueue.task_done()
            break;

        md = spectrum.metadata

        if writerWavelengths is None:
            writerWavelengths = np.zeros(spectrum.scan.size)

        if writerDarkCount.size == 1:
            writerDarkCount = np.zeros(spectrum.scan.size)

        #TODO add conversion to radiance
        cols="wavlength DC\tdark({}s)\tscanMinDark(radiance)\n"\
            .format(darkCountTime)
        data = np.transpose(np.vstack((writerWavelengths,
                                      spectrum.scan,
                                       writerDarkCount,
                                       spectrum.scan-writerDarkCount)))
        format = "%7.3f %.2f %.3f, %.2f"

        f = open(spectrum.path+"/spectrum_"+md.time+
                 ".txt","w")
        f.write(str(md))
        f.write("User: {}\n".format(getpass.getuser()))
        f.write(">>>>>Begin Spectral Data<<<<<\n")
        f.write(cols)
        np.savetxt(f, data, fmt=format)
        f.close()

        print("wroteFile")
        writerQueue.task_done()
        
