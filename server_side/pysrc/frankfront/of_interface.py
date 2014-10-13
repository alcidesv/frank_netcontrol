from __future__ import print_function, absolute_import

from flask import json
import re

from .app import app
import interface_read as iread

@app.route("/rest/net_interfaces")
def netinterface():
    idata = iread.gather_interface_data()
    inames = idata.pop('ith_names')
    ith_data = []
    extra_data = get_extra()
    for iname in inames:
        d = idata[ iname ]
        d['name'] = iname
        d['id'] = iname
        d['flags'] = ' '.join( idata[iname]['flags'] )
        d['dst_addr'] = idata[iname].get('dst_addr', None)
        d.update( extra_data[iname] )
        ith_data.append( d )
        
    ith_data.sort( key=(lambda x: x['name'] ) )
    return json.jsonify( net_interfaces = ith_data )

# We can get some more data from the interfaces by reading
# at /proc/net/dev
_is_net = re.compile( r'([a-z0-9-]+):' )
field_sep = re.compile( r'[ \t]+' )
titles = [
    'receive_bytes',
    'receive_packets',
    'receive_errs',
    'receive_drops',
    'receive_fifo',
    'receive_frame',
    'receive_compressed',
    'receive_multicast',
    
    'transmit_bytes',
    'transmit_packets',
    'transmit_errs',
    'transmit_drops',
    'transmit_fifo',
    'transmit_colls',
    'transmit_carrier',
    'transmit_compressed',    
    ]
def get_extra():
    r = {}
    with open('/proc/net/dev') as f:
        for (i, line) in enumerate( f ):
            if i < 2:
                continue 
            ith = {}
            mo = re.search( _is_net, line )
            if mo != None:
                iname = mo.group(1)
                fields = re.split( field_sep, line )
                del fields[0:2]
                for (j,field) in enumerate(fields):
                    field_name = titles[ j ]
                    ith[ field_name ] = int( field.strip('\n') )
                r[iname] = ith 
    return r
                    
                        