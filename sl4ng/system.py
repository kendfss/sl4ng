from __future__ import annotations
import time, random, string

import pyperclip, psutil
from .iteration import shuffle


def agora(string: bool = False) -> str | tuple:
    """
    Here's the local time, Mrs. Wolf!
    Dependencies: time
    In: string=False
    Out: tuple/string(HH:MM:SS)
    """
    now = tuple(time.localtime())[3:-3]
    return now if not string else ':'.join(str(i) for i in now)


def kill(process: str, casefold: bool = True):
    """
    Kill all instances of the argued process name
    Dependencies: psutil
    In: "process_name.exe"[str],casefold=True[bool]
    Out: None
    Inspired by Giampaolo Rodolà from StackOverflow
        http://stackoverflow.com/questions/2940858/ddg#4230226
    """
    import psutil

    if casefold:
        [
            p.kill()
            for p in psutil.process_iter()
            if p.name().casefold()
            == process.casefold() + ('.exe', '')[process.endswith('.exe')]
        ]
    else:
        [
            p.kill()
            for p in psutil.process_iter()
            if p.name() == process + ('.exe', '')[process.endswith('.exe')]
        ]


def guid(
    format: tuple = [8, 4, 4, 4, 12],
    sep: str = '-',
    copy: bool = True,
    braces: bool = True,
) -> str:
    """
    Generate a GUID for different resources
    Dependencies: random,string,pyperclip.copy,m3ta.shuffle
    In: format{length of the intervals of the guid you want}
    Out: str
    """
    # chars = ''.join(i for i in shuffle(string.ascii_uppercase + string.digits+string.ascii_lowercase) if i!=sep)
    chars = ''.join(i for i in shuffle(string.hexdigits) if i != sep)
    ranstr = [random.choice(chars) for i in range(sum(format))]
    [ranstr.insert(i + sum(format[: i + 1]), sep) for i, j in enumerate(format[:-1])]
    result = "{%s}" % (s := ''.join(ranstr)) if braces else s
    pyperclip.copy(result) if copy else None
    return result
