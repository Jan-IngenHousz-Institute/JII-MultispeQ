"""
Download Project Data from PhotosynQ

A local copy of the data frames and the Project Information
gets saved in the same directory as the file executed by default.
"""

import jii_multispeq.project as project
import jii_multispeq.protocol as protocol

email = "your-email@domain.com"
projectId = 29652

## Get the project data and information
df, info = project.get(email, projectId)

## Print the project information
project.print_info(info)

## Get Protocol Name
protocol_name =  protocol.get_protocol_name(info)
print(protocol_name)

## Get Protocol Code
protocol_code = protocol.get_protocol(info)
print(protocol_code)

## Get Protocol's dataframe with its information
data = df[protocol_name]
print(data.info('verbose'))
