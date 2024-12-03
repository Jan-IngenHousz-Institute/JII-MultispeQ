"""
Take a measurement with a MultispeQ
loading protocol and analysis from
local file
"""

import jii_multispeq.measurement as measurement
import jii_multispeq.device as device

import protocols.template as protocol

ser = device.connect('/com1')

data, crc32 = device.measure( ser, protocol._protocol, 'example', 'Simple example for a MultispeQ measurment', './local-test' )

device.disconnect( ser )

out = protocol.analyze( data )

print( out )
