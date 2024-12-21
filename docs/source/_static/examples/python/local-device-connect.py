"""
Example on how to send a command to a connected
MultispeQ via a serial connection.
"""

import jii_multispeq.device as _device

## Establish connection
_connection = _device.connect( "/com1" )

## Test if connection is open and device is communicating
if _device.is_connected( _connection ):

  ## Send the command for device settings (memory)
  response = _device.send_command( _connection, "print_memory" )

  ## View response
  print( response )

## Close the connection
_device.disconnect( _connection )
