import gps
import threading

import calendar

months = {"01":"Jan","02":"Feb","03":"Mar","04":"Apr","05":"May",
          "06":"Jun","07":"Jul","08":"Aug","09":"Sep","10":"Oct",
          "11":"Nov","12":"Dec"}

weekdays = ["Mon","Tue","Wed","Thur","Fri","Sat","Sun"]


class formattedTime:
    """
    Class to store the gps time that has been formatted
    Thread safe, lock prevents time from being updated and 
    read at the same time        
    """
    

    def __init__(self):
        self._time = None
        self._lock = threading.Lock()


    def getTime(self):
        self._lock.acquire()
        time = self._time
        self._lock.release()

        return time

    def updateTime(self, unFormattedTime):

        self._lock.acquire()
        formattedTime = self.formatTime(unFormattedTime)
        self._time = formattedTime
        self._lock.release()

    def formatTime(self, gpsTime):
        # formats raw gps time

        if(gpsTime== "nogps"):
            return gpsTime

        year = gpsTime[0:4]
        month = gpsTime[5:7]
        day = gpsTime[8:10]
        hour = gpsTime[11:13]
        minute = gpsTime[14:16]
        second = gpsTime[17:19]
        mil_sec = gpsTime[20:23]
        timeZone = gpsTime[23]

        weekDay=(calendar.weekday(int(year), int(month),int(day)))

        if timeZone =='Z':
            timeZone = 'GMT'

        month = months[month]
        weekDay = weekdays[weekDay]

        gpsTimeStr = (weekDay+'_'+month+'_'+day+'_'+hour+'_'+minute+
                      '_'+second+'_'+mil_sec+'_'+timeZone+'_'+year)
        return gpsTimeStr


currentTime = formattedTime()

# condition to alert other threads when the gps
# updates.  used for synchronization
gpsTick = threading.Condition()

# event to signal to stop reading gps
endSig = threading.Event()

def gpsClock():
    """
    function to get current gps time continually
    and update current time

    signals other threads by gpsTick.notify
    
    ends when endSig is set
    """

    try:
        session = gps.gps("localhost", "2947")
        session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
    except socket.error:
        session = "nogps"

    if(session == "nogps"):
        while not endSig.isSet():
            time.sleep(60)

            gpsTick.acquire()
            gpsTick.notify()
            gpsTick.release()

    else:

        while not endSig.isSet():

            report = session.next()

            if(report['class'] == 'TPV'):
                if hasattr(report, "time"):
                    gpsTick.acquire()
                    currentTime.updateTime(report.time)
                    gpsTick.notify()
                    gpsTick.release()

    

if __name__ == "__main__":

    clk = threading.Thread(target = gpsClock)

    
    gpsTick.acquire()

    print("starting clk")
    clk.start()

    i = 0

    while i < 10:

        gpsTick.wait()
        gpsTick.wait()

        print("currentTime: {}".format(currentTime.getTime()))

        i = i+1


    print("releasing gpsTick")
    gpsTick.release()

    print("stopping")
    endSig.set()

    print("waiting for clk thread")
    clk.join()
    print("ending")
    

    
    
