import json
import os,sys

class BoardConfig:

    def __init__( self, configfile ):
        if not os.path.exists( configfile ):
            raise RuntimeError( 'Could not find configuration file %s'%(configfile) )
            
        try:
            f = open( configfile, 'r' )
            self.json = json.loads( f.read() )
        except:
            raise RuntimeError(  'Could not load the configuration json file.' )

        self.baud_rate = self.json['config']['baud']
        self.port      = self.json['config']['port']
