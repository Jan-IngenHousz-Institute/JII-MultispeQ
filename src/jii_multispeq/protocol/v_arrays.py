"""
MultispeQ protocols can contain a so called ``v_arrays`` that allow to define 
values as variabls, which can be used throughout the protocol, so the value
itself doesn't need to be repeated multiple times throughout the protocol.
The functions allow to access the ``v_arrays`` themselfs as well as
accessing specific variable values, so they can be available for the later
data analysis.
"""

import numpy as np

def get_v_arrays ( protocol=None ):
  """
  Get the ``v_arrays`` (variable arrays) from a given protocol.
  See :func:`~jii_pq_analysis.protocol.get_protocol` on how to extract a single protocol.

  :param protocol: Single MultispeQ Protocol
  :type protocol: dict
  
  :returns: ``v_arrays`` content
  :rtype: dict
  
  :raises ValueError: If no protocol is provided.
  :raises ValueError: If protocol is not provided as a dictionary.
  :raises Exception: If the provided protocol doesn't have a v_arrays.
  """

  if protocol is None:
    raise ValueError("No protocol provided")

  if not isinstance( protocol, dict ):
    raise ValueError("Provided Protocol needs to be formatted as a dictionary")

  if "v_arrays" not in protocol:
     raise Exception("Provided Protocol has no v_arrays")

  return protocol['v_arrays']
