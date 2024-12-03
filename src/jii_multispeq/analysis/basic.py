"""
Helper functions to support the analysis of a single measurement
from a MultispeQ device.
"""

def GetLabelLookup ( data=None ):
  """
  Generate a protocol lookup table for a protocol set.

  :param data: The protocol output
  :type data: dict

  :return: Lookup table
  :rtype: dict
  """

  if data is None:
    return None

  if not 'set' in data:
     return None

  lookup = {}

  for i, item in enumerate(data['set']):
    if 'label' in item:
      if item['label'] not in lookup:
        lookup[item['label']] = []
        lookup[item['label']].append(i)
    else:
      if 'unknown' not in lookup:
        lookup['unknown'] = []
        lookup['unknown'].append(i)

  if len( lookup.items() )  == 0:
    return None
  
  else:
    return lookup


def GetProtocolByLabel ( label=None, data=None, array=False ):
  """
  Returns the protocol from within the protocol set matching the provided label.
  If only one label exists, one protocol object is returned.
  When multiple protocols in the set have the same label an array with all
  protcol objects of matching labels is returned.

  :param label: The label from the protocol set
  :type label: str
  :param data: The protocol data
  :type data: dict
  :param array: Always return an array, default is False
  :type array: bool

  :return: Single protocol or a list of protocols
  :rtype: dict or list[dict]
  """

  if label is None:
    return None
  
  if data is None:
    return None

  if not 'set' in data:
     return None

  if (array is None) or (not isinstance(array, bool )):
    array = False

  out = [a for a in data['set'] if ('label' in a) and (a['label'] == label)]

  if len(out)  == 0:
      return None
  if len(out) == 1:
      return out if array else out[0]
  else:
      return out

def GetIndexByLabel ( label=None, data=None, array=False ):
  """
  Find the positions for protocols within a protocol set matching the
  provided label. If only one label exists within a set, a number is returned.
  When multiple protocols in the set have the same label an array with all
  indexes of matching labels is returned.

  :param label: The label from the protocol set
  :type label: str
  :param data: The protocol data
  :type data: dict
  :param array: Always return an array, default is False
  :type array: bool

  :return: Single index or an array of indexes
  :rtype: int or list[int]
  """

  if label is None:
    return None
  
  if data is None:
    return None

  if not 'set' in data:
     return None

  if (array is None) or (not isinstance(array, bool )):
    array = False

  out = [i for i, a in enumerate(data['set']) if ('label' in a) and (a['label'] == label)]

  if len(out)  == 0:
      return None
  if len(out) == 1:
      return out if array else out[0]
  else:
      return out
