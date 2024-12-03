"""
Working with a Protocol 

Accessing the protocol from the Project Information and
it's components which can further assist in the data analysis.
"""

import jii_multispeq.project as project
import jii_multispeq.protocol as protocol

projectId = 29652

## Get the project data and information
df, info = project.get(projectId=projectId)

## Get Protocol Name
protocol_name =  protocol.get_protocol_name(info)
print(protocol_name)

## Get the code for the selected protocol
protocol_code =  protocol.get_protocol(info)
print( protocol_code )

## Get the variable array (v_arrays) from a selected protocol
v_arrays = protocol.get_v_arrays(protocol_code)
print( v_arrays )

## Get all labels from sub-protocols
labels = protocol.get_subprotocol_labels(protocol_code)
print( labels )

## Get sub-protocols by label
by_label = protocol.get_subprotocols_by_label(protocol_code, "PIRK")
print( by_label )

## Get sub-protocols by index
by_index = protocol.get_subprotocol_by_index(protocol_code, 2)
print( by_index )
