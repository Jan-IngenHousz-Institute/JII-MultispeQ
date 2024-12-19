"""
Constants
"""

## Test for the end of MultispeQ output
REGEX_RETURN_END =      r'([\}][\r|\n]{0,})|(\]\]\}[\r\n]+)|(\}[0-9a-f]{8}\s*$)'

## Detect nil and NaN values
REGEX_NIL_NAN =         r'[\"\s]*(nil|-?NAN)[\"\s]*'

## Test for checksum at the data string
REGEX_CHECKSUM =        r'\}[0-9a-f]{8}$'
REGEX_CHECKSUM_RNS =    r'\}[0-9a-f]{8}[\s\r|\n]?$'
