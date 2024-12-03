"""
Take measurements using the MultispeQ device connected to 
a serial port. The returned data can be analyzed and viewed.
"""

import datetime
import json
import re
import warnings
import hashlib
import os

from tabulate import tabulate

from jii_multispeq.measurement.checksum import get_crc32, strip_crc32

def measure ( port=None, protocol=[{}], filename=None, notes="", directory="./local/" ):
  """
  Take a measurement using a MultispeQ connected via a serial connection (USB or Bluetooth).

  :param port: Port the MultisepQ is connected to.
  :type port: str
  :param protocol: Measurement Protocol
  :type protocol: str or dict
  :param name: Name for meaurement file. Default name is current date and time.
  :type name: str
  :param notes: Notes for the measurement
  :type notes: str
  :param directory: Directory the measurement is saved in. Default directory is "local".
  :type directory: str

  :return: The MultispeQ data is returned on success, otherwise None.
  :rtype: str
  
  :raises ValueError: if no port is defined
  :raises ValueError: if no protocol for the MultispeQ is provided
  :raises ValueError: if protocol is not encoded as a string or dictionary
  :raises ValueError: if notes are not provided as a string
  :raises ValueError: if directory is not provided as a string
  :raises Exception: if port is not open or device connected
  """

  start = datetime.datetime.now()

  if port is None:
    raise ValueError("A port for the MultispeQ needs to be defined")
  
  if not isinstance(protocol, (dict, str)):
    raise ValueError("Provided protocol needs to be a string or dictionary")
  
  if not isinstance(notes, str):
    raise ValueError("Provided notes have to be a string")
  
  if not isinstance(directory, str):
    raise ValueError("Provided directory has to be a string")
  
  if filename is None:
    filename = start.strftime("YYYY-MM-DD HHmmss")

  # Check if the port is open
  if not port.is_open:
    raise Exception("Port not open, connect device to port first")

  # Check if the protocol is a dictionary and stringify
  if isinstance( protocol, dict ):
    protocol = json.dumps( protocol, indent=None)

  # Write the protocol to the Instrument
  port.write( protocol.encode() )

  # Data string
  data = ""

  # Regular expression to test for CRC32 checksum
  prog = re.compile( r'[}ABCDEF0-9]{9}' )

  # Read port
  while True:
    data += port.readline()

    # Stop reading when linebreak received
    if prog.search( data.decode() ):
      break
  
  # Remove linebreaks and split crc and data
  data, crc32 = strip_crc32( data )

  json_str = data.replace("'", "\"")

  """
  {
    "device_name":"My Instrument",
    "device_version":"1",
    "device_id":"ff:ff:ff:ff",
    "device_battery":15,
    "device_firmware":2.21,
    "sample":[
        {
            "protocol_id":"123",
            "light_intensity":100,
            "data_raw":[]
        }
    ]
  }
  """

  try:
    data = json.loads(json_str)
  except json.decoder.JSONDecodeError as e:
    warnings.warn(e)
    data = { 'Error': e }
    pass

  # Show a warning for battery below 25%
  if 'device_battery' in data and data['device_battery'] < 25:
    warnings.warn("Device battery low! Currently at %s%, recharge soon." % data['device_battery'])

  # Add filename
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
  if not os.path.exists( directory ):
    os.makedirs( directory )

  path = os.path.join( directory, (filename + '.json') )

  ## Check if filename already exists, if not attach crc32
  if os.path.exists(path):
    path = os.path.join( directory, (filename + ' - ' + get_crc32(json_str) + '.json') )
    warnings.warn("File already existed, and file saved as %s" % path )

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
        if isinstance( data['sample'][0], list ) and len(data['sample'][0]) > 0:
          
          ## Seems like it is the standard format
          output = fn( data['sample'][0][0] )
          
          ## TODO: Not sure if we should add data back or how we address it...
          # And the raw data
          # for key in data['sample'][0][0].keys():
          #   output[key] = data['sample'][0][0].get(key, None)

        ## Perhaps some scrambled format, so sample is sent to the function  
        else:
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


def to_df ( data=None ):
  """
  Tabular display of data for a single measurent. If a parameter is a 
  list or dictionary or other type 'n/a' will be displayed as such
  content will not be plotted.

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