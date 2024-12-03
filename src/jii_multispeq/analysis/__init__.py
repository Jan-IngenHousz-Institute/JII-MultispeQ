"""
The provided functions can help to analyze data aquired from a MultispeQ device.

There are two parts to the analysis, the :mod:`~jii_multispeq.analysis.basic`
functions that support the analysis of a single measurment returned from a device
and the rest of the :mod:`~jii_multispeq.analysis` module, that focuses on
functions supporting the multiple measurements which have already been processed.
"""

from jii_multispeq.analysis.basic import GetIndexByLabel, GetLabelLookup, GetProtocolByLabel
from jii_multispeq.analysis.dataframe import make_object_col, add_params_to_info
from jii_multispeq.analysis.pirk import get_pirk_slices_and_intensities
