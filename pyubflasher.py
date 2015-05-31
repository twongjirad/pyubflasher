#!/usr/bin/env python
import argparse
import pyubflasher.actions as actions
from pyubflasher.flasherboard import FlasherBoard

def get_board():
    return FlasherBoard()

def get_parser( board ):
    parser = argparse.ArgumentParser( 'Commands to the Flasher Driver Board' )
    parser.add_argument( '--board-menu', action=actions.BoardMenuAction,
                         help='Print the Board\'s help menu' )
    parser.add_argument( '--query-all-registers',action=actions.DisplayAllRegistersAction,
                         help='Print the voltage values for all 36 registers' )
    parser.add_argument( '--query-register',action=actions.DisplayRegisterAction,nargs=1,
                         help='Print the voltage values for all 36 registers' )
    return parser

#def doit( args ):
#
#    if args.board_menu:
#        board.printMenu()

if __name__ == "__main__":
    #board = get_board()
    parser = get_parser( None )

    parser.parse_args()
