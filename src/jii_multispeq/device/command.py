"""
Commands are raw communication with the MultispeQ device.
"""

import json
import re
import time
import warnings
from tabulate import tabulate
from jii_multispeq.measurement.checksum import strip_crc32
from jii_multispeq.measurement.sanitize import sanitize
from jii_multispeq.constants import REGEX_RETURN_END, REGEX_RETURN_END_CLI

def is_connected ( connection=None ):
  """
  Test the connection to a MultispeQ.

  :param connection: Connection to the MultispeQ.
  :type connection: serial

  :return: True if a MultispeQ is connected, otherwise False
  :rtype: bool

  """

  # Set timeout to 0.01 
  connection.timeout = .01

  if not connection.is_open:
    return False

  # Send handshake phrase
  data = send_command( connection, "hello" )

  connection.timeout = None

  # Test if phrase MultispeQ Ready was received
  if data.strip() == 'MultispeQ Ready':
    print("MultispeQ found")
    return True
  
  return False

def get_memory ( connection=None, verbose=False ):
  """
  Get the MultispeQ setting saved in its memory (EEPROM).

  :param connection: Connection to the MultispeQ.
  :type connection: serial

  :return: Instrument data and CRC32 checksum
  :rtype: dict, str

  """

  # Set timeout to 0.01 
  connection.timeout = .01

  # Send handshake phrase
  connection.write( "print_memory".encode() )

  # Send linebreak to start command
  connection.write( "\r\n".encode() )

  # Data string
  data = ""

  # Regular expression to test for CRC32 checksum
  prog = re.compile( REGEX_RETURN_END )

  # Read port
  while True:
    read = connection.readline()
    
    # Decode and append received data
    data += read.decode()

    # Stop reading when linebreak received
    if prog.search(data):
      break

  data, crc32 = strip_crc32( data )
def get_memory ( connection=None, verbose=False ):
  """
  Get the MultispeQ setting saved in its memory (EEPROM).

  :param connection: Connection to the MultispeQ.
  :type connection: serial
  :param verbose: Print out data (default: False)
  :type verbose: bool

  :return: Instrument memory
  :rtype: dict

  """

  # Send command
  data = send_command( connection, "print_memory", False)

  # Sanitize quotes
  data = sanitize( data )

  try:
    data = json.loads(data)
    pass
  except json.JSONDecodeError as e:
    print(e)
    pass

  # Display Information
  if verbose:
    output = tabulate( data.items() , headers=['Parameter', 'Value'])
    print( output )

  # Reset timeout
  connection.timeout = None

  return data

def send_command ( connection=None, command="", verbose=False ):
  """
  Send a command to a MultispeQ device.

  :param connection: Connection to the MultispeQ.
  :type connection: serial
  :param command: Command
  :type command: str
  
  :return: Instrument output
  :rtype: str

  :raises ValueError: if no connection is defined
  :raises ValueError: if command is not provided as a string
  :raises Exception: if connection is not open or device connected
  """

  if connection is None:
    raise ValueError("A connection for the MultispeQ needs to be defined")

  if not isinstance(command, str):
    raise ValueError("Provided command needs to be a string")
  
  # Check if the connection is open
  if not connection.is_open:
    raise Exception("Connection not open, connect device or port locked by other application")

  # Set timeout to 0.01 
  connection.timeout = .01

  # Check if it is a known command
  prog = re.compile( r"|".join(CMDS) )
  if not prog.search( command ):
    warnings.warn("Unknown command, device or script might get stuck.")

  prog_cli = re.compile( REGEX_RETURN_END_CLI, re.MULTILINE )
  prog = re.compile( REGEX_RETURN_END )

  # Flush input buffer
  connection.reset_input_buffer()

  # Send command
  connection.write( command.encode() )

  # Send linebreak to start command
  connection.write( "\r\n".encode() )

  # Ensure data is actually sent before reading
  connection.flush()

  # Read port
  data = ""
  chunk = ""
  while True:

    if connection.in_waiting > 0:
      chunk = connection.read(connection.in_waiting).decode()
      data += chunk

      if verbose is True:
        print(chunk)

      # Stop reading when linebreak received
      if prog.search(chunk) or prog_cli.search(chunk):

        # Brief wait to ensure no more data is coming
        time.sleep(0.05)
            
        # Final check - if no more data waiting, we're done
        if connection.in_waiting == 0:
          break

  # Reset timeout
  connection.timeout = None

  return data

## List of commands
CMDS = [
  "1000", "1007", "1053", "battery", "compiled", "configure_bluetooth", "calibrate_magnetometer", "device_info",
  "digital_write", "expr", "flow_calibration_set_point", "flow_calibration_setting",
  "flow_calibration_value", "flow_off", "flow_v", "get_flow",  "hall", "hello", "indicate",
  "indicate_off", "light", "memory", "on_5v", "p2p", "par_led", "print_all", "print_date",
  "print_magnetometer", "print_magnetometer_bias", "print_memory","pulse", "readonce",
  "reboot", "reset", "reset_flow_calibration", "reset_flow_zero_point", "scan_i2c",
  "set_accelerometer", "set_accelerometer_bias", "set_colorcal1", "set_colorcal2",
  "set_colorcal3", "set_colorcal_blanks", "set_cp", "set_dac", "set_date",
  "set_default_flow_rate", "set_detector1_offset", "set_detector2_offset",
  "set_detector3_offset", "set_detector4_offset", "set_device_info", "set_energy_save_time",
  "set_flow", "set_led_par", "set_magnetometer", "set_magnetometer_bias", "set_op",
  "set_open_closed_positions", "set_par", "set_serial", "set_shutdown_time", "set_thickness",
  "set_thickness_quick", "set_user_defined", "single_pulse", "sleep", "spm", "start_watchdog",
  "stop_watchdog", "tcs_length", "temp", "testmode", "upgrade", "usb", "usb_on", "xRb"
]
