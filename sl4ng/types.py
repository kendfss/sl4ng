__all__ = 'generator module function DDict defaultdict'.split()

from collections import defaultdict
from typing import Tuple
from warnings import warn
import os

from .iteration import unique, flat

# from .persistance import save, load
from .debug import tipo

generator = type(i for i in range(0))
module = type(os)
function = type(lambda x: x)


class DDict(defaultdict):
    """
    the standard collections.defaultdict with a less obscure __repr__ method
    """

    @property
    def __rack(self):
        pairs = (': '.join(map(repr, pair)) for pair in self.items())
        r = ',\n   '.join(pairs)
        return '{\n   ' + r + '\n}'

    def __repr__(self):
        return tipo(self) + self.__rack

    def __str__(self):
        return ' '.join(self.__rack.split())


defaultdict = DDict
