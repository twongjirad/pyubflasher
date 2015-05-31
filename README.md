# pyubflasher
Control software for MicroBooNE LED Flasher Board

uses python modules: pyserial, json, argparse. json is built-in for Python >=2.6; argparse for Python >=2.7.  pyserial is external.

# Planned functionality

Basically, the code has to set and query the state of the board. The state is basically the voltage values delievered to each of th 26 LEDs.  Th values are held in 36 registers, whose address run sequentially starting from 0x10.  The state must be set/saved with a configuration database at some point.  The desired functions are:

* query if board is on
* reset firmware program
* query either all or individual channel values
* set values using config. database or from file
* zero out voltages

