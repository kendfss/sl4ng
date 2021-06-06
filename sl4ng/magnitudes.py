"""
Making numbers readable and dimensional one order of magnitude at a time
"""
__all__ = 'nice_size nice_duration MemorySize Duration'.split()

from .debug import show
from .iteration import sample, nopes


orders = {
    0: 'mono',
    1: 'deca',
    2: 'hecto',
    3: 'kilo',
    6: 'mega',
    9: 'giga',
    12: 'tera',
    15: 'peta',
    18: 'exa',
    21: 'zetta',
    24: 'yotta',
}

sredro = {v:k for k, v in orders.items()}

def lasso(number:complex, unit:str='') -> str:
    """
    Make a large number more readable by inserting commas before every third power of 10 and adding units
    """
    return f'{number:,} {unit}'.strip()

def set_case(unit:str, lower:bool=False) -> str:
    """
    Set the case of a number's unit string
    """
    return [unit.upper().strip(), unit.lower().strip()][lower]

def set_length(mag:str, unit:str, long:bool=False, sep:str='-') -> str:
    """
    Set the length of a number's unit string
    """
    return ('', sep)[long].join(((mag[0], unit[0]), (mag, unit))[long])

def magnitude(value:complex, omissions:list='mono deca hecto'.split()):
    """
    Determine the best order of magnitude for a given number
    """
    mags = tuple(sorted(i for i in orders.keys() if not orders[i] in omissions))
    booly = lambda i: len(str(int(value))) < len(str(10**mags[i+1]))
    fits = tuple(nopes((booly(i) for i in range(len(mags)-1)),True))
    fit = mags[min(fits) if fits else len(mags)-1]
    return orders[fit]

def nice_size(self:complex, unit:str='bytes', long:bool=False, lower:bool=False, precision:int=2, sep:str='-', omissions:list='mono deca hecto'.split()):
    """
    This should behave well on int subclasses
    """
    mag = magnitude(self, omissions)
    precision = sredro[mag] if self<5 else precision
    unit = set_case(set_length(mag, unit, long, sep), lower)
    val = round(self*10**-(sredro[mag]), precision)
    return lasso(val, unit)
    
class MemorySize(int):
    """
    Why should you have to sacrifice utility for readability?
    """
    def __repr__(self):
        return nice_size(self)



second = 1
minute = 60 * second
hour = 60 * minute
day = 24 * hour
week = 7 * day
feb = 4 * week
year = 365.25 * day
# year = 13.044642857142858 * feb


def time_dict(duration):
    periods = {
        # 'years': int(duration // year),
        'febs': int(duration // feb),
        # 'febs': int(duration % year // feb),
        'weeks': int(duration % feb // week),
        # 'weeks': int(duration % feb // week),
        'days': int(duration % week // day),
        # 'days': int(duration % week // day),
        'hours': int(duration % day // hour),
        # 'hours': int(duration % day // hour),
        'minutes': int(duration % hour // minute),
        # 'minutes': int(duration % hour // minute),
        
        'seconds': round(duration % minute),        
    }
    return periods


def length(period):
    return eval(period[:-1])


def timer_duration(periods, peak, base, watch):
    string = ''
    if watch:
        peak = 'hours'
        base = 'minutes'
    elif length(base) > second:
        base = 'seconds'
    for k,v in periods.items():
        if length(peak) >= length(k) >= length(base):
            if k == peak:
                string += f'{v:02d}'
            else:
                string += f':{v:02d}'
    return string


def verbose_duration(periods, peak, base, short=False):
    string = ''
    for k, v in periods.items():
        if v:
            if length(peak) >= length(k) >= length(base):
                if k == peak:
                    string += f'{v} {k[:1 if short else None]}'
                else:
                    string += f', {v} {k[:1 if short else None]}'
    return string


def nice_duration(duration, verbose=False, short=False, watch=False):
    """
    Given a number of seconds, return a string which indicates the amount of time in:
        Months (28 days), weeks, days, hours, minutes, seconds
    
    parameters:
        duration
            number of seconds
        verbose
            include units in result
        short
            abbreviate units
        watch
            only "hours:minutes"
    
    examples:
        >>> humanize_duration(62)
        '01:02'
        
        >>> t = 12532510
        
        >>> humanize_duration(t)
        20:05:01:15:10
        
        >>> humanize_duration(t, verbose=True)
        20 weeks, 5 days, 1 hours, 15 months, 10 seconds
        
        >>> humanize_duration(t,verbose=True, short=True)
        20 w, 5 d, 1 h, 15 m, 10 s
        
        >>> humanize_duration(t, watch=True) # equates to "what time will it be after this many seconds have passed"
        01:15
    """
    periods = time_dict(duration)
    significant = [i for i in periods.keys() if periods.get(i)]
    base = min(significant, key=length)
    peak = max(significant, key=length)
    if not verbose:
        return timer_duration(periods, peak, base, watch)
    return verbose_duration(periods, peak, base, short)    

class Duration(float):
    """
    Why should you have to sacrifice utility for readability?
    """
    def __repr__(self):
        return nice_duration(self)



if __name__ == '__main__':
    band = lambda level, base=10, shift=0, root=1: tuple(root+i+shift for i in ((level+1)*base, level*base))[::-1]
    format = lambda selection: int(''.join(str(i) for i in selection))
    
    digits = range(*band(0))
    
    l = 0
    s = 0
    b = 30
    r = 1
    x,y = band(l, b, s, r)
    # print(x,y)
    val = sample(digits,y)
    sizes = [format(val[:i][::-1]) for i in range(x, y)]
    # show(sizes)
    # sizes = [44259260028,315436]
    
    for size in sizes[::-1]:
        string = f"""{(len(lasso(max(sizes)))-len(lasso(size)))*' '+lasso(size)}
            {size = }
            {len(str(size)) = }
            {nice_size(size) = }
            {magnitude(size) = }
        
            
        """.splitlines()
        print(*((x.strip(), x)[i<1] for i, x in enumerate(string)), sep='\n\t', end='\n\n')
    print(lasso(sizes[-1]))
    print(band(l,s,b,r))
    print(x,y)
    print(f'{format(digits):,}')
    # print(all(rep(size)==rep2(size) for size in sizes))