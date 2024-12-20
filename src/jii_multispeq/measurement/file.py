"""
Support on working with local measurement files.
"""

import json
import os
import datetime
import warnings

from tabulate import tabulate
import pandas as pd

from jii_multispeq.measurement import analyze as _analyze 

def list_files ( directory='./local/' ):
  """
  List all local files in the provided directory

  :param directory: Directory
  :type directory: str

  :return: None
  :rtype: None
  """

  if not os.path.exists ( directory ):
    raise ValueError("Selected directory does not exist.")

  tbl_content = []

  for root, _, files in os.walk( directory ):
    tbl_content = []
    for file in files:
      if file.lower().endswith('.json'):

        file_path = os.path.join(root, file)

        try:
          with open( file_path, 'r', encoding='utf-8') as fp:
            data = json.load( fp )
        except json.JSONDecodeError:
          warnings.warn('Error: Invalid JSON (%s)' % file_path )
          continue

        ctime = os.path.getctime(file_path)
        date_str = datetime.datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M')
        name_str = 'n/a'
        notes_str = 'n/a'
        type_str = 'single'

        if isinstance(data, list) and len(data) > 1:
          type_str = "multi (%s)" % len(data)

        if isinstance(data, dict):
          if 'created_at' in data:
            date_str = datetime.datetime.fromisoformat(data['created_at']).strftime('%Y-%m-%d %H:%M')
          if 'name' in data:
            name_str = data['name']
          if 'notes' in data:
            notes_str = "n/a" if data['notes'] == "" else data['notes']

        tbl_content.append([
          file,
          date_str,
          type_str,
          name_str,
          notes_str
        ])

    if len(tbl_content) > 0:

      print( "\n├─ %s (%s)\n" % (root, len(tbl_content) ) )
      table = tabulate( tbl_content, headers=['File', 'Date', 'Type', 'Name', 'Notes'] )
      print( table )


def load_files ( directory=None, recursive=False, fn=None ):
  """
  Load files from selected directories into a dictionary.

  :param directory: Measurements in one or multiple directories
  :type directory: str or list[str]
  :param recursive: Recursive listing of files and subdirectories
  :type recursive: bool
  :param fn: Function to analyze the provided data
  :type fn: function

  :return: Dictionary with Measurements
  :rtype: list[dict]

  :raise ValueError: if directory is not provided with a sting or list
  :raise ValueError: if recursive is not True or False
  :raise ValueError: if no valid function is provided
  """

  if directory is None:
    warnings.warn("No directroy selected")
    return []

  if not isinstance(directory, (str, list)):
    raise ValueError("Directory needs to be provided as a string or list")

  if (not fn is None) & (not hasattr( fn, '__call__')):
    raise Exception("No function is provided")

  if isinstance(directory, str):
    directory = [directory]

  files_all = []

  for dir in directory:

    if not os.path.exists(dir):
      warnings.warn("Directory %s does not exist" % dir)
      continue

    # If recursive directory selection is used
    if recursive:
      for root, _, files in os.walk( dir ):
        for file in files:
          if file.lower().endswith('.json'):
            files_all.append( os.path.join(root, file) )
    else:
      for file in os.listdir( dir ):
        filepath = os.path.join(dir, file)
        if os.path.isfile(filepath) and filepath.lower().endswith('.json'):
          files_all.append( filepath )
  
  # Remove duplicates that may occure when recursive is used with multiple directories
  files_all = list(set(files_all)) 

  # Now gather data from all files to return one list[dict]
  data = []
  for file_path in files_all:
    try:
      with open( file_path, 'r', encoding='utf-8') as fp:
        data.append( json.load( fp ) )
    except json.JSONDecodeError:
      warnings.warn('Error: Invalid JSON (%s)' % file_path )
      continue
  
  ## Run function on every element
  if (not fn is None) & (hasattr( fn, '__call__')):
    data[:] = [_analyze(itm, fn) for itm in data]

  return data


def load_files_df ( directory=None, recursive=False, fn=None ):
  """
  Load files from selected directories into a dataframe.

  :param directory: Measurements in one or multiple directories
  :type directory: str or list[str]
  :param recursive: Recursive listing of files and subdirectories
  :type recursive: bool
  :param fn: Function to analyze the provided data
  :type fn: function

  :return: Dataframe with Measurements
  :rtype: pandas.DataFrame
  """

  ## Load all files and apply function if selected
  data = load_files ( directory, recursive, fn )
  
  ## Now the data can be added to the dataframe
  df = pd.DataFrame(data)

  return df