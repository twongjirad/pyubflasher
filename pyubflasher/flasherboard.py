import serial
from pyubflasher.boardconfig import BoardConfig
import os,sys

class FlasherBoard:
    def __init__( self, config_file="__default__" ):
        if config_file=="__default__":
            mypath = os.path.dirname(os.path.realpath(__file__))
            config_file = mypath+"/config/boardconfig.json"
        self.config = self.loadConfig( config_file  ) 
        self.port = self.openPort()
        print "Successfully opened port to flasher board through ",self.port
        
    def loadConfig( self, config_file ):
        self.configFile = config_file
        return BoardConfig( self.configFile )
        
    def openPort( self ):
        try:
            ser = serial.Serial( self.config.port, self.config.baud_rate, timeout=1 )
        except:
            raise RuntimeError('Could not open the serial port! Tried %s'%(self.config.port))
        return ser

    def clearReadBuffer(self):
        rbuf = 'SPAM'
        out = []
        while rbuf!='':
            rbuf = self.port.readline()
            out.append( rbuf )
        return out
        
    def printMenu( self ):
        self.clearReadBuffer()
        self.port.write( 'HE\r\n' )
        out = self.clearReadBuffer()
        for l in out:
            print l.strip()
