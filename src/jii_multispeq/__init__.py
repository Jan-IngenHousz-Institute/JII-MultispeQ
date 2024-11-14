"""
JII MultispeQ package initialization
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("jii_multispeq")
except PackageNotFoundError:
    # package is not installed
    pass

# Make sure to expose __version__ at package level
__all__ = ['__version__']

from jii_multispeq.about import version

import jii_multispeq.project
import jii_multispeq.protocol
