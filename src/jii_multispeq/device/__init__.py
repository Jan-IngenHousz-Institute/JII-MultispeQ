"""
Serial communication with a MultispeQ device to take measurements
using protocols and send commands.
"""

from jii_multispeq.device.command import send_command, is_connected, get_memory, CMDS
from jii_multispeq.device.connection import connect, disconnect, get_ports
