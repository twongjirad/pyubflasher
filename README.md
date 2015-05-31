# pyubflasher
Control software for MicroBooNE LED Flasher Board

uses pyserial

# Planned functionality

Basically, the code has to set and query the state of the board. The state is basically the voltage values in each of the 36 registers.  The state must coordinate with a configuration database at some point.  The desired functions are:

* query if board is on
* reset firmware program
* query all and individual channel values
* set values using config. database or from file
* zero out voltages

