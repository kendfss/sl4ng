# A house for small stones

from functools import lru_cache, reduce
from itertools import chain, combinations, count
from math import pi, ceil
from typing import Iterable, Generator
from numbers import Number, Real, Complex, Integral

# from .types import regenerator
from .iteration import flat, regenerator

def sign(number:Real) -> str:
    return '-+'[number >= 0]

def pyramid(length:Integral, shift:Integral=0) -> Real:
    """
    Returns the product of dividing 1 by each intger in the range(2+shift,2+int(length)+shift) (aka - the number of poops in your pocket)
    if the length is not an integer it will be converted to one
    """
    val = 1
    for i in range(2 + shift, 2 + int(length) + shift):
        val /= i
    return val


def first_primes(n:Integral) -> list:
    """
    Generates a list of the first n primes. A cast will be used if the input is not an integer
    """
    n = int(n) - 1
    bank = []
    track = 2
    while len(bank)< n + 1:
        if all(track % y for y in range(2, min(track, 11))):
            bank.append(track)
        track += 1
    return sorted(set(bank))


def primeslt(n:Integral) -> Generator:
    """
    Generates a list of primes with value lower than the input integer
    """
    return (x for x in range(n) if x > 1 and all(x % y for y in range(2, min(x, 11))))
primes_lower_than = primeslt

def succ(n:Integral) -> Integral:
    """
    Returns the successor of the input number
    """
    return n + 1


def pred(n:Integral) -> Integral:
    """
    Returns the predecessor of the input number
    """
    return n - 1


def rt(x:Integral, n:Complex=2) -> Complex:
    """
    Returns the n-th root of the input number, x
    """
    return x ** (1 / n)


def gcd0(a:Integral, b:Integral) -> Integral:
    """
    The famous euclidean algorithm for computing the greatest common divisor of a pair of numbers a and b
    """
    while a != b:
        if a > b:
            a -= b
        else:
            b -= a
    return a

    
def gcd(*args:[int, tuple]) -> Integral:
    """
    Compute the gcd for more than two integers at a time. Returns input if only one argument is given and it is greater than zero
    """
    if any(i <= 0 for i in args):
        return None
    if len(args) > 1:
        gcds = {d for pair in combinations(args, 2) if all(i % (d := gcd0(*pair)) == 0 for i in args)}
        return max(gcds) if gcds else 1
    elif sum(args) > 0:
        return max(args)


def eratosthenes(n:Integral, imaginarypart:bool=False) -> Generator:
    """
    Implements eratothenes' sieve as a Generator. 
        If the input is not an int it will be rounded to one. 
        Imaginary-part-based rounding optionable
    """
    iscomp = isinstance(n, complex) or issubclass(type(n), complex)
    n = round(n.imag) if imaginarypart and iscomp else round(n.real) if iscomp else round(n)
    rack = range(2, n)
    marked = set()
    primes = set()
    for i in rack:
        if i not in marked:
            multiples = {j for j in rack if j % i == 0 and j > i}
            marked.update(multiples)
            yield i


def _factors(n:Integral) -> Generator:
    """
    Compute the factors of an integer
    """
    pipe = lambda array: reduce(lambda x, y: x*y, array, 1)
    primes = tuple(eratosthenes(n))
    facts = {n, 1} if n!= 0 else {}
    for p in primes:
        if n%p==0:
            e = 1
            while n%p**e==0:
                facts.add(p**e)
                e += 1
    if facts == {n, 1}:
        yield from facts
    else:
        for numbers in chain.from_iterable(combinations(facts, r) for r in range(1, len(facts))):
            if n%pipe(numbers)==0:
                facts.add(pipe(numbers))
        yield from facts   


def factors(*args:[int, tuple]) -> Generator:
    """
    Compute the common factors of any finite number of integers
    """
    args = regenerator(flat(args))
    if all(isinstance(i, int) or i==int(i) for i in args):
        yielded = set()
        for i in args:
            if not i in yielded:
                for j in _factors(i):
                    if not j in yielded:
                        yielded.add(j)
                        if all(not arg%j for arg in args):
                            yield j


@lru_cache(maxsize = 500)
def factorial(n:Integral) -> Integral:
    """
    Return n! for any integer
    """
    if n>=0:
        k = 1
        while n:
            k *= n
            n -= 1
        return k
    else:
        return -factorial(abs(n))


def binomial(n:Integral, k:Integral) -> Integral:
    """
    Returns the n choose k for any k in range(n)
    """
    return int(factorial(n)/(factorial(n-k)*factorial(k)))


def options(iterable:Iterable) -> Integral:
    """
    Returns the number of ways to choose elements from the given iterable
    This will consume a Generator
    """
    consumable = regenerator(iterable)
    length = sum(1 for i in consumable)
    return sum(binomial(length, i) for i in range(length))


def isHarmoDiv(n:Integral) -> bool:
    """
    Computes a boolean whose value corresponds to the statement 'the number n is a Harmonic Divisor Number'
    """
    facts = factors(n)
    return int(harmean(facts)) == harmean(facts)


def isfactor(divisor:Integral, divisee:Integral) -> bool:
    """
    Determines if a Number is a multiple of a Divisor
    """
    return divisee % divisor == 0


def isprime(n:Integral) -> bool:
    """
    Confirm that an integer has no factors other than 1 and itself
    """
    if n < 2:
        return False
    tried = []
    for i in range(2, int(n/2)+1):
        if any(not i%j for j in tried):
            continue
        else:
            tried.append(i) if i > 1 else None
            if not n%i:
                return False
    return True


def isperfect(n:Integral) -> bool:
    """
    Check if an integer is equal to the sum of its factors
    """
    return n == sum(factors(n))


def isabundant(n:Integral) -> bool:
    """
    Check if an integer is greater than the sum of its factors
    """
    return n > sigma(factors(n))


def isdeficient(n:Integral) -> bool:
    """
    Check if an integer is smaller than the sum of its factors
    """
    return n < sigma(factors(n))


def isfilial(n:Integral) -> bool:
    """
    Check if an integer is divisible by the sum of its digits
    """
    return not n % sum(eval(i) for i in str(n))


def mulper(n:Integral) -> Integral:
    """
    Computes the Multiplicative Persistence of an int or float in base-10 positional notation
    If the number is a float the decimal will be removed
    """
    # Exclusions
    if len(str(n)) == 1:
        return 0
    elif (str(0) in str(n)) or ((len(str(n)) == 2) and (str(1) in str(n))):
        return 1
    else:
        ctr = 0
        while len(str(n)) > 1:
            # digitList = [int(i) for i in "".join(str(n).split('.'))]
            digitList = map(int, str(i).replace('.', ''))
            n = reduce(lambda x, y: x*y, digitList, 1)
            ctr += 1
        return ctr


def addper(n:Integral) -> Integral:
    """
    Computes the Additive Persistence of an int or float in base-10 positional notation
    """
    if len(str(n)) == 1:
        return 0
    elif len(str(n)) < 1:
        return ValueError("Your number of choice has less than one digit")
    else:
        ctr = 0
        while len(str(n)) > 1:
            digitList = [int(i) for i in "".join(str(n).split('.'))]
            n = sum(digitList)
            ctr += 1
        return ctr


def triangular(a:Integral, b:Integral) -> Integral:
    """
    Returns the triangular number of an interval [a,b]
    """
    interval = [i for i in range(b) if i > a]
    for num in interval:
        a += num
    return a+b


def rationability(v:Complex) -> Complex:
    """
    Get the subtractive series of the digits of a float, or that of an integer's reciprocal, measured from its math.ceil value
    rationability(math.pi)
        0.8584073464102069
    rationability(3)
        0.6666666666666666
    """
    v = 1/v if isinstance(v, int) else v
    n = ceil(v)
    p = str(v).replace('.', '')
    for i, j in enumerate(p):
        n -= int(j)*10**-i
    return n


def root(value:Complex, power:Complex=2) -> Complex:
    """
    Get the root of a number
    
    rt(complex(1,1))
        (1.0986841134678098+0.45508986056222733j)
    rt(complex(1,1),3)
        (1.0842150814913512+0.2905145555072514j)
    """
    return value**(1/power)


def odds(n:Integral=-1) -> Generator:
    """
    Yield the first n odd numbers, use a negative value for all of them
    """
    ctr = count()
    while n:
        m = next(ctr)
        if m % 2:
            yield m
            n -= 1

def evens(n:Integral=-1) -> Generator:
    """
    Yield the first n even numbers, use a negative value for all of them
    """
    ctr = count()
    while n:
        m = next(ctr)
        if not m % 2:
            yield m
            n -= 1

def congrues(n:Integral, modulus:Integral=6, cls:Integral=1) -> bool:
    """
    Check if n is equal to +-cls modulo modulus
    """
    return n % modulus in {cls, modulus-cls}


def mulseq(root:Integral, base:Integral=2, terms:Integral=-1, start:Integral=0, step:Integral=1) -> Generator:
    """
    Generate a sequence of multiples of a root and a base. By default it will yield the doubles sequence of the root.
    """
    counter = count(start=start, step=step)
    while terms:
        yield root * base**next(counter)
        terms -= 1



if __name__ == "__main__":
    pass