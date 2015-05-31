import argparse
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

