"""
Functions to work with MultispeQ protocols. This includes getting the protocol
from the project information and extracting information from the protocol code
including subprotocols by their labels or positions within the protocol.
"""

import json

def get_protocol( project=None, index=0 ):
  """
  Return the protocol for a project given the project information.
  A project's protocol for a MultispeQ is a list of protocols. This 
  function is returning a single protocol from the list.

  :param project: Project information as returned by :func:`jii_multispeq.project.get`
  :type project: dict
  :param index: Protocol position in list of project protocols. The default protocol position is 0.
  :type index: int

  :returns: The code of the selected protocol.
  :rtype: dict

  :raises ValueError: if no project information is provided
  :raises KeyError: if the key protocol_json is missing in the project information
  :raises ValueError: if the protocol_json value is not formatted properly
  :raises ValueError: if the provided index is not an integer
  :raises IndexError: if the provided index is out of range
  """

  if project is None:
     raise ValueError("No Project information provided")

  if "protocol_json" not in project:
     raise KeyError("Provided Project information does not contain a protocol (missing key: protocol_json)")

  if not isinstance(project["protocol_json"], str):
     raise ValueError("Protocol is not formatted as a string")
    
  if (index is None) or not isinstance(index, int):
    raise ValueError("Selected protocol index needs to be an integer (e.g. 0)")
  
  protocol = json.loads(project['protocol_json'])

  if index not in range(0,len(protocol)):
    raise IndexError("Provided Index %s out of range" % index)

  return protocol[index]

def get_protocol_name(project=None, index=0 ):
  """
  Get the protocol name from the provided Project.
  The PhotosynQ_Py library is creating a dictionary of data frames, with the
  keys being the protocol names. Most projects have only one protocol, but
  some projects in the past had multiple.

  :param project: Project information as returned by :func:`jii_multispeq.project.get`
  :type project: dict
  :param index: Protocol position in list of project protocols. The default protocol position is 0.
  :type index: int

  :returns: a string with the protocol name
  :rtype: string
  
  :raises ValueError: if no project information is provided
  :raises KeyError: if the protocols key is missing in the project information
  :raises IndexError: if provided index is out of range for the protocols list
  """

  # Display exeption if no dictionary is provided
  if project is None:
    raise ValueError("Provided Project has no information")
  
  # Check if first level keys are available
  if "protocols" not in project:
    raise KeyError("Provided Project doesn't seem to have the correct format, missing key")

  if index not in range(0,len(project["protocols"])):
    raise IndexError("Provided Index %s out of range" % index)
    
  return project["protocols"][index]["name"]

def get_subprotocol_labels( protocol=None ):
  """
  Returns a list of labels for each subprotocol. In case a sub-protocol has no
  label, ``None`` is returned.

  :param protocol: Protocol as returned by :func:`jii_multispeq.protocol.get_protocol`
  :type protocol: dict

  :returns: list of sub-protocols label
  :rtype: list[str]

  :raises ValueError: If no protocol is provided
  :raises ValueError: If the provided protocol is not a dictionary
  :raises KeyError: If the _protocol_set_ key is missing in the provided protocol
  """

  if protocol is None:
    raise ValueError("No Protocol provided")

  if not isinstance(protocol, dict):
    raise ValueError("Provided Protocol needs to be formatted as a dictionary")

  if "_protocol_set_" not in protocol:
    raise KeyError("The selected protocol has no sub-protocols (requires: _protocol_set_)")
  
  labels = []

  for sub_protocol in protocol['_protocol_set_']:
    if ('label' in sub_protocol):
      labels.append(sub_protocol['label'])
    else:
      labels.append(None)

  return labels

def get_subprotocols_by_label( protocol=None, label="" ):
  """
  Returns a list of sub_protocols in a protocol with given label value
  label is the desired label. If the protocol does not have labels, will be ignored.
  protocol is the protocol to be seaerched.

  :param protocol: Protocol as returned by :func:`jii_multispeq.protocol.get_protocol`
  :type protocol: dict
  :param label: Protocol label to search
  :type label: string

  :returns: list of sub-protocols with matching label
  :rtype: list[dict]

  :raises ValueError: If no protocol is provided
  :raises ValueError: If the provided protocol is not a dictionary
  :raises KeyError: If the _protocol_set_ key is missing in the provided protocol
  """

  if protocol is None:
    raise ValueError("No Protocol provided")

  if not isinstance(protocol, dict):
    raise ValueError("Provided Protocol needs to be formatted as a dictionary")

  if "_protocol_set_" not in protocol:
    raise KeyError("The selected protocol has no sub-protocols (requires: _protocol_set_)")

  selected_protocols = []
  for sub_protocol in protocol['_protocol_set_']:
      if ('label' in sub_protocol) and (sub_protocol['label'] == label):
          selected_protocols.append(sub_protocol)
  return selected_protocols

def get_subprotocol_by_index( protocol=None, index=0 ):
  """
  Returns a list of sub_protocols in a protocol with given label value
  label is the desired label. If the protocol does not have labels, will be ignored.
  protocol is the protocol to be seaerched.

  :param project_json: project information file
  :param subidx: index of the selected sub-protocol
  :param index: protocol position in the list of protocols (default: 0)

  :returns: single sub-protocol as a dictionary
  :rtype: dict

  :raises ValueError: If no protocol is provided
  :raises ValueError: If the provided protocol is not a dictionary
  :raises KeyError: If the _protocol_set_ key is missing in the provided protocol
  :raises ValueError: If provided index is not an integer
  :raises IndexError: If provided index is out of range
  """

  if protocol is None:
    raise ValueError("No Protocol provided")

  if not isinstance(protocol, dict):
    raise ValueError("Provided Protocol needs to be formatted as a dictionary")

  if "_protocol_set_" not in protocol:
    raise KeyError("The selected protocol has no sub-protocols (requires: _protocol_set_)")

  if not isinstance(index, int):
    raise ValueError("Provided index needs to be an integer")

  if index not in range(0,len(protocol["_protocol_set_"])):
    raise IndexError("Provided Index for sub-protocol %s out of range" % index)

  return protocol["_protocol_set_"][index]
