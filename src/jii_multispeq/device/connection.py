"""
Establish serial communication with MultispeQ device.
"""

import serial
from tabulate import tabulate
import serial.tools.list_ports as list_ports

def connect ( port=None, baudrate=115200, timeout=None ):
  """
  Connect a MultspeQ device to a serial port.

  :param port: Port the MultisepQ is connected to.
  :type port: str
  :param baudrate: Set the baudrate. Default is 115,200.
  :type baudrate: int
  :param timeout: Set the timeout. Derault is 0.01
  :type timeout: float

  :return: Serial connection or None if connection fails.
  :rtype: serial

  :raises ValueError: if port is not defined
  :raises ValueError: if port is not provided as a string
  :raises ValueError: if baudrate is not defined or provided as an integer
  :raises ValueError: if timeout is not provided as a float
  :raises SerialExeption: if device is not connected
  """

  if port is None:
    raise ValueError("No port is provided")
  
  if not isinstance(port, str):
    raise ValueError("The port name needs to be a string")
  
  if baudrate is None or not isinstance(baudrate, int):
    raise ValueError("The baudrate needs to be defined and provided as an integer")

  if not timeout is None and not isinstance(timeout, float):
    raise ValueError("Timeout needs to be defined as a float")

  connection = serial.Serial( port=port, baudrate=baudrate, timeout=timeout )

  if not connection.is_open:
    raise serial.SerialException("Device not connected")
  
  print("Connected Opened")

  return connection


def disconnect ( connection=None ):
  """
  Disconnect device from serial port.

  :param port: Port the MultisepQ is connected to.
  :type port: str

  :return: None
  """

  if connection.is_open:
    connection.close()
    print("Connection closed")
  else:
    print("Connection already closed")

  return None


def get_ports ():
  """
  List available serial ports.

  :return: None
  """

  ports = []
  for p in list_ports.comports():
    ports.append( [p.device, p.name, p.description, p.manufacturer, p.product] )

  output = tabulate( ports, headers=['Port', 'Name', 'Description', 'Manufacturer', 'Product'])
  print( output )

  return None
