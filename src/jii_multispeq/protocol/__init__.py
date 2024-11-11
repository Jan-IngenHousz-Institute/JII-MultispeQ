"""
The :mod:`~jii_multispeq.protocol` module helps extracting the protocol from the project
information, as well as extracting information from the protocol for a subsequent analysis
of the MultispeQ data based on settings and information within the used protocol.
"""

from jii_multispeq.protocol.protocol import get_protocol, get_protocol_name, get_subprotocol_labels, get_subprotocols_by_label, get_subprotocol_by_index
from jii_multispeq.protocol.v_arrays import get_v_arrays
