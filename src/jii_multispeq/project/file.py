"""
Functions to help working with local project data and information files.
"""

import json
import pandas as pd
import os
import warnings

def file_df_name (projectId):
  """
  Generate the default file name for project data file.

  :param projectId: The project's ID as found on PhotosynQ. If not provided, an Exception will be raised.
  :type projectId: int or str
  
  :return: The default file name for the project data frame.
  :rtype: str

  :raises ValueError: If no project ID is provided.
  """

  if projectId is None:
    raise ValueError("No Project ID provided to generate a filename")

  return str("PhotosynQ_" + str(projectId) + ".pickle")


def file_info_name (projectId):
  """
  Generate the default file name for project info file.
  
  :param projectId: The project's ID as found on PhotosynQ. If not provided, an Exception will be raised.
  :type projectId: int or str
  
  :return: The default file name for the project information.
  :rtype: str

  :raises ValueError: If no project ID is provided.
  """

  if projectId is None:
    raise ValueError("No Project ID provided to generate a filename")

  return str("PhotosynQ_" + str(projectId) + ".json")


def file_exists ( filename="", directory='.'):
  """
  Check if local file exists.

  :param filename: The filename of the file. Defaults to an empty string.
  :type filename: str
  :param directory: The file location. Defaults to the current directory (".").
  :type directory: str
  
  :return: True if the file exists, False otherwise.
  :rtype: bool

  :raises ValueError: If filename or directory are not strings.
  """

  if not isinstance(filename, str):
    raise ValueError("Provided filename needs to be a string")

  if not isinstance(directory, str):
    raise ValueError("Provided directory needs to be a string")

  return os.path.isfile( os.path.join( directory, filename ) )


def save (projectId, directory='.', df=None, info=None):
  """
  Save project data and information to local files.
  For the data a file named like ``PhotosynQ_xxx.pickle`` will be saved. The content is compressed using
  the ``zip`` algorithm.
  For the project information a file in the ``JSON`` format is saved.

  :param projectId: The project's ID as found on PhotosynQ. If not provided, an Exception will be raised.
  :type projectId: int or str
  :param directory: The file location. Defaults to the current directory (".").
  :type directory: str
  :param df: List of dataframes as returned by :func:`~jii_multispeq.project.get`
  :type df: list[dataframe]
  :param info: Project information as returned by :func:`~jii_multispeq.project.get`
  :type info: dict
  
  :returns: None
  :rtype: NoneType

  :raises ValueError: If no project ID is provided.
  :raises ValueError: If directory is not a string.
  """

  if projectId is None:
    raise ValueError("No Project ID provided to generate a filename")
  
  if not isinstance(directory, str):
    raise ValueError("Provided directory needs to be a string")

  if df is not None:
    file = os.path.join( directory, file_df_name(projectId) )
    pd.to_pickle( df, file, compression='zip' )

  if info is not None:
    file = os.path.join( directory, file_info_name(projectId) )
    with open(file, 'w', encoding='utf-8') as f:
      json.dump(info, f, ensure_ascii=False, indent=2)


def load (projectId, directory='.'):
  """
    Load a project's data and information based on the project's ID from the local drive.

    :param project_id: The project's ID as found on PhotosynQ. If not provided, a ValueError will be raised.
    :type project_id: int or str
    :param directory: The file location. Defaults to the current directory (".").
    :type directory: str
    
    :returns: A list of DataFrames representing the project's data and the project's information. Each will be set to None if the corresponding file is not found.
    :rtype: list[pandas.DataFrame], dict
  """

  # Generate file name for data frame(s)
  df_file = file_df_name(projectId)
  
  # Generate file name for project file
  project_file = file_info_name(projectId)

  # Check if data file exists
  if not file_exists(df_file, directory):
    warnings.warn("Project Data File not found (PhotosynQ_xxx.pickle)")
    df = None

  # Load data frames
  else:
    df = pd.read_pickle( os.path.join(directory,df_file), compression='zip' )

  # Check if project file exists
  if not file_exists(project_file, directory):
    warnings.warn("Project Information File not found (PhotosynQ_xxx.json)")
    info = None
  
  # Load project information
  else:
    with open( os.path.join(directory,project_file), 'r') as file:
      info = json.load(file)

  return df, info
