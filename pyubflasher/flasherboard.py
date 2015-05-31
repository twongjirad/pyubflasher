import serial
from pyubflasher.boardconfig import BoardConfig
import os,sys



class FlasherBoard:
    def __init__( self, config_file="__default__" ):
        if config_file=="__default__":
            mypath = os.path.dirname(os.path.realpath(__file__))
            config_file = mypath+"/config/boardconfig.json"
        self.config = self.loadConfig( config_file  ) 
        self.port = None
        
    def loadConfig( self, config_file ):
        self.configFile = config_file
        return BoardConfig( self.configFile )
        
    def openPort( self ):
        if self.port is None:
            try:
                self.port = serial.Serial( self.config.port, self.config.baud_rate, timeout=1 )
            except:
                raise RuntimeError('Could not open the serial port! Tried %s'%(self.config.port))
            print "Successfully opened port to flasher board through ",self.port
        else:
            return self.port
        # clear out junk
        self.port.write('\r')
        out = self.clearReadBuffer()
        return self.port

    def clearReadBuffer(self):
        self.openPort()
        rbuf = 'SPAM'
        out = []
        while rbuf!='':
            rbuf = self.port.readline()
            out.append( rbuf )
        return out
        
    def printMenu( self ):
        self.openPort()
        self.clearReadBuffer()
        self.port.write( 'HE\r\n' )
        out = self.clearReadBuffer()
        for l in out[2:]:
            print l.strip()

    def queryAllRegisters(self):
        self.openPort()
        print "PRINTING ALL PROGRAMED VOLTAGE VALUES"
        self.port.write( 'RD %d\r'%(10))
        #str_adc = self.port.readline()
        #print str_adc
        out = self.clearReadBuffer()
        print out
        pass
