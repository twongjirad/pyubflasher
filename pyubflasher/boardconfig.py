import json
import os,sys

class BoardConfig:

    def __init__( self, configfile ):
        if not os.path.exists( configfile ):
            raise RuntimeError( 'Could not find configuration file %s'%(configfile) )
        self.config_file = configfile
        try:
            f = open( configfile, 'r' )
            self.json = json.loads( f.read() )
            f.close()
        except:
            raise RuntimeError(  'Could not load the configuration json file.' )

        self.baud_rate = self.json['config']['baud']
        self.port      = self.json['config']['port']
        
    def setPortName(self, portname):
        if "/dev/tty" not in portname:
            print "The port name seems fishy. Are you sure this is right?"
            print "OK..., but run --restore-port-default to go back to default port when this does not work."
        self.port = portname
        self.json['config']['port'] = portname
    def saveCurrent(self ):
        f = open(self.config_file,'w')
        json.dump( self.json, f )
        f.close()

