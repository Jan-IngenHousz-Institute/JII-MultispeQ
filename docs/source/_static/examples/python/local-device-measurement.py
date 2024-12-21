"""
Take a single SPAD measurement with a MultispeQ
without saving it to a local file
"""

import jii_multispeq.measurement as _measurement
import jii_multispeq.device as _device

## MultispeQ Protocol
spad_protocol = [{
  "spad": [1]
}]

## MultispeQ Response Analysis
def spad_fn( _data ):
  output = {}
  output["SPAD"] = _data["spad"][0]
  return output

## Establish connection
_connection = _device.connect( "/com1" )

## Test if connection is open and device is communicating
if _device.is_connected( _connection ):

  data, crc32 = _measurement.measure( _connection, spad_protocol, 
                                     None, 
                                     'Single SPAD meaurement' )

  ## Run the analysis function
  data = _measurement.analyze( data, spad_fn )

  ## View response as a table
  _measurement.view( data )

## Close the connection
_device.disconnect( _connection )
