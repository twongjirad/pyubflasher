# pyubflasher
Control software for MicroBooNE LED Flasher Board

uses python modules: pyserial, json, argparse. json is built-in for Python >=2.6; argparse for Python >=2.7.  pyserial is external.

## Planned functionality

Basically, the code has to set and query the state of the board. The state is basically the voltage values delievered to each of th 26 LEDs.  Th values are held in 36 registers, whose address run sequentially starting from 0x10.  The state must be set/saved with a configuration database at some point.  The desired functions are:

* query if board is on
* reset firmware program
* query either all or individual channel values
* set values using config. database or from file
* zero out voltages

## Command List

```
usage: Commands to the Flasher Driver Board [-h] [--board-menu]
                                            [--query-all-registers]
                                            [--query-register QUERY_REGISTER]
                                            [--set-all-registers SET_ALL_REGISTERS]
                                            [--set-register SET_REGISTER SET_REGISTER]
                                            [--restore-port-default]
                                            [--set-port SET_PORT]
                                            [--print-port] [--reload-fpga]
                                            [--save-channel-adcs SAVE_CHANNEL_ADCS]
                                            [--load-channel-adcs LOAD_CHANNEL_ADCS]
                                            [--list-channel-configs]
                                            [--show-channel-config SHOW_CHANNEL_CONFIG]
                                            [--check-connection]

optional arguments:
  -h, --help            show this help message and exit
  --board-menu          Print the Board's help menu
  --query-all-registers
                        Print the voltage values for all 36 channels [0,36)
  --query-register QUERY_REGISTER
                        Print the voltage values for one channel. Allowed
                        values=[0,36)
  --set-all-registers SET_ALL_REGISTERS
                        Set ADC value for all channels. Either hexstring
                        '[0x00,0xFF)' or decminal '[0,4096)'.
  --set-register SET_REGISTER SET_REGISTER
                        Set ADC value 'A' for channel 'N'. ADC: hexstring
                        '[0x00,0xFF)' or decminal '[0,4096)'. Channel: hex
                        [0x10,0x33) or decimal [0,36).
  --restore-port-default
                        Restore default port settings (e.g. name, baud rate)
  --set-port SET_PORT   Set port (e.g. /dev/ttyUSB0)
  --print-port          Print the serial port name
  --reload-fpga         Reload the FPGA program from copy stored on flash
                        memory. Will wait 30 seconds before querying the
                        device again.
  --save-channel-adcs SAVE_CHANNEL_ADCS
                        Store channel data to file. default storage location
                        in pyubflasher/config
  --load-channel-adcs LOAD_CHANNEL_ADCS
                        Load channel data from file. file needs to be in
                        config folder pyubflasher/config
  --list-channel-configs
                        Show stored channel configurations
  --show-channel-config SHOW_CHANNEL_CONFIG
                        Print Channel ADC values stored in a configuration
                        file
  --check-connection    Check if we can talk to board still. If yes, returns
                        "CONNECTED", otherwise "DISCONNECTED"
```