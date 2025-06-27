"""
Taking measurements using a MultispeQ connected via Serial port and
analyze the data from the instrument.

Also functions are provided to load data from locally saved measurements
as well as from notebooks saved by the PhotosynQ Desktop Application
(limited support).
"""

from jii_multispeq.measurement.measure import measure, analyze, view, to_df
from jii_multispeq.measurement.checksum import get_crc32, strip_crc32
from jii_multispeq.measurement.file import list_files, load_files, load_files_df
from jii_multispeq.measurement.notebook import import_notebook