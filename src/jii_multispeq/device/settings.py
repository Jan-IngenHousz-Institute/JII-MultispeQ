"""
Settings for the MultispeQ device.

Most of the MultispeQ settings can be accessed and changed using the :func:`jii_multispeq.device.command.send_command` function.
For convenience and to make some of the more frequenetly used settings more accessible through the functions below.

:Example:

.. code-block:: python

   import jii_multispeq.device as _device
   import jii_multispeq.device.settings as _settings

   ## Establish connection
   _connection = _device.connect( "/com1" )

   ## Settings without a parameter
   _settings.clamp_closed( _connection )

   ## Settings with a parameter
   _settings.pilot_blink( _connection, "off" )
"""

from jii_multispeq.device.command import send_command

def set_clamp_open(connection):
  """
  Calibrate the open leaf clamp position. Hold the clamp open at approximately ~4mm and run the function to set the position.
    
  :param connection: Connection to the MultispeQ.
  :type connection: serial

  :return: None
  """
  send_command( connection, command="s+set_op+", verbose=True, is_silent=True )


def set_clamp_closed(connection):
  """
  Calibrate the closed leaf clamp position. Hold the clamp open at approximately ~2mm and run the function to set the position.

  :param connection: Connection to the MultispeQ.
  :type connection: serial

  :return: None
  """
  send_command( connection, command="s+set_cp+", verbose=True, is_silent=True )


def calibrate_compass(connection):
  """
  Calibrate the Instruments compass. Hold the device and move it in a steady spherical motion to calibrate 
  the internal compass after starting the calibration.
  
  :param connection: Connection to the MultispeQ.
  :type connection: serial

  :return: None
  """
  send_command( connection, command="scan_i2c+calibrate_magnetometer+", verbose=True )


def set_shutdown_time(connection, seconds=1800):
  """
  Shut down time to power down the device. It automatically shuts down after 30 minutes by default. 
  Hold the button for ~10s to restart it after shutdown.
  Adjust this timing by selecting a different shutdown interval.

  =============== =================
  Time in Minutes Setting (seconds)
  =============== =================
  10 min          600 (minimum)
  30 min          1800
  60 min          3600
  2 hr            7200
  =============== =================

  :param connection: Connection to the MultispeQ.
  :type connection: serial
  :param seconds: Shutdown time in seconds.
  :type seconds: int

  :return: None

  :raises ValueError: if baudrate is not defined or provided as an integer

  :Example:

  .. code-block:: python
     
     # Set shut down time to 30 min
     set_shutdown_time( _connection, 1800 )

  """

  if seconds is None or not isinstance(seconds, int):
    raise ValueError("The shutdown time needs to be defined in seconds and provided as an integer")

  if seconds < 600:
    raise ValueError("The shutdown time needs to be a minimum of 600 seconds")

  send_command( connection, command="set_shutdown_time+%s+" % seconds, verbose=True, is_silent=True )


def set_pilot_blink(connection, state='on'):
  """
  Device active. Blink the indicator light every 10 seconds to show that the device remains active.
    
  :param connection: Connection to the MultispeQ.
  :type connection: serial
  :param state: On/Off (on, 1) (off,0).
  :type state: int or string

  :return: None

  :raises ValueError: if state is not on, 1 or off, 0

  :Example:

  .. code-block:: python
     
     # Keep device powered while connected to USB
     set_pilot_blink( _connection, "on" )

  """

  state = state.lower() if isinstance(state, str) else state

  if state not in [0, 1, 'on', 'off']:
    raise ValueError(f"Invalid value '{state}'. Expected 0, 1, 'on', or 'off'.")
  
  if state == 'on':
    state = 1

  if state == 'off':
    state = 0

  send_command( connection, command="spm+%s+" % state, verbose=True, is_silent=True )


def set_usb_on(connection, state='on'):
  """
  USB connection. The device stays powered while connected via USB and will only shut down automatically 
  after disconnection based on the configured shutdown time.

  :param connection: Connection to the MultispeQ.
  :type connection: serial
  :param state: On/Off (on, 1) (off,0).
  :type state: int or string

  :return: None

  :Example:

  .. code-block:: python
     
     # Turn on pilot blink
     set_usb_on( _connection, "on" )

  """

  state = state.lower() if isinstance(state, str) else state

  if state not in [0, 1, 'on', 'off']:
    raise ValueError(f"Invalid value '{state}'. Expected 0, 1, 'on', or 'off'.")
  
  if state == 'on':
    state = 1

  if state == 'off':
    state = 0

  send_command( connection, command="usb_on+%s+" % state, verbose=True, is_silent=True )


def power_off(connection):
  """
  Turn off the Instrument completely.
    
  :param connection: Connection to the MultispeQ.
  :type connection: serial

  :return: None
  """
  send_command( connection, command="sleep", verbose=True, is_silent=True )


def check_caliq_connection(connection):
  """
  Check if the CaliQ and Instrument are properly communicating.
    
  :param connection: Connection to the MultispeQ.
  :type connection: serial

  :return: None
  """
  data = send_command( connection, command="xRb+128+", verbose=True )

  if data.strip() == '0':
    print('CaliQ device connected')