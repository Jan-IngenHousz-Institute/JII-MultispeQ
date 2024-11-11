"""
JII MultispeQ package initialization
"""

try:
    from jii_multispeq import __version__
except ImportError:
    # Fallback version
    __version__ = "0.0.0"

# Make sure to expose __version__ at package level
__all__ = ['__version__']

from jii_multispeq.about import version

import jii_multispeq.project
import jii_multispeq.protocol
