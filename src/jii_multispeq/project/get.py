"""
Extension of the PhotosynQ Python Library to download project data and information
as well as save a local copy for subsequent faster data loading and offline work.
"""

import photosynq_py as ps
from jii_multispeq.project.file import load, save 

def get ( email=None, projectId=None, directory='.', processed_data=True, raw_traces=False, force=False):
  """
  Get the data for a Project based on it's ID. In case data and info files exist locally already, they will be used for loading the data.
  Otherwise, the data will be downloaded from the PhotosynQ platform and files will be saved locally for future use.

  :param email: The email used for the PhotosynQ account. If not provided, a local copy will be loaded, if available.
  :type email: str
  :param project_id: The project's ID as found on PhotosynQ. If not provided, a ValueError will be raised.
  :type project_id: int or str
  :param directory: The file location. Defaults to the current directory (".").
  :type directory: str
  :param processed_data: Including processed data into the requested project data. Defaults to True.
  :type processed_data: bool
  :param raw_traces: Including raw data traces in the requested project data. Defaults to False, as data files could be large.
  :type raw_traces: bool
  :param force: If True a download is forced, overwriting existing files. Defaults to False.
  :type force: bool
  :return: A list of DataFrames representing the project's data and the project's information. Each will be set to None if the corresponding file is not found.
  :rtype: list[pandas.DataFrame], dict
  
  :raises ValueError: If no project ID is provided.
  :raises ValueError: If provided project ID is not an integer.

  :alias: :func:`~jii_multispeq.project.file.download`
  """

  if projectId is None:
    raise ValueError("No Project ID provided")
  
  if isinstance(projectId, str) and not projectId.isdigit():
    raise ValueError("Project ID provided needs to be an integer (can be provided as a string)")

  df, info = load( projectId, directory )

  # Logic in case files are found
  if (( df and info ) is not None) and not force:
    print("Project Data and information found.")
    return df, info

  # Logic in case files are not found
  else:
    print("Project Data and information not found.")

    if email is None:
      raise Exception("No email provided")

    # use your photosynq account to login (you will be prompted for your password)
    ps.login(email)

    # retrieve a dataframe with data from the given project ID
    info = ps.get_project_info(projectId)
    data = ps.get_project_data(projectId, processed_data, raw_traces) # Use raw data
    df = ps.build_project_dataframe(info, data)

    # logout
    ps.logout()

    # save dataframe as pickle file for future use
    save (projectId, directory, df, info)

  return df, info