"""
Take measurements using the MultispeQ device connected to 
a serial port. The returned data can be analyzed and viewed.
"""

import datetime
import time
import json
import re
import warnings
import hashlib
import os
import pandas as pd

from jii_multispeq.constants import REGEX_RETURN_END
from jii_multispeq.measurement.sanitize import sanitize

from tabulate import tabulate

from jii_multispeq.measurement.checksum import strip_crc32

def measure ( connection=None, protocol=[{}], filename='auto', notes="", directory="./local/" ):
  """
  Take a measurement using a MultispeQ connected via a serial connection (USB or Bluetooth).

  :param connection: Connection to the MultispeQ.
  :type connection: serial
  :param protocol: Measurement Protocol
  :type protocol: str, dict or list
  :param filename: Name for saved measurement file. If set to None, no file is saved, Default name is current date and time.
  :type filename: str
  :param notes: Notes for the measurement
  :type notes: str
  :param directory: Directory the measurement is saved in. Default directory is "local".
  :type directory: str

  :return: The MultispeQ data is returned on success, otherwise None.
  :rtype: str
  
  :raises ValueError: if no connection is defined
  :raises ValueError: if no protocol for the MultispeQ is provided
  :raises ValueError: if protocol is not encoded as a string or dictionary
  :raises ValueError: if notes are not provided as a string
  :raises ValueError: if directory is not provided as a string
  :raises Exception: if connection is not open or device connected
  """

  start = datetime.datetime.now()

  if connection is None:
    raise ValueError("A connection for the MultispeQ needs to be defined")
  
  if not isinstance(protocol, (dict, str, list)):
    raise ValueError("Provided protocol needs to be a string or dictionary")
  
  if not isinstance(notes, str):
    raise ValueError("Provided notes have to be a string")
  
  if not isinstance(directory, str):
    raise ValueError("Provided directory has to be a string")
  
  if filename == 'auto':
    filename = start.strftime("%Y-%m-%d_%H%M")

  # Check if the connection is open
  if not connection.is_open:
    raise Exception("Connection not open, connect device to port first")

  # Check if the protocol is a dictionary and stringify
  if isinstance( protocol, (dict, list) ):
    protocol = json.dumps( protocol, separators=(',', ':'))

  # Flush input buffer
  connection.reset_input_buffer()

  # Write the protocol to the Instrument
  connection.write( protocol.encode() )

  # Send linebreak to start protocol
  connection.write( "\r\n".encode() )

  # Ensure data is actually sent before reading
  connection.flush()

  # Data string
  data = ""

  # Regular expression to test for CRC32 checksum
  prog = re.compile( REGEX_RETURN_END, re.M | re.I )

  # Read port
  while True:
    # Check if data is in the buffer
    if connection.in_waiting > 0:
      
      # Read bytes in buffer
      chunk = connection.read(connection.in_waiting).decode()
      data += chunk
    
      # Stop reading when linebreak received
      if prog.search( data ):
        break

    # Small delay to prevent excessive CPU usage
    time.sleep(0.01)

  # Remove linebreaks and split crc and data
  data, crc32 = strip_crc32( data )

  ## Sanitize Strings
  json_str = sanitize( data )

  try:
    data = json.loads(json_str)
  except json.decoder.JSONDecodeError as e:
    warnings.warn(e)
    return { 'Error': e }, crc32 #TODO: pass

  # Show a warning for battery below 25%
  if 'device_battery' in data and data['device_battery'] < 25:
    warnings.warn('Device battery low! Currently at %s%%, recharge soon.' % data['device_battery'])

  # Add filename
  if not filename is None:
    data['name'] = filename

  # Add Notes
  data['notes'] = notes

  # Add Date
  data['created_at'] = start.astimezone().isoformat()

  # Add Protocol
  data['protocol'] = json.loads(protocol)

  # Calculate Checksums
  data['md5_protocol'] = hashlib.md5( protocol.encode() ).hexdigest()
  data['md5_measurement'] = hashlib.md5( json_str.encode() ).hexdigest()

  ## Save file with measurements in notebook format
  if not filename is None:
    if not os.path.exists( directory ):
      os.makedirs( directory )

    path = os.path.join( directory, (filename + '.json') )

    ## Check if filename already exists. If true, " - #"" is attached
    i = 1
    while os.path.exists(path):
      path = os.path.join( directory, '%s - %s.json' % (filename,i) )
      i += 1

    ## Write to disk
    with open( path, 'w') as fp:
      json.dump(data, fp,  indent=2)

  return data, crc32


def analyze ( data=None, fn=None ):
  """
  Pipe data from the MultispeQ measurement to an analysis function.
  This can be done manually, but this helps with the convoluted
  structure of the measurement output.

  :param data: MultispeQ data output
  :type data: dict
  :param fn: Function to analyze the provided data
  :type fn: function
  
  :return: Analyzed data output, returns None if fails
  :rtype: dict

  :raises ValueError: if no data is provided
  :raises Exeption: if fn is not a function
  """

  if data is None:
    raise ValueError("No data is provided")
  
  if not isinstance(data, dict):
    raise ValueError("The provided data is not a dictionary")

  if fn is None:
    return data

  ## Output
  output = None

  if not hasattr( fn, '__call__'):
    raise Exception("No function is provided")
  
  try:
    ## Check if data is a dictionary and sample key is present
    if isinstance( data, dict ) and 'sample' in data:

      ## Check if sample is a list and has an element
      if isinstance( data['sample'], list ) and len(data['sample']) > 0:

        ## Now check if the first element in the sample list is a list as well that has an element
        # if isinstance( data['sample'][0], list ) and len(data['sample'][0]) > 0:
          
          ## Seems like it is the standard format
          # output = fn( data['sample'][0][0] )
          
          ## TODO: Not sure if we should add data back or how we address it...
          # And the raw data
          # for key in data['sample'][0][0].keys():
          #   output[key] = data['sample'][0][0].get(key, None)
        
        output = fn( data['sample'][0] )

      ## Perhaps some scrambled format, so sample is sent to the function
      else:
        output = fn( data['sample'] )

    ## Probably unknown data source, so it just gets passed to the function
    else:
      output = fn( data )

  except Exception as e:
    warnings.warn(e)
    pass

  ## Now that we have the output, so now the rest can be added
  keys = ['name', 'notes', 'created_at', 'protocol', 'md5_protocol', 'md5_measurement']
  
  ## Low level data information
  keys += ['device_name', 'device_version', 'device_id', 'device_battery', 'device_firmware']

  for key in keys:
    if key in data:
      output[key] = data.get(key, None)

  return output


def view ( data=None ):
  """
  Tabular display of data for a single measurent. If a parameter is a 
  list or dictionary or other type 'n/a' will be displayed as such
  content will not be plotted.

  :param data: MultispeQ data output
  :type data: dict

  :return: None
  :rtype: NoneType

  :raises ValueError: if no data is provided
  :raises ValueError: if data is not a dictionary
  """

  if data is None:
    raise ValueError("No data provided")
  
  if not isinstance(data, dict):
    raise ValueError("Provided data needs to be a dictionary")
  
  keys = sorted(data.keys(), key=str.lower)
  table_content = []

  for key in keys:
    value = data[key]
    vtype = type(value)

    if isinstance(value, (str, float, int )) or value is None:
      value = str(value)
    else:
      value = 'n/a'

    table_content.append([key, value, vtype])

  table = tabulate(table_content, headers=['Parameter', 'Value', 'Type'])
  
  print(table)

  return None


def to_df ( data=None, append=None ):
  """
  Adding data to dataframe. A new dataframe can be created
  or the data can be appended to an existing one, if the
  column format is the same.

  :param data: MultispeQ data output
  :type data: dict or list[dict]

  :return: None
  :rtype: NoneType

  :raises ValueError: if no data is provided
  :raises ValueError: if data is not a dictionary
  """

  if data is None:
    raise ValueError("No data provided")
  
  if not isinstance(data, (dict, list)):
    raise ValueError("Provided data needs to be a dictionary or list of dictionarys")
  
  df = pd.DataFrame( data )

  return df