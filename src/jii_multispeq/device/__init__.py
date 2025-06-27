"""
Serial communication with a MultispeQ device to take measurements
using protocols and send commands.
"""

from jii_multispeq.device.command import send_command, is_connected, get_memory, info, CMDS
from jii_multispeq.device.connection import connect, disconnect, get_ports
from jii_multispeq.device.settings import set_clamp_open, set_clamp_closed, set_shutdown_time, set_pilot_blink, set_usb_on, power_off, check_caliq_connection, calibrate_compass
