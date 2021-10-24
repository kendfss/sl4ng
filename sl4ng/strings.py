from typing import Iterable, Any, Generator, Callable, Iterator
from itertools import chain
import string, random

import pyperclip

from .iteration import regenerator

# from .types import function
from .debug import tipo


def join(
    iterable: Iterable[Any] = None, sep: str = '', head: str = '', tail: str = ''
) -> str:
    """
    Cast elements of an array to string and concatenate them.
    This will consume a Generator
    Examples:
        >>> m3ta.show(
                map(
                    join,
                    (range(i) for i in range(1,5))
                )
            )
        0
        01
        012
        0123

        # Also works as a closure using keyword arguments
        >>> m3ta.show(
            map(
                join(sep=', ',head='[',tail=']'),
                (range(i) for i in range(1,5))
            )
        )
        [0]
        [0, 1]
        [0, 1, 2]
        [0, 1, 2, 3]
    """
    if not isinstance(iterable, type(None)):
        return head + sep.join(map(str, iterable)) + tail
    else:

        def wrapper(iterable: Iterable[Any]):
            iterable = map(str, iterable)
            return head + sep.join(iterable) + tail

        return wrapper


def ascii(omissions: str = 'w', include: bool = False) -> str:
    """
    Return the ascii character base excluding the given omissions:
        "p" ->  ' ' + punctuation
        "u" ->  uppercase
        "l" ->  lowercase
        "d" ->  digits
    Feel free to omit combinations:
        ascii('lup')
            0123456789
    """
    d = {
        "p": " " + string.punctuation,
        "u": string.ascii_uppercase,
        "l": string.ascii_lowercase,
        "d": string.digits,
        "w": string.whitespace,
    }
    return (
        "".join(d[key] for key in d if key in omissions)
        if include
        else "".join(d[key] for key in d if not key in omissions)
    )


asciis = kbd = abc = ascii
alphabet = kbd()


def emptyString(line: str) -> bool:
    """
    Determine if a string is empty ('', ' ','\n','\t') or not
    """
    return any(line == i for i in '* *\n*\t'.split('*'))


def rewrite(
    string: str,
    charmap: dict = {
        'A': 'T',
        'T': 'A',
        'C': 'G',
        'G': 'C',
        'a': 't',
        't': 'a',
        'c': 'g',
        'g': 'c',
    },
    sep: str = '',
) -> str:
    """
    Given a sequence derived from 'ATCG', this function returns the complimentary base pairs of the given dna sequence
    Dependencies: None
        Arguments: permutation from 'ATCG'
    Out: compliment of input
    """
    return sep.join([charmap[string[i]] for i in range(len(string))])


def monoalphabetic(
    message: str, shift: int, alphabet: str = kbd(), space: str = None
) -> str:
    """
    A simple implementation of the monoalphabetic cipher.
    By convention, use a:
        Positive integer shift if you want to encode
        Negative integer if you want to decode
    """
    words = message.split(space)
    for index, word in enumerate(words):
        new = ''
        for letter in word:
            if decode:
                substitute = alphabet[(alphabet.index(letter) - shift) % len(alphabet)]
            else:
                substitute = alphabet[(alphabet.index(letter) + shift) % len(alphabet)]
            new += substitute
        words[index] = new
    if space == None:
        space = ' '
    return space.join(words)


caesar = monoalphabetic


def splitall(splitters: Iterable[str], target: str) -> regenerator:
    """
    >>> [*splitall('-_.', 'author-file_name.ext')] == 'author file name ext'.split()
    True
    """
    splitters = iter(splitters)
    result = target.split(next(splitters))
    for splitter in splitters:
        result = [*chain.from_iterable(i.split(splitter) for i in result)]
    yield from filter(None, result)


class splitter:
    """
    Callable which splits a string by a the elements of an iterable. Ignore any empty strings.
    >>> [*splitter('-_.')('author-file_name.ext')] == 'author file name ext'.split()
    True
    """

    def __init__(self, splitters: Iterable[str]):
        self.splitters = regenerator(splitters)

    def __call__(self, argument) -> regenerator:
        return splitall(self.splitters, argument)

    def __repr__(self):
        return f"{tipo(self)}{tuple(self.splitters)}"


def multisplit(splitters: Iterable[str], target: str = None) -> (Callable, regenerator):
    """
    Wrapper on sl4ng.strings.splitall and sl4ng.strings.splitter
    """
    return (
        splitall(splitters, target)
        if not isinstance(target, type(None))
        else splitter(splitters)
    )


def memespace(
    string: str, spaces: int = 1, keep_spaces: bool = False, copy: bool = False
):
    """
    Aestheicize a string
    eg:
        >>> memespace('so edgy')
        s o e d g y
        >>> memespace('so edgy', 2)
        s  o  e  d  g  y
        >>> memespace('so edgy', 2, True)
        s  o     e  d  g  y
    """
    string = string if keep_spaces else join(string.split())
    out = ''
    for i, j in enumerate(string, 1):
        out += j
        out += ' ' * spaces if i < len(string) else ''
    pyperclip.copy(out) if copy else None
    return out


def memecase(string, copy: bool = False):
    """
    Randomize the case of text in strings
    >>> memecase('something about narwhals, bacon, and midnight')
    sOmeTHINg aBOuT nArwHaLS, BAcoN, aND mIDNighT
    """
    out = ''
    for i in string:
        out += random.choice([i.upper(), i.lower()])
    pyperclip.copy(out) if copy else None
    return out


def sinusize(string: str, copy: bool = False):
    """
    Map the characters of a string to critical and solvent points of a sinusoid
    eg
        >>> sinusize('hello_world')
         e   _   l
        h l o w r d
           l   o
    """
    mat = [[] for i in range(3)]
    for i, j in enumerate(string):
        if not i % 2:
            mat[0].append(' ')
            mat[1].append(j)
            mat[2].append(' ')
        elif not (i % 4) - 1:
            mat[0].append(j)
            mat[1].append(' ')
            mat[2].append(' ')
        else:
            mat[0].append(' ')
            mat[1].append(' ')
            mat[2].append(j)
    out = join([join(line) for line in mat], '\n')
    pyperclip.copy(out) if copy else None
    return out


def clean_url(url, root=True, protocol='http'):
    """
    Remove trailing/leading slashes from a url
    params
        root
            if the url starts at the domain level
        protocol
            ignored if root=False
            what protocol should be added to the start of a url
    """
    out = '/'.join(filter(None, url.split('/')))
    if root:
        if ':/' in out:
            out = out.replace(':/', '://')
        else:
            out = '://'.join((protocol, out))
    return out
