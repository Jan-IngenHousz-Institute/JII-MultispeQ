"""
Function to help view project information.
"""

import json
import pprint

def print_info(project=None, show_code=False):
  """
  Print formatted information about the provided Project.

  :param project: Project information as returned by :func:`~jii_multispeq.get.get` or :func:`~jii_multispeq.file.load`.
  :type project: dict
  :param show_code: Display the protocol's code in addition to the description. Defaults to False.
  :type show_code: bool
  
  :return: None
  :rtype: NoneType
  
  :raises ValueError: if no project data is provided or the project data has the wrong format

  :alias: :func:`~jii_multispeq.project.info.show`
  """

  # Required keys
  keys = { 'name', 'id', 'project_url', 'tag_list', 'data_count', 
           'created_at', 'updated_at', 'locations', 'creator', 'description', 
           'directions_to_collaborators', 'filters', 'protocols', 'protocol_json' }

  # Display exeption if no dictionary is provided
  if project is None:
    raise ValueError("Provided Project has no information")
  
  # Check if first level keys are available
  if not keys <= project.keys():
    raise ValueError("Provided Project doesn't seem to have the correct format, missing key")

  # Project Title
  print( "=" * (11 + len(project["name"]) + len( str(project["id"])) ))
  print( "  %s (ID: %s)" % (project["name"], project["id"]))
  print( "=" * (11 + len(project["name"]) + len( str(project["id"])) ))
  
  # Project URL
  print( "\nURL: %s\n" % (project["project_url"]))

  # Tags
  if len(project["tag_list"]) > 0:
    print( "Tag(s): %s\n" % (", ".join(project["tag_list"])))

  # Basic Info
  print( "Basic Info:\n-----------")
  print( "Datasets:    %s" % (project["data_count"]))
  print( "Created:     %s" % (project["created_at"]))
  print( "Last Update: %s" % (project["updated_at"]))

  # Location
  if len(project["locations"]) > 0:
    print( "Locations:")
    for location in project["locations"]:
      print( " - %s (%s, %s)" % (location["address"], location["latitude"], location["longitude"]))

  # Project Creator
  print( "\nProject Creator:\n----------------")
  print( "Name:      %s" % (project["creator"]['name']))
  if project["creator"]['institute'] != '':
    print( "Institute: %s" % (project["creator"]['institute']))
  print( "URL:       %s" % (project["creator"]['profile_url']))  

  # Description
  print( "\nProject Details:\n----------------" )
  if project["description"] is None or (len(project["description"]) <= 80):
      print(project["description"])
  else:
    print( pprint.pformat( project["description"], width=80 )[2:-2].replace("'\n '", "\n") )

  # Directions
  if project["directions_to_collaborators"] is None or (len(project["directions_to_collaborators"]) <= 80):
      print( "Directions: \n%s" % (project["directions_to_collaborators"]))
  else:
    print( "Directions: \n%s" % (pprint.pformat( project["directions_to_collaborators"], width=80 )[2:-2].replace("'\n '", "\n") ) )
  
  # Meta Data
  question_type = ["Multiple Choice", "Multiple Choice (with images)", "Short Answer", "Take picture"]
  if len(project["filters"]) > 0:
    print("\nMeta Data:\n----------")
    for filter in project["filters"]:
      print( " * %s - %s%s" % (filter["label"], question_type[ filter["value_type"] ], (' (Deleted)' if filter["is_deleted"] is True else "" ) ))
      print( "   Unique Inputs: %s" % ( len(filter["value"])) )

  # Protocol
  if len(project["protocols"]) > 0:
    print("\nProtocol(s):\n------------")
    for protocol in project["protocols"]:
      print( " * %s (ID: %s)\n   %s" % (protocol["name"], protocol["id"], 
        protocol["description"] if (protocol["description"] is None) or (len(protocol["description"]) <= 80) else pprint.pformat( protocol["description"], width=80 )[2:-2].replace("'\n '", "\n   ") ))

  # Protocol JSON
  if show_code: 
    print("\nProtocol Code:\n--------------")
    print( pprint.pprint( json.loads(project['protocol_json']), compact=True) )
