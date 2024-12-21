"""
Load measurements from local files to
list of dictionaries or into a pandas
dataframe.
"""

import jii_multispeq.measurement as _measurement

def fn( _data ):
  ## Data Processing here
  return _data

## View Files in Directories
_measurement.list_files('./local')

## Load Files Into a List
data = _measurement.load_files('./local')

## Load Files Into a List Using Recursive Search
data = _measurement.load_files('./local', True)

## Load Files Into a Dataframe
df = _measurement.load_files_df('./local')

## Load Files and Apply Function on File Content
data = _measurement.load_files('./local', fn=fn)
