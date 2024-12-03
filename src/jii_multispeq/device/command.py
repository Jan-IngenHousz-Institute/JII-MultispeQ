"""
Commands are raw communication with the MultispeQ device.
"""

import json
import re
import warnings
from tabulate import tabulate
from jii_multispeq.measurement.checksum import strip_crc32 

def is_connected ( port=None ):
  """
  Test the connection to a MultispeQ.

  :param port: Port the MultisepQ is connected to.
  :type port: str

  :return: Instrument data and CRC32 checksum
  :rtype: dict, str

  """

  # Set timeout to 0.01 
  port.timeout = .01

  # Send handshake phrase
  port.write( "hello\n".encode() )

  # Data string
  data = ""

  # Read port
  while True:
    read = port.readline()
    data += read

    # Stop reading when linebreak received
    if "\n" in read.decode():
      break

  # Decode received data
  data = data.decode()

  # Regular expression to test for CRC32 checksum
  prog = re.compile( r'[}ABCDEF0-9]{9}' )
  result = prog.search( data )

  if result is None:
    raise ValueError("String has no checksum")
  
  data, crc32 = strip_crc32( data )

  json_str = data.replace("'", "\"")
  data = json.loads(json_str)

  info =[
      data["device_name"],
      data["device_version"],
      data["device_id"],
      data["device_battery"],
      data["device_firmware"]
    ]

  # Display Information
  output = tabulate( [info], headers=['Name', 'Version', 'ID', 'Battery', 'Firmware'])
  print( output )

  # Reset timeout
  port.timeout = None

  return data, crc32

def get_memory ( port=None ):
  """
  Get the MultispeQ setting saved in its memory (EEPROM).

  :param port: Port the MultisepQ is connected to.
  :type port: str

  :return: Instrument data and CRC32 checksum
  :rtype: dict, str

  """

  # Set timeout to 0.01 
  port.timeout = .01

  # Send handshake phrase
  port.write( "print_memory\n".encode() )

  # Data string
  data = ""

  # Regular expression to test for CRC32 checksum
  prog = re.compile( r'[}ABCDEF0-9]{9}' )

  # Read port
  while True:
    data += port.readline().decode()

    # Stop reading when linebreak received
    if prog.search( data ):
      break

  data, crc32 = strip_crc32( data )

  json_acceptable_string = data.replace("'", "\"")
  data = json.loads(json_acceptable_string)

  # Display Information
  output = tabulate( data.items() , headers=['Parameter', 'Value'])
  print( output )

  # Reset timeout
  port.timeout = None

  return data, crc32

def send_command ( port=None, command="" ):
  """
  Send a command to a MultispeQ device.

  :param port: Port the MultisepQ is connected to.
  :type port: str
  :param command: Command
  :type command: str
  
  :return: Instrument output
  :rtype: str

  :raises ValueError: if no port is defined
  :raises ValueError: if command is not provided as a string
  :raises Exception: if port is not open or device connected
  """

  if port is None:
    raise ValueError("A port for the MultispeQ needs to be defined")

  if not isinstance(command, str):
    raise ValueError("Provided command needs to be a string")
  
  # Check if the port is open
  if not port.is_open:
    raise Exception("Port not open, connect device to port first")

  # Set timeout to 0.01 
  port.timeout = .01

  # Check if it is a known command
  prog = re.compile( r"|".join(CMDS) )
  if not prog.match( command ):
    warnings.warn("Unknown command, it might not work.")

  # Send command
  port.write( command.encode() )

  # Read port
  data = ""
  while True:
    read = port.readline()
    print(read)
    data += read.decode()

    # Stop reading when linebreak received
    if "\n" in read.decode():
      break

  # Reset timeout
  port.timeout = None

  return data

## List of commands
CMDS = [
  "1053", "battery", "compiled", "configure_bluetooth", "device_info", "digital_write",
  "expr", "flow_calibration_set_point", "flow_calibration_setting",
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
  "set_thickness_quick", "set_user_defined", "single_pulse", "sleep", "start_watchdog",
  "stop_watchdog", "tcs_length", "temp", "testmode", "upgrade", "usb"
]
