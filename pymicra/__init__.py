"""
Pymicra - Python tool for Micrometeorological Analyses
------------------------------------------------------

 :Author: Tomas Chor
 :Date of start: 2015-08-15

"""
import os

vfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'version')
__version__ = open(vfile, 'rt').read().strip()

# ---------
# Here we create a "global" unitregistry for pymicra
try:
    from pint.unit import UnitRegistry
    import os

    abspath = os.path.dirname(os.path.abspath(__file__))
    ureg = UnitRegistry()
    ureg.load_definitions(os.path.join(abspath, 'pymicra.pint'))
    Q_ = ureg.Quantity
except ImportError:
    print('No pint installed yet. Install pint!')
# ---------
from . import decorators

from .io import *
from .util import *
from .micro import *
from .signal import *
from .core import *

from . import io
from . import physics
from . import util
from . import constants
from .micro import spectral
from . import micro
from . import algs
from . import methods

notation = Notation()

# ---------
# Some quick pandas display configurations
import pandas as _pd

_pd.options.display.max_rows = 26
_pd.options.display.width = 160
