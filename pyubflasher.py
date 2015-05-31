#!/usr/bin/env python
import argparse
import pyubflasher.actions as actions
from pyubflasher.flasherboard import FlasherBoard

def get_board():
    return FlasherBoard()

def get_parser( board ):
    parser = argparse.ArgumentParser( 'Commands to the Flasher Driver Board' )
    # Help
    parser.add_argument( '--board-menu', action=actions.BoardMenuAction,
                         help='Print the Board\'s help menu' )

    # Get/Set Channel ADC Registers
    parser.add_argument( '--query-all-registers',action=actions.DisplayAllRegistersAction,
                         help='Print the voltage values for all 36 channels [0,36)' )
    parser.add_argument( '--query-register',action=actions.DisplayRegisterAction,nargs=1,
                         help='Print the voltage values for one channel. Allowed values=[0,36)' )
    parser.add_argument( '--set-all-registers',action=actions.SetAllRegisters,nargs=1,
                         help='Set ADC value for all channels.  Either hexstring \'[0x00,0xFF)\' or decminal \'[0,4096)\'.' )
    parser.add_argument( '--set-register',action=actions.SetChannelRegister,nargs=2,
                         help='Set ADC value \'A\' for channel \'N\'. ADC: hexstring \'[0x00,0xFF)\' or decminal \'[0,4096)\'. Channel: hex [0x10,0x33) or decimal [0,36).')
                         

    # Configuration
    parser.add_argument( '--restore-port-default',action=actions.RestorePortDefault,
                         help='Restore default port settings (e.g. name, baud rate)' )
    parser.add_argument( '--set-port', nargs=1, action=actions.SetPortName,
                         help='Set port (e.g. /dev/ttyUSB0)' )
    parser.add_argument( '--print-port',nargs=0,action=actions.PrintPortName,
                         help='Print the serial port name' )
    parser.add_argument( '--reload-fpga', action=actions.ReloadFPGAprogram, nargs=0,
                         help='Reload the FPGA program from copy stored on flash memory. Will wait 30 seconds before querying the device again.' )

    # Heart beat
    parser.add_argument( '--check-connection',nargs=0,action=actions.CheckConnection,
                         help='Check if we can talk to board still. If yes, returns \"CONNECTED\", otherwise \"DISCONNECTED\"' )
    return parser

#def doit( args ):
#
#    if args.board_menu:
#        board.printMenu()

if __name__ == "__main__":
    #board = get_board()
    parser = get_parser( None )

    parser.parse_args()
