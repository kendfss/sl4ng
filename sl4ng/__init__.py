from typing import Iterable, Any, Iterator, Sequence
import os

from .debug import *
from .iteration import *
from .maths import *
from .stats import *
from .strings import *
from .system import *
from .web import *
from .magnitudes import *


HERE, THIS = os.path.split(__file__)

if sys.platform == "darwin":
    def __startfile(args: str) -> None:
        os.popen(f"open {arg}")
    os.startfile = __startfile

if __name__ == "__main__":
    pass
