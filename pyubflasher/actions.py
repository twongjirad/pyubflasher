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
