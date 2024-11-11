"""
The :mod:`~jii_multispeq.project` module helps downloading the data from the PhotosynQ platform, as well
as managing files locally and display information about a locally saved project.

The **Data** related functions are loading the data either from a cloud or local source.
**View Info** functions display the information about the project and the **File Functions**
are helper functions to manage the local files. While they can be used individually they
should not be required to use if functions like :func:`~jii_multispeq.project.get` and
:func:`~jii_multispeq.project.info.print_info` are used.
"""

from jii_multispeq.project.get import get
from jii_multispeq.project.file import file_df_name, file_info_name, file_exists, save, load
from jii_multispeq.project.info import print_info

## Function Alias Names
from jii_multispeq.project.info import print_info as show
from jii_multispeq.project.get import get as download
