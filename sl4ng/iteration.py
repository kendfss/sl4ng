# Statisticals checked against: http://www.alcula.com/calculators/statistics/

from itertools import tee, _tee, islice, chain, combinations
from numbers import Number, Real
from typing import Iterable, Any, Sequence, List, Callable, Generator, Hashable
from math import log
import random, time



class __regen:
    """
    A namespace for utilities used in creating regenerators
    """
    @staticmethod
    def choose(iterable:Iterable[Any], *indices:Sequence[int]) -> Generator:
        """
        Yield specific elements from an iterable by index:
        >>> [*choose(range(1, 10), 0, 3)]
        [1, 4]
        >>> [*choose(range(1, 10), (0, 3))]
        [1, 4]
        
        """
        indices = [*flatten(indices)]
        yielded = []
        for i, e in enumerate(iterable):
            if i in indices:
                yield e
                yielded.append(e)
            if len(yielded) == len(indices):
                break
    @staticmethod
    def tipo(inpt:Any=type(lambda:0), keep_module:bool=False) -> str:
        """
        Return the name of an object's type
        Dependencies: None
        In: object
        Out: str
        """
        if keep_module:
            return str(type(inpt)).split("'")[1]
        return str(type(inpt)).split("'")[1].split('.')[-1]
    @staticmethod
    def flatten(iterable:Iterable) -> Generator:
        """
        Flatten a 2d iterable
        Example:
        >>> list(flatten([[1, 2], [3, 4]]))
                [1, 2, 3, 4]
        based on:
            https://pythonprinciples.com/challenges/Flatten-a-list/
        """
        for i in iterable:
            if hasattr(i, '__iter__') or hasattr(i, '__next__'):
                yield from i
            else:
                yield i

class regenerator:
    """
    A self-replenishing (or non-consumable) iterator. All methods whose return value is iterable return regenerators
    :args & kwargs:
        Any arguments needed to initialize the Generator-type/function. Will not be used unless hasattr(iterable, '__call__') and iterable is not a regenerator.
    eg:
        >>> x = regurge(i for i in range(2))
        >>> [*x]
        [0, 1]
        >>> bytes(x)
        b'\x00\x01'
        >>> [*x]
        [0, 1]
    """
    def __init__(self, iterable, *args, **kwargs):
        if hasattr(iterable, '__call__') and not isinstance(iterable, type(self)):
            self.active, self._inert = tee(iterable(*args, **kwargs))
        else:
            self.active, self._inert = tee(iterable)
    def __next__(self):
        return next(self.active)
    def __iter__(self):
        self.active, self._inert = tee(self._inert)
        return self.active
    def __getitem__(self, index:int):
        if isinstance(index, int):
            index = index if index >= 0 else len(self) + index
            for i, e in enumerate(self):
                if i == index:
                    return e
        else:
            raise
        raise IndexError(f'{__regen.tipo(self)} contains fewer than {index} elements')
    def __call__(self, *indices:Iterable[int]):
        """
        Access particular indices of the underlying iterator
        eg
            >>> x = regen(range(3))
            >>> [*x(1)]
            [1]
            >>> [*x(1,2)]
            [1, 2]
            >>> [*x(1,2,3)]
            [1, 2]
        """
        return type(self)(__regen.choose(self.active, *__regen.flatten(indices)))
    def __bool__(self):
        """
        Returns True iff. the underlying iterator is non-empty. False otherwise.
        """
        tmp, self._inert = tee(self._inert)
        try:
            next(tmp)
            return True
        except StopIteration:
            return False
    def __matmul__(self, other:Iterable):
        if hasattr(other, '__iter__'):
            return type(self)(product(self, other))
        raise TypeError(f'Matrix-multiplication is not defined between {__regen.tipo(self, True)} and "{__regen.tipo(other, True)}"-type. It must have an "__iter__" or "__index__" method.')
    def __len__(self):
        return sum(1 for i in self)
    def __add__(self, other:Iterable):
        """
        Create a new regenerator whose first elements come from self and remaining element(s) is/come-from other.
        If other is not iterable it shall be added as the last element.
        If you want to add an iterable as a single element, use self.append
        eg
            >>> x = regenerator(range(2))
            >>> y = x + 10
            >>> [*y]
            [0, 1, 10]
            >>> y += x
            >>> [*y]
            [0, 1, 10, 0, 1]
        """
        other = other if hasattr(other, '__iter__') else [other]
        return type(self)([*self, *other])
    def __radd__(self, other:Iterable):
        """
        Swap the order of __add__
        """
        other = other if hasattr(other, '__iter__') else [other]
        return type(self)(chain(other, self))
    def __mul__(self, value:int):
        """
        Replicate the behaviour of multiplying lists by integers
        """
        if hasattr(value, '__int__'):
            return type(self)(chain.from_iterable(self for i in range(int(value))))
        raise TypeError(f'Multiplication is not defined for "{__regen.tipo(other, True)}". It must have an "__int__"')
    def __rmul__(self, value:int):
        """Commutative multiplication"""
        return self.__mul__(value)
    def __pow__(self, value:int):
        """
        value-dimensional Cartesian product of self with itself
        """
        if hasattr(value, '__int__'):
            return type(self)(product(self, repeat=int(value)))
        raise TypeError(f'Exponentiation is not defined for {type(other)}. It must have an "__int__" method.')
    
    def count(self, value:Any):
        """
        how many copies of value?
        """
        return sum(1 for i in self if i==value)
    def scale(self, value:Any):
        """
        Multiply every element of self by value. Done in place.
        """
        self._inert = (i*value for i in self)
        return self
    def boost(self, value:Any):
        """
        Add value to every element of self. Done in place.
        """
        self._inert = (i+value for i in self)
        return self
    def indices(self, value:Any, shift:int=0):
        """
        Similar to a list's index method, except that it returns every index whose element is a match
        Works by calling enumerate and selecting at equivalent elements.
        :shift:
            kwarg for the "enumerate" call.
        """
        return type(self)(i for i, e in enumerate(self, shift) if e == value)
    def append(self, value:Any):
        """
        add "value" as the last element of the array
        """
        other = [value]
        self._inert = chain(self._inert, other)
        return self
    def inject(self, value:Any):
        """
        If "value" is an iterable: its elements will be added to the end of "self"
        Otherwise: it is the same as append
        """
        other = value if hasattr(value, '__iter__') else [value]
        self._inert = chain(self._inert, *other)
        return self
regen = regenerator


def xrange(stop:Number, start:Number=0, step:Number=1, reverse:bool=False) -> Generator:
    """
    xrange(start, stop, step)
    An implementation of the old xrange Generator
    examples:
        >>> [*xrange(2)]
        [0, 1]
        >>> [*xrange(2, 1)]
        [1]
        >>> [*xrange(2, 1, 0.5)]
        [1, 1.5]
        >>> [*xrange(2, 1, 0.5, reverse=True)] # 
        [1.5, 1.0]
        >>> [*xrange(10, 1, 1, True)]
        [9, 8, 7, 6, 5, 4, 3, 2, 1]
    
    todo:
        add the ability to use single-argument negative stops?
    """
    if reverse:
        while start<stop:
            yield stop - step
            stop -= step
    else:
        while start<stop:    
            yield start
            start += step


def tight(iterable:Iterable[Any], yielded:list=None) -> Generator:
    """
    Produce a new iterator of unique elements from a given array
    will consume a Generator
    """
    yielded = yielded if not isinstance(yielded, type(None)) else []
    for i in iterable:
        if not i in yielded:
            yield i
            yielded.append(i)
unique = tight


def walks(iterable:Iterable[Any], length:int=2) -> Generator:
    """
    Break an iterable into len(iterable)-length steps of the given length, with each step's starting point one after its predecessor
    example
        >>> for i in walks(itertools.count(),2):print(''.join(i))
        (0, 1)
        (1, 2)
        (2, 3)
        # etc.
    Inspired by the hyperoperation 16**2[5]2
    Extended to generators with cues from more_itertools' "stagger"
    Extended to infinite generators by pedantry
    """
    consumable = regenerator(iterable)
    t = tee(consumable, length)
    yield from zip(*(it if n==0 else islice(it, n, None) for n, it in enumerate(t)))


def flatten(iterable:Iterable) -> Generator:
    """
    Transform an N-dimensional array into a N-1-dimensional array.
    Example:
    >>> list(flatten([[1, 2], [3, 4]]))
            [1, 2, 3, 4]
    based on:
        https://pythonprinciples.com/challenges/Flatten-a-list/
    """
    for i in iterable:
        if hasattr(i, '__iter__') or hasattr(i, '__next__'):
            for j in i:
                yield j
        else:
            yield i


def flat(iterable:Iterable, dict_keys:bool=False, strings:bool=False) -> Generator:
    """
    Create a completely flat version of an iterable.
    params:
        strings
            yield each character from each string if set to True
        dict_keys
            yield the keys instead of the values if set to True
    """
    # if isinstance(iterable, fo;):
        # yield iterable
    if isinstance(iterable, str):
        yield from iterable if strings else [iterable]
    elif isinstance(iterable, dict):
        itr = iterable.keys() if dict_keys else iterable.values()
        for val in itr:
            yield from flat(val, dict_keys, strings)
    elif isinstance(iterable, (list, tuple, map, filter)):
        for val in iterable:
           if hasattr(val, '__iter__'):
               yield from flat(val, dict_keys, strings)
           else:
               yield val
    elif hasattr(iterable, '__iter__'):
        yield from iterable
    else:
         yield iterable



def nopes(iterable:Iterable[Any], yeps:bool=False) -> Generator:
    """
    if yeps==False
        Return the indices of all false-like boolean values of an iterable
    Return indices of all true-like boolean values of an iterable

    example
        >>> t = (0, 1, 0, 0, 1)
        >>> tuple(nopes(t))
        (0, 2, 3)
        >>> tuple(nopes(t, True))
        (1, 4)
    """
    for i, j in enumerate(iterable):
        if (not j, j)[yeps]:
            yield i


def roll(iterable:Iterable, stop:int, start:int=0, step:int=1) -> tuple:
    """
    Return 'stop' elements from an effective cycle of the iterable, using only those whose modulus is greater than 'start'
    
    Example:
        >>> roll('boris', 5)
        ('b', 'o', 'r', 'i', 's')
        >>> roll('boris', 6)
        ('b', 'o', 'r', 'i', 's', 'b')
        >>> roll('boris', 6, 1)
        ('o', 'r', 'i', 's', 'b', 'o')
        >>> roll('boris', 6, 1, 2)
        ('r', 's', 'o')
    """
    consumable = regenerator(iterable)
    return tuple(consumable[(i + 0) % len(consumable)] for i in range(0, stop + start, step) if i >= start)


def deduplicate(unhashable:Iterable) -> dict:
    """
    Because dictionaries seem to be less hashable than lists, which are also formally unhashable
    This will consume a Generator
    """
    if isinstance(unhashable, dict):
        trimmed = {}
        for key, val in unhashable.items(): 
            if val not in trimmed.values():
                trimmed[key] = val 
        return trimmed           
    else: 
        raise TypeError(f'Protocol for your {tipo(unhashable)} is pending')


def band(iterable:Iterable[Real]) -> Real:
    """
    Returns the extrema of the given iterable
    """
    consumable = regenerator(iterable)
    return min(consumable), max(consumable)


def bandgap(iterable:Iterable[Real]) -> Real:
    """
    Returns the breadth of a given iterable of elements overwhich subtraction, max, and min, are well defined
    """
    consumable = regenerator(iterable)
    return max(consumable) - min(consumable)


def lispart(lis:Iterable, depth:int) -> list:
    """
    Returns a collection of n*m elements as a list of m lists with n elements each
    devised by David C. Ullrich from stack exchange
    """
    consumable = regenerator(consumable)
    assert(len(consumable)%depth == 0), f'The iterable cannot be factored into "{depth}" arrays'
    return [consumable[j*depth:(j+1)*depth] for j in range(int(len(consumable)/depth))]


def cast(x:int, y:int, iterable:Iterable=None) -> list:
    """
    Return a YxX matrix (y lists of length x) whose elements are from slices of the iterable
    """
    base = regenerator(iterable) if iterable else tuple(range(x * y))
    assert x*y==len(list(tee(base)[0])), f"Iterable does not cast to (x, y) = {(x, y)}"
    # return [base[slice(i*x, x+i*x)] for i in range(y)]
    return [base[i * x: x + i * x] for i in range(y)]

def sigma(iterable:Iterable[Any], v0:Any=0) -> Any:
    """
    Returns the sum of a iterable
    """
    for i in iterable:
        v0 += i
    return v0


def pipe(iterable:Iterable[Number]) -> Number:
    """
    Returns the multiplicative product of the elements of a collection
    """
    consumable = regenerator(iterable)
    if len(consumable) < 1:
        return "this list is empty"
    else:
        v0 = 1
        for i in consumable:
            v0 *= i
        return v0


def powerset(iterable:Iterable[Any]) -> regenerator:
    """
    Returns the powerset of an iterable as a list
    """
    consumable = regenerator(iterable)
    return regenerator(chain.from_iterable(combinations(consumable, r) for r in range(sum(1 for i in consumable)+1)))
    
    
def sample(iterable:Iterable[Any], size:int) -> tuple:
    """
    Obtains a random sample of any length from any iterable and returns it as a tuple
    Unlike random.sample, this may yield the same element several times.
    """
    consumable = regenerator(iterable)
    choiceIndices = tuple(random.randint(0, len(consumable)-1) for i in range(size))
    return tuple(consumable[i] for i in choiceIndices)


def shuffle(iterable:Iterable[Any]) -> tuple:
    """
    Given an iterable, this function returns a new tuple of its elements in a new order
    """
    consumable = regenerator(iterable)
    cache = []
    pot = []
    while len(cache) < len(consumable):
        v0 = random.randrange(len(consumable))
        if v0 not in cache:
            cache.append(v0)
            pot.append(consumable[v0])
    return tuple(pot)
randomizer = shuffler = shuffle


def unzip(iterable:Iterable[Sequence[Any]]) -> List[list]:
    """
    Obtain the inverse of a zip of a collection of arrays
    This is about the same as a clockwise rotation of a matrix by 90 degrees
    This will omit empty arrays
    examples
        >>> sl4ng.show(unzip(range(3) for i in range(3)))
        [0, 0, 0]
        [1, 1, 1]
        [2, 2, 2]
        
        
        >>> sl4ng.show(unzip(range(j) for j in range(10)))
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        [1, 1, 1, 1, 1, 1, 1, 1]
        [2, 2, 2, 2, 2, 2, 2]
        [3, 3, 3, 3, 3, 3]
        [4, 4, 4, 4, 4]
        [5, 5, 5, 5]
        [6, 6, 6]
        [7, 7]
        [8]
        
        
    """
    consumable = regenerator(iterable)
    str_escape = lambda string: string.replace("'", "\'").replace("\\", "\\\\")
    length = 0
    racks = []
    for i in consumable:
        for j, k in enumerate(i):
            if j > length-1:
                exec(f"x{j} = []")
                racks.append(eval(f'x{j}'))
                length += 1
            app_elem = f"""x{j}.append('{(k, str_escape(k))[isinstance(k, str)]}')"""
            eval(app_elem)
    return racks

def diffs(iterable:Iterable[Number], flip:bool=False) -> Generator:
    """
    Yield the difference between each element of an iterable and its predecessor
    example:
        >>> [*diffs(range(3))]
        [1, 1]
        >>> [*diffs(range(3), True)]
        [-1, -1]
    """
    consumable = iter(iterable)
    last = next(consumable)
    for i in consumable:
        yield i - last if not flip else last - i
        last = i

def discontinuities(iterable:Iterable[Number], delta:Number=1) -> Generator:
    """
    Obtain the ordinal positions of any elements who do not differ from their successors by delta
    Iterable must, at least, be a semigroupoid with subtraction
    Not Generator safe.
    example:
        >>> [*discontinuities(range(3))]
        []
        >>> [*discontinuities(range(3), 2)]
        [0, 1]
    """
    iterable = iter(iterable)
    last = next(iterable)
    for i, e in enumerate(iterable):
        if e - last != delta:
            yield i
        last = e

def stationaries(iterable:Iterable[Number]) -> Generator:
    """
    Generate the indices of the stationary points of an iterable
    example:
        >>> [*stationaries(range(3))]
        []
        >>> [*stationaries((3, 4, 4, 3, 2, 1, 1), 2)]
        [1, 5]
    """
    iterable = iter(iterable)
    last = next(iterable)
    for i, e in enumerate(iterable):
        if e == last:
            yield i
            last = e

def discontinuous(iterable:Iterable[Number], differential:Number=1) -> Generator:
    """
    Check if an additive semigroupoid has any jumps which are inequivalent to a given differential
    example:
        >>> [*discontinuous(range(3))]
        False
        >>> [*discontinuous(range(3), 2)]
        True
    """
    if differential:
        last = None
        for i, e in enumerate(iterable):
            if i > 0:
                if not eq(last + differential, e):
                    return False
            last = e
        return True
    return eq(*iterable)



def sums(iterable:Iterable[Number], flip:bool=False) -> Generator:
    """
    Yield the sum of each element of an iterable and its predecessor
    example:
        >>> [*sums('abc')]
        ['ba', 'cb']
        >>> [*sums('abc', True)]
        ['ab', 'bc']
    """
    consumable = iter(iterable)
    last = next(consumable)
    for i in consumable:
        yield i + last if not flip else last + i
        last = i

def quots(iterable:Iterable[Number], flip:bool=False) -> Generator:
    """
    Yield the quotient of each element of an iterable by its predecessor
    example:
        >>> [*quots(range(1, 4))]
        [2.0, 1.5]
        >>> [*quots(range(1, 4), True)]
        [0.5, 0.6666666666666666]   
    """
    consumable = iter(iterable)
    last = next(consumable)
    for i in consumable:
        yield i / last if not flip else last / i
        last = i

def prods(iterable:Iterable[Number], flip:bool=False) -> Generator:
    """
    Yield the product of each element of an iterable by its predecessor
    example:
        >>> [*prods(range(1, 4))]
        [2, 6]
        >>> [*prods(range(1, 4), True)]
        [2, 6]
    """
    consumable = iter(iterable)
    last = next(consumable)
    for i in consumable:
        yield i * last if not flip else last * i
        last = i

def logs(iterable:Iterable[Number], flip:bool=False) -> Generator:
    """
    Yield the log of each element of an iterable in the base of its predecessor
    example:
        >>> [*logs(range(2, 5))]
        [1.5849625007211563, 1.2618595071429148]
        >>> [*logs(range(2, 5), True)]
        [0.6309297535714574, 0.7924812503605781]
    """
    consumable = iter(iterable)
    last = next(consumable)
    for i in consumable:
        yield log(i, last) if not flip else log(last, i)
        last = i

def cumsum(iterable:Iterable[Number], first:bool=True) -> Generator:
    """
    Yield the log of each element of an iterable in the base of its predecessor
    example:
        >>> [*cumsum(range(4))]
        [0, 1, 3, 6]
        >>> [*cumsum(range(4), False)]
        [1, 3, 6]
    """
    consumable = iter(iterable)
    last = 0
    if first:
        yield last
    for i in consumable:
        last += i
        yield last

def cumdif(iterable:Iterable[Number], first:bool=True) -> Generator:
    """
    Yield the log of each element of an iterable in the base of its predecessor
    example:
        >>> [*cumdif(range(4))]
        [0, -1, -3, -6]
        >>> [*cumdif(range(4), False)]
        [-1, -3, -6]
    """
    consumable = iter(iterable)
    last = next(consumable)
    if first:
        yield last
    for i in consumable:
        last -= i
        yield last

def cumprod(iterable:Iterable[Number], first:bool=True) -> Generator:
    """
    Yield the cumulative product of the elemements of an iterable
    example:
        >>> [*cumprod(range(1, 4))]
        [1, 2, 6]
        >>> [*cumprod(range(1, 4), False)]
        [2, 6]
    """
    consumable = iter(iterable)
    last = next(consumable)
    if first:
        yield last
    for i in consumable:
        last *= i
        yield last

def cumquot(iterable:Iterable[Number], first:bool=True) -> Generator:
    """
    Yield the cumulative quotient of the elemements of an iterable
    example:
        >>> [*cumquot(range(1, 4))]
        [1, 0.5, 0.16666666666666666]
        >>> [*cumquot(range(1, 4), False)]
        [0.5, 0.16666666666666666]
    """
    consumable = iter(iterable)
    last = next(consumable)
    if first:
        yield last
    for i in consumable:
        last /= i
        yield last


def choose(iterable:Iterable[Any], *indices:Iterable[int]) -> Generator:
    """
    Yield specific elements from an iterable by index:
    >>> [*choose(range(1, 10), 0, 3)]
    [1, 4]
    >>> [*choose(range(1, 10), (0, 3))]
    [1, 4]
    
    """
    indices = regenerator(flat(indices))
    yielded = []
    for i, e in enumerate(iterable):
        if i in indices:
            yield e
            yielded.append(e)
        if len(yielded) == len(indices):
            break

def skip(iterable:Iterable[Any], *indices:Iterable[int]) -> Generator:
    """
    Skip specific elements from an iterable by index
    """
    indices = tuple(flat(indices))
    for i, e in enumerate(iterable):
        if not i in indices:
            yield e

def dupers(array:Iterable, once:bool=True, key:Callable=lambda x:x) -> Generator:
    """
    Yield the elements of a finite iterable whose frequency is greater than one
    :once:
        if set to false, all duplicate copies of the element shall be yielded
    :key:
        the function/type to use as the key for the sorting function (sorted(array, key=key))
    eg
        >>> [*dupes([1,2,2,2,1,3])]
        [1, 2]
        >>> [*dupes([1,2,2,2,1,3], False)]
        [1, 2, 2]
    """
    array = iter(sorted(array, key=key))
    last_seen = next(array)
    last_yield = None
    for i in array:
        if i==last_seen:
            if once:
                if i!=last_yield:
                    yield i
            else:
                yield i
            last_yield = i
        last_seen = i
    
def slices(iterable:Iterable, length:int, fill:Any=None) -> Generator:
    """
    Yield the adjacent slices of a given length for the given iterable. Trailing values will be padded by copies of 'fill'
        use filter(all, slices(iterable, length)) to discard remainders
    :fill:
        the default value of any 
    eg:
        >>> [*slices('abc', 2, None)]
        [('a', 'b'), ('c', None)]
        >>> [*filter(all, slices('abc', 2, None))]
        [('a', 'b')]
    """
    itr = iter(iterable)
    while (main:=[*islice(itr, 0, length)]):
        main += [fill for i in range(length-len(main))]
        yield tuple(main)


def repeat(func:Callable, inpt:Any, times:int=2, **kwargs):
    """
    Get the output of recursive calls of a function some number of times
    Dependencies: None
    In: function,input,times[=1]
    Out: Function call
    
    repeat(lambda x: x+1,0)
        2
    repeat(lambda x: x+1,0,1)
        1
    """
    for i in range(times):
        inpt = func(inpt, **kwargs)
    return inpt
recursor = repeat


def eq(*args:Iterable[Any]) -> bool:
    """
    Check if arguments are equal
    Will always return True if the only argument given is not an iterable
    """
    if len(args) == 1:
        if hasattr(arg:=args[0], '__iter__'):
            return eq(*arg)
        return True
    
    args = iter(args)
    arg0 = next(args)
    
    for i in args:
        if i != arg0:
            return False
    return True


def clock(func:Callable, value:bool=False, name:bool=False, verbose:bool=False) -> Callable:
    """
    A decorator for benchmarking functions
    
    :name:
        option to print the name of the function with the time taken to call it
    :value:
        return the value of the function instead of the period
    
    taken from
    Mari Wahl, mari.wahl9@gmail.com
    University of New York at Stony Brook
    """
    def wrapper(*args:Any, **kwargs:Any) -> Any:
        t = time.perf_counter()
        res = func(*args, **kwargs)
        delta = time.perf_counter()-t
        if verbose:
            if name:
                print(f"{func.__name__}\n\t{delta}")
            else:
                print(f"d={delta}")
        return res if value else delta
    return wrapper
benchmark = clock


def imap(argument:Any, *functions:Callable) -> Generator:
    """
    Converse of a map. Yield calls of the functions with the object as an argument
    Generator safe
    """
    iterates = hasattr(object, '__iter__')
    for func in functions:
        yield func((argument, regenerator(argument))[iterates])


def rmap(argument:Any, *functions:Callable) -> Any:
    """
    Recursively call functions on an argument. Return the result of the last call
    Generator safe
    """
    functions = iter(functions)
    iterates = hasattr(object, '__iter__')
    result = next(functions)((argument, regenerator(argument))[iterates])
    for func in functions:
        result = func((result, regenerator(result))[iterates])
    return result


def dictate(dictionary:dict, *omissions:Hashable, include:bool=False):
    """
    Create a selective clone of a dictionary
    params:
        omissions
            the hashable values corresponding to keys you would like to remove
        include
            If true, only keys specified in "omissions" will persist in the final dictionary
            
    >>> dictate(dict(zip('abc', range(3))), 'a')
    {'b': 1, 'c': 2}
    >>> dictate(dict(zip('abc', range(3))), 'a', include=True)
    {'a': 0}
    >>> dictate(dict(zip('abc', range(3))), 'b c'.split(), include=True)
    {'b': 1, 'c': 2}
    
    """
    if include:
        return {key: dictionary.get(key) for key in dictionary if key in flat(omissions)}
    return {key: dictionary.get(key) for key in dictionary if not key in flat(omissions)}


def itersplit(iterable:Iterable[Any], *indices:int, cumulative:bool=False):
    """
    Split an iterable at the given indices or their cumulative sums
    
    examples:
        >>> sl4ng.show(itersplit('gravitation', 3, 6, 8))
        ('g', 'r', 'a')
        ('v', 'i', 't')
        ('a', 't')
        ('i', 'o', 'n')
        >>> sl4ng.show(itersplit('gravitation', 3, 3, 2, cumulative=True))
        ('g', 'r', 'a')
        ('v', 'i', 't')
        ('a', 't')
        ('i', 'o', 'n')
    """
    indices = flat(indices)
    indices = regenerator(cumsum(indices, first=False)) if cumulative else sorted(indices)
    assert all(isinstance(i, int) for i in indices), "Some indices aren't integers"
    
    boxes = tuple([] for i in indices)
    index = 0
    iterable = iter(iterable)
    for i, e in enumerate(iterable):
        if i >= indices[index]:
            yield tuple(boxes[index])
            index += 1
        
        try:
            boxes[index].append(e)
        except IndexError:
            break
            

    if (last := tuple([e, *iterable])):
        yield tuple(last)


def interval(start:float, stop:float, step:float, reverse=False) -> Generator:
    """
    Compute an [x0, x1, dx)-interval and its cardinality
    Params
        start:
            least element of the interval
        stop:
            cutoff element
        step:
            difference between consecutive elements
        reverse:
            traverse the interval in reverse order
        
    """
    # ctr = 0
    # itr = []
    while start + step < stop:
        # itr.append(start)
        yield start
        start += step
        # ctr += 1
    # return ctr, itr

class Interval:
    def __init__(self, start:float, stop:float, step:float):
        """
        Compute a yielding [)-interval and access useful properties such as its cardinality.
        This is essentially equivalent to "range", for non-integer aritmetics
        Params
            start:
                least element of the interval
            stop:
                cutoff element
            step:
                difference between consecutive elements
            reverse:
                traverse the interval in reverse order
            
        """
        self.start = start 
        self.stop = stop 
        self.step = step
    def __iter__(self):
        start = self.start 
        stop = self.stop 
        step = self.step
        while start + step < stop:
            yield start
            start += step
    def __len__(self):
        return sum(1 for i in self)
    def __reversed__(self):
        start = self.start 
        stop = self.stop 
        step = self.step
        while stop - step > start:
            yield start
            stop -= step
    def __getitem__(self, key:int):
        for index, item in enumerate(self):
            if index==key:
                return item
        raise IndexError

if __name__ == "__main__":
    from statistics import median
    # pass
    # for i in range(1,10):
        # print([*range(i)])
        # print(median(range(i)))
    n = 6
    for i in range(n):
        print(roll(range(3), i))
    for i in range(n):
        print(roll(range(3), 3, i))
    