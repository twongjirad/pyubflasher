import argparse
import os,sys
from pyubflasher.flasherboard import FlasherBoard

class BoardMenuAction( argparse.Action ):
    def __init__(self, option_strings, nargs=0, dest=None, **kwargs ):
        super(BoardMenuAction,self).__init__(option_strings=option_strings, 
                                             nargs=nargs,
                                             dest=dest, 
                                             **kwargs )
    def __call__(self,parser,namespace,values,option_string=None):
        board = FlasherBoard()
        board.printMenu()
        setattr(namespace,self.dest,values)

class DisplayAllRegistersAction( argparse.Action ):
    def __init__(self, option_strings, nargs=0, dest=None, **kwargs ):
        super(DisplayAllRegistersAction,self).__init__(option_strings=option_strings, 
                                                       nargs=nargs,
                                                       dest=dest, 
                                                       **kwargs )
    def __call__(self,parse,namespace,values,option_string=None):
        board = FlasherBoard()
        board.queryAllRegisters()
        setattr(namespace,self.dest,values)

class DisplayRegisterAction( argparse.Action ):
    def __init__(self, option_strings, nargs=1, dest=None, **kwargs ):
        super(DisplayRegisterAction,self).__init__(option_strings=option_strings, 
                                                   nargs=nargs,
                                                   dest=dest, 
                                                   **kwargs )
    def __call__(self,parse,namespace,values,option_string=None):
        board = FlasherBoard()
        try:
            chid = int(values[0])
        except:
            raise TypeError("Channel ID must be (decimal) integer. Given %s"%(values[0]))
        if chid<0 or chid>=36:
            raise ValueError("Channel ID must be between [0,36). Given %s"%(values[0]))

        board.queryRegister( chid )
        setattr(namespace,self.dest,values)


class SetPortName( argparse.Action ):
    def __init__(self, option_strings, nargs=1, dest=None, **kwargs ):
        super(SetPortName,self).__init__(option_strings=option_strings,nargs=nargs,dest=dest,**kwargs)
    def __call__(self, parse, namespace, values, option_string=None ):
        board = FlasherBoard()
        board.changePortName( values[0] )

class RestorePortDefault( argparse.Action ):
    def __init__(self, option_strings, nargs=0, dest=None, **kwargs ):
        super(RestorePortDefault,self).__init__(option_strings=option_strings,nargs=nargs,dest=dest,**kwargs)
    def __call__(self, parse, namespace, values, option_string=None ):
        mypath = os.path.dirname(os.path.realpath(__file__))
        config_file = mypath+"/config/currentconfig.json"
        os.system("cp %s/config/boardconfig.json %s"%(mypath,config_file))        

class PrintPortName( argparse.Action ):
    def __init__(self, option_strings, nargs=0, dest=None, **kwargs ):
        super(PrintPortName,self).__init__(option_strings=option_strings,nargs=nargs,dest=dest,**kwargs)
    def __call__(self, parse, namespace, values, option_string=None ):
        board = FlasherBoard()
        print "Port Name: ",board.config.port

class CheckConnection( argparse.Action ):
    def __init__(self, option_strings, nargs=0, dest=None, **kwargs ):
        super(CheckConnection,self).__init__(option_strings=option_strings,nargs=nargs,dest=dest,**kwargs)
    def __call__(self, parse, namespace, values, option_string=None ):
        board = FlasherBoard()
        if board.weStillConnected():
            print "CONNECTED"
        else:
            print "DISCONNECTED"

class ReloadFPGAprogram( argparse.Action ):
    def __init__(self, option_strings, nargs=0, dest=None, **kwargs ):
        super(ReloadFPGAprogram,self).__init__(option_strings=option_strings,nargs=nargs,dest=dest,**kwargs)
    def __call__(self, parse, namespace, values, option_string=None ):
        board = FlasherBoard()
        board.reloadFPGAprogram()
    
class SetAllRegisters( argparse.Action ):
    def __init__(self, option_strings, nargs=1, dest=None, **kwargs ):
        super(SetAllRegisters,self).__init__(option_strings=option_strings,nargs=nargs,dest=dest,**kwargs)
    def __call__(self, parse, namespace, values, option_string=None ):
        adc = values[0]
        if "0x" in adc:
            adcval = adc.strip().split("x")[-1]
        else:
            adcval = int(adc)
        board = FlasherBoard()
        board.setAllRegisters( adcval )

class SetChannelRegister( argparse.Action ):
    def __init__(self, option_strings, nargs=2, dest=None, **kwargs ):
        super(SetChannelRegister,self).__init__(option_strings=option_strings,nargs=nargs,dest=dest,**kwargs)
    def __call__(self, parse, namespace, values, option_string=None ):
        ch = values[0]
        if "0x" in ch:
            chval = ch.strip().split("x")[-1]
        else:
            chval = int(ch)

        adc = values[1]
        if "0x" in adc:
            adcval = adc.strip().split("x")[-1]
        else:
            adcval = int(adc)

        board = FlasherBoard()
        board.setChannelRegister( chval, adcval )
    
class SaveChannelADCs( argparse.Action ):
    def __init__(self, option_strings, nargs=1, dest=None, **kwargs ):
        super(SaveChannelADCs,self).__init__(option_strings=option_strings,nargs=nargs,dest=dest,**kwargs)
    def __call__(self, parse, namespace, values, option_string=None ):
        mypath = os.path.dirname(os.path.realpath(__file__))
        print "All your configurations are belong to us: in %s/config"%(mypath)
        fname = mypath + "/config/" + os.path.basename( values[0] )
        board = FlasherBoard()
        board.saveChannelValues( fname )

class LoadChannelADCs( argparse.Action ):
    def __init__(self, option_strings, nargs=1, dest=None, **kwargs ):
        super(LoadChannelADCs,self).__init__(option_strings=option_strings,nargs=nargs,dest=dest,**kwargs)
    def __call__(self, parse, namespace, values, option_string=None ):
        mypath = os.path.dirname(os.path.realpath(__file__))
        fname = mypath + "/config/" + os.path.basename( values[0] )
        if not os.path.exists(fname):
            raise RunTimeError("Could not find config file: needs to be in config folder %s/config"%(mypath))
        board = FlasherBoard()
        board.loadChannelValues( fname )

class ListChannelConfigs( argparse.Action ):
    def __init__(self, option_strings, nargs=0, dest=None, **kwargs ):
        super(ListChannelConfigs,self).__init__(option_strings=option_strings,nargs=nargs,dest=dest,**kwargs)
    def __call__(self, parse, namespace, values, option_string=None ):
        board = FlasherBoard()
        board.listChannelConfigs()

class ShowChannelConfig( argparse.Action ):
    def __init__(self, option_strings, nargs=1, dest=None, **kwargs ):
        super(ShowChannelConfig,self).__init__(option_strings=option_strings,nargs=nargs,dest=dest,**kwargs)
    def __call__(self, parse, namespace, values, option_string=None ):
        board = FlasherBoard()
        board.showChannelConfig( values[0] )

class QueryTransientWidth( argparse.Action ):
    def __init__(self, option_strings, nargs=0, dest=None, **kwargs ):
        super(QueryTransientWidth,self).__init__(option_strings=option_strings,nargs=nargs,dest=dest,**kwargs)
    def __call__(self, parse, namespace, values, option_string=None ):
        board = FlasherBoard()
        board.printTransientWidth()

class SetTransientWidth( argparse.Action ):
    def __init__(self, option_strings, nargs=1, dest=None, **kwargs ):
        super(SetTransientWidth,self).__init__(option_strings=option_strings,nargs=nargs,dest=dest,**kwargs)
    def __call__(self, parse, namespace, values, option_string=None ):
        board = FlasherBoard()
        board.setTransientWidth(values[0])
    
class QueryLEDTriggerDelay( argparse.Action ):
    def __init__(self, option_strings, nargs=0, dest=None, **kwargs ):
        super(QueryLEDTriggerDelay,self).__init__(option_strings=option_strings,nargs=nargs,dest=dest,**kwargs)
    def __call__(self, parse, namespace, values, option_string=None ):
        board = FlasherBoard()
        board.printLEDTriggerDelay()

class SetLEDTriggerDelay( argparse.Action ):
    def __init__(self, option_strings, nargs=1, dest=None, **kwargs ):
        super(SetLEDTriggerDelay,self).__init__(option_strings=option_strings,nargs=nargs,dest=dest,**kwargs)
    def __call__(self, parse, namespace, values, option_string=None ):
        board = FlasherBoard()
        board.setLEDTriggerDelay(values[0])
    
