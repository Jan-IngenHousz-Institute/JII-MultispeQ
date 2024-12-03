"""
Support on working with local measurement files.
"""

import json
import os
import datetime
import warnings

from tabulate import tabulate
import pandas as pd

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

        if isinstance(data, list) and len(data) > 1:
          if 'created_at' in data[0]:
            date_str = datetime.datetime.fromisoformat(data[0]['created_at']).strftime('%Y-%m-%d %H:%M')
          if 'name' in data[0]:
            name_str = data[0]['name']
          if 'notes' in data[0]:
            notes_str = data[0]['notes']

        tbl_content.append([
          file,
          date_str,
          name_str,
          notes_str
        ])

    if len(tbl_content) > 0:

      print( "\n├─ %s (%s)\n" % (root, len(tbl_content) ) )
      table = tabulate( tbl_content, headers=['File', 'Date', 'Name', 'Notes'] )
      print( table )


def load_files ( directory=None, recursive=False ):
  """
  Load files from selected directories into a dictionary.

  :param directory: Measurements in one or multiple directories
  :type directory: str or list[str]

  :return: Dictionary with Measurements
  :rtype: list[dict]

  :raise ValueError: if directory is not provided with a sting or list
  :raise ValueError: if recursive is not True or False
  """

  if directory is None:
    warnings.warn("No directroy selected")
    return []

  if not isinstance(directory, (str, list)):
    raise ValueError("Directory needs to be provided as a string or list")

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
        if os.path.isfile(file) and file.lower().endswith('.json'):
          files_all.append( file )

  # Remove duplicates that may occure when recursive is used with multiple directories
  files_all = list(set(files_all)) 

  # Now gather data from all files to return one list[dict]
  data = []
  for file_path in files_all:
    try:
      with open( file_path, 'r', encoding='utf-8') as fp:
        data += json.load( fp )
    except json.JSONDecodeError:
      warnings.warn('Error: Invalid JSON (%s)' % file_path )
      continue
  
  return data


def load_files_df ( directory=None, recursive=False ):
  """
  Load files from selected directories into a dataframe.

  :param directory: Measurements in one or multiple directories
  :type directory: str or list[str]

  :return: Dataframe with Measurements
  :rtype: pandas.DataFrame
  """

  data = load_files ( directory, recursive )
  
  ## Now the data needs to be transformed to be added to the dataframe
  print(data)

  df = pd.DataFrame()

  return df