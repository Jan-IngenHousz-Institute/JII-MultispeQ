"""
Import PhotosynQ Notebooks into a dataframe.
"""

import os
import warnings
import json

import photosynq_py as ps

def import_notebook ( source=None ):
  """
  Import one or multiple Notebook files exported from the
  PhotosynQ, Inc. Desktop Application's notebook.

  .. warning::
    The values calculated by Macros in the PhotosynQ, Inc. Desktop Application are not available when 
    imported using this package. Notebook files can be exported according to the 
    `PhotosynQ, Inc. Documentation <https://help.photosynq.com/desktop-application/notebook.html>`_.
    This package only provides limited support of the Notebook format.

  :param source: Notebook file(s)
  :type source: str or list[str]

  :return: Dataframe or None
  :rtype: pandas.Dataframe

  :raises ValueError: if no source file is provided
  """

  if source is None:
    raise ValueError("No source file provided")
  
  if isinstance( source, str ):
    if os.path.exists( source ):
      return ps.build_notebook_dataframe( source )
    else:
      raise Exception("Provided source does not exist")
    
  if isinstance( source, list ):
    data = []
    for file in source:
      if os.path.exists( file ):
        try:
          with open( file, 'r', encoding='utf-8') as fp:
            data += json.load( fp )
        except json.JSONDecodeError:
          warnings.warn('Error: Invalid JSON (%s)' % file )
          continue
      else:
        warnings.warn("Provided source does not exists. Continuing with remaining files")

    # Write everything to a single file
    with open( '__tmp__.json', 'w', encoding='utf-8' ) as fp:
      json.dump(data, fp,  indent=2)

    # Now do the import and delete the temporary file afterwards
    df = ps.build_notebook_dataframe( '__tmp__.json' )
    os.remove( '__tmp__.json' )

    return df

  return None