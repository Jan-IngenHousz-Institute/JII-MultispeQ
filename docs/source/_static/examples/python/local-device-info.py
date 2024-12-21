"""
Example on how to get the device settings from
a connected MultispeQ via a serial connection.
"""

import jii_multispeq.device as _device
import jii_multispeq.measurement as _measurement

## Establish connection
_connection = _device.connect( "/com1" )

## Test if connection is open and device is communicating
if _device.is_connected( _connection ):

  ## Send the command for device settings (memory)
  response, crc32 = _device.get_memory( _connection )

  ## View response as a table
  _measurement.view( response )

## Close the connection
_device.disconnect( _connection )
