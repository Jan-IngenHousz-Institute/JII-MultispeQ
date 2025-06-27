"""
Constants
"""

## Test for the end of MultispeQ output
REGEX_RETURN_END =      r'(([\]]{2}[\}][\r|\n]{1,})|([\}][0-9a-f]{8}[\s\r|\n]{0,})$)'
REGEX_RETURN_END_CLI =  r'(bad command:[\d\s\w]+)|(\})|(.*?Ready)$'

## Detect nil and NaN values
REGEX_NIL_NAN =         r'\s*"?(nil|-?NAN)"?\s*'

## Test for checksum at the data string
REGEX_CHECKSUM =        r'\}[0-9a-f]{8}$'
REGEX_CHECKSUM_RNS =    r'\}[0-9a-f]{8}\s?$'
