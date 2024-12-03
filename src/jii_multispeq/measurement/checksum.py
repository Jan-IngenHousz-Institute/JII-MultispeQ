"""
Checksum handeling and calculation for MultispeQ Measurements.
"""

import zlib
import warnings

def get_crc32( data=None ):
  """
  Calculate a CRC32 checksum from data and represent as HEX.

  :param data: Data stream
  :type data: str

  :return: HEX CRC32 checksum
  :rtype: str

  :raises ValueError: if no data is provided
  :raises ValueError: if provided data is not a string
  """

  if data is None:
    raise ValueError("Data not provided")
  
  if not isinstance(data, str):
    raise ValueError("Provided data needs to be a string")

  sum = zlib.crc32( data.encode('utf-8') )

  return hex(sum)[2:].upper()

def strip_crc32 ( data=None ):
  """
  Strip CRC32 checksum from data string and return data and checksum separately.

  :param data: Data stream
  :type data: str

  :return: data string and HEX CRC32 checksum
  :rtype: str, str

  :raises ValueError: if no data is provided
  :raises ValueError: if provided data is not a string
  """

  if data is None:
    raise ValueError("Data not provided")
  
  if not isinstance(data, str):
    raise ValueError("Provided data needs to be a string")
  
  # Decode received data
  data = data.strip()
  
  crc32 = data[-8:]
  data = data[:-8]

  if crc32 != get_crc32( data ):
    warnings.warn("Checksum missmatch. There might has been an issue during data transfer.")

  return data, crc32
