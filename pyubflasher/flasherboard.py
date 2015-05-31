import serial
from pyubflasher.boardconfig import BoardConfig
import os,sys,time

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
        self.NCHANNELS = 36
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
            raise TypeError("Channel ID must be (decimal) integer in [0,%d)"%(self.NCHANNELS))
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
        self.port.write( 'RDI 10 %d\r'%(self.NCHANNELS))

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
            if ich==self.NCHANNELS:
                break
            
        for ich in keys:
            print "[ CH %d, %s ] %d (0x%s)" % ( ich, channel_register_map[ich], adcs[ich]["adc"], adcs[ich]["hex"] )
        #print "-----------------------------------------"

    def changePortName(self,portname):
        self.config.setPortName( portname )
        self.config.saveCurrent()


    def getIDinfo(self):
        self.openPort()
        self.port.write('ID\r')
        out = self.clearReadBuffer()
        return out[1:-1]

    def weStillConnected(self):
        try:
            idmsg = self.getIDinfo()
            if idmsg[0].strip()=="Module Type  : Micro Boone LED Driver":
                return True
            else:
                return False
        except:
            return False

    def reloadFPGAprogram(self):
        self.openPort()
        self.port.write('FF\r')
        print "Waiting 30 seconds for reset..."
        time.sleep(30)
        print "Checking for connection..."
        self.weStillConnected()

    def setChannelRegister(self, channel, adcval ):
        if type(adcval) is int:
            if adcval<0 or adcval>=4096:
                raise ValueError("Valid (decimal) ADC value is [0,4096). Given %d."%(adcval))
            hexval = "%x"%(adcval)
        elif type(adcval) is str:
            dec = int(adcval,16)
            if dec<0 or dec>=4096:
                raise ValueError("Valid (hex) ADC value is [0x0, 0xFF). Given %s (decimal=%d)"%(adcval,dec))
            hexval = adcval
        else:
            raise TypeValue("ADC value must be decimal value between [0,4096) or hex string between [0x0,0xFF). Give %s"%(type(adcval)))
            
        if type(channel) is int:
            if channel not in channel_register_map:
                raise ValueError("Invalid (decimal) channel number.  Given %d"%(channel))
            channel = channel_register_map[channel] # convert to Hex
        elif type(channel) is str:
            if "x" in channel:
                channel = channel.strip().split("x")[-1]
            decch = int(channel,16)
            if decch<int('0x10',16) or decch>=int('0x33',16):
                raise ValueError("Invalid (hex) channel number. Given 0x%s"%(channel))
        else:
            raise TypeValue("Channel value must be decimal value between [0,%d) or hex string between [0x0,0x33). Give %s"%(self.NCHANNELS,channel))

        # Finally do it
        self.openPort()
        self.port.write('WR %s %s\r'%(channel,hexval))
        time.sleep(0.1)
        out = self.clearReadBuffer()
        if len(out)!=2:
            print out
            raise RuntimeEror("Error Setting channel register: out[-2]")
        else:
            print out[0].strip()
        
    def setAllRegisters( self, adcval ):
        self.openPort()
        for ich in xrange(0,self.NCHANNELS ):
            self.setChannelRegister(ich, adcval )
