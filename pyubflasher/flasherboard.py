import serial
from pyubflasher.boardconfig import BoardConfig
import os,sys

channel_register_map = {
    0:"10",
    1:"11",
    2:"12",
    3:"13",
    4:"14",
    5:"15",
    6:"16",
    7:"17",
    8:"18",
    9:"19",
    10:"1A",
    11:"1B",
    12:"1C",
    13:"1D",
    14:"1E",
    15:"1F",
    16:"20",
    17:"21",
    18:"22",
    19:"23",
    20:"24",
    21:"25",
    22:"26",
    23:"27",
    24:"28",
    25:"29",
    26:"2A",
    27:"2B",
    28:"2C",
    29:"2D",
    30:"2E",
    31:"2F",
    32:"30",
    33:"31",
    34:"32",
    35:"33",
}    

class FlasherBoard:
    def __init__( self, config_file="__current__" ):
        if config_file=="__current__":
            mypath = os.path.dirname(os.path.realpath(__file__))
            config_file = mypath+"/config/currentconfig.json"
            if not os.path.exists(config_file):
                os.system("cp %s/config/boardconfig.json %s"%(mypath,config_file))
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
            #print "Successfully opened port to flasher board through ",self.port
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

    def queryRegister(self,chid):
        if type(chid) is not int:
            raise TypeError("Channel ID must be (decimal) integer in [0,36)")
        self.openPort()
        self.port.write( 'RD %s\r'%(channel_register_map[chid]))
        out = self.clearReadBuffer()
        strhex = out[1].strip()
        val = int( strhex, 16 )
        print "[CH %d, %s ] %d (0x%s)" % ( chid, channel_register_map[chid], val, strhex )

    def queryAllRegisters(self):
        self.openPort()
        #print "-----------------------------------------"
        #print "PRINTING ALL PROGRAMMED VOLTAGE VALUES"
        self.port.write( 'RDI 10 36\r')

        adcs = {}
        out = self.clearReadBuffer()
        # return: [command echo, ... string with values ...]
        keys = channel_register_map.keys()
        keys.sort()
        ich = 0
        for buf in out[1:]:
            data = buf.strip().split()
            for strval in data:
                adcs[ich] = {"adc":0,"hex":"" }
                adcs[ich]["adc"] = int(strval,16) # isn't python nice?
                adcs[ich]["hex"] = strval
                ich+=1
            if ich==36:
                break
            
        for ich in keys:
            print "[ CH %d, %s ] %d (0x%s)" % ( ich, channel_register_map[ich], adcs[ich]["adc"], adcs[ich]["hex"] )
        #print "-----------------------------------------"

    def changePortName(self,portname):
        self.config.setPortName( portname )
        self.config.saveCurrent()

