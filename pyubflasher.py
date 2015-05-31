#!/usr/bin/env python
import argparse
from pyubflasher.flasherboard import FlasherBoard

def get_board():
    return FlasherBoard()

def parse_args():
    print "parse args"
    parser = argparse.ArgumentParser( 'Commands to the Flasher Driver Board' )
    parser.add_argument( '--board-menu', action='store_true', default=False, 
                           help='Print the Board\'s help menu' )
    args = parser.parse_args()
    return args

def doit( args ):
    
    board = get_board()

    if args.board_menu:
        board.printMenu()

if __name__ == "__main__":
    args = parse_args()
    print args
    doit( args )
