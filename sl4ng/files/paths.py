from typing import Iterable

import os, sys, time


defaultScriptDirectory = r'e:\projects\monties'
commons = {
    'music': os.path.join(os.path.expanduser('~'), 'music', 'collection'),
    'images': os.path.join(os.path.expanduser('~'), 'pictures'),
    'pictures': os.path.join(os.path.expanduser('~'), 'pictures'),
    'pics': os.path.join(os.path.expanduser('~'), 'pictures'),
    'videos': os.path.join(os.path.expanduser('~'), 'videos'),
    'ytdls': {
        'music': {
            'singles': os.path.join(os.path.expanduser('~'), 'videos', 'ytdls', 'music', 'singles'),
            'mixes': os.path.join(os.path.expanduser('~'), 'videos', 'ytdls', 'music', 'mixes'),
            'albums': os.path.join(os.path.expanduser('~'), 'videos', 'ytdls', 'music', 'album'),
        },
        'graff': os.path.join(os.path.expanduser('~'), 'videos', 'ytdls', 'graff'),
        'bullshit': os.path.join(os.path.expanduser('~'), 'videos', 'ytdls', 'bullshitters'),
        'bull': os.path.join(os.path.expanduser('~'), 'videos', 'ytdls', 'bullshitters'),
        'code': os.path.join(os.path.expanduser('~'), 'videos', 'ytdls', 'cscode'),
        'cs': os.path.join(os.path.expanduser('~'), 'videos', 'ytdls', 'cscode'),
        'maths': os.path.join(os.path.expanduser('~'), 'videos', 'ytdls', 'maths'),
        'math': os.path.join(os.path.expanduser('~'), 'videos', 'ytdls', 'maths'),
        'movies': os.path.join(os.path.expanduser('~'), 'videos', 'ytdls', 'movies'),
        'other': os.path.join(os.path.expanduser('~'), 'videos', 'ytdls', 'other'),
        'physics': os.path.join(os.path.expanduser('~'), 'videos', 'ytdls', 'physics'),
        'phys': os.path.join(os.path.expanduser('~'), 'videos', 'ytdls', 'physics'),
        'politics': os.path.join(os.path.expanduser('~'), 'videos', 'ytdls', 'politics'),
        'pol': os.path.join(os.path.expanduser('~'), 'videos', 'ytdls', 'politics'),
    },
    'documents': os.path.join(os.path.expanduser('~'), 'documents'),
    'docs': os.path.join(os.path.expanduser('~'), 'documents'),
    'downloads': os.path.join(os.path.expanduser('~'), 'downloads'),
    'desktop': os.path.join(os.path.expanduser('~'), 'desktop'),
    'books': os.path.join(os.path.expanduser('~'), 'documents', 'bookes'),
    'monties': os.path.join(defaultScriptDirectory, str(time.localtime()[0])),
    'scripts': defaultScriptDirectory,
    'demos': os.path.join(defaultScriptDirectory, 'demos'),
    'site': os.path.join(sys.exec_prefix, 'lib', 'site-packages'),
    'home': os.path.expanduser('~'),
    'user': os.path.expanduser('~'),
    'root': os.path.expanduser('~'),
    '~': os.path.expanduser('~'),
}
os.makedirs(commons['monties'], exist_ok=True)


def delevel(path:str, steps:int=1) -> str:
    """
    This will climb the given path tree by the given number of steps.
    No matter how large the number of steps, it will stop as soon as it reaches the root.
    Probably needs revision for paths on systems which hide the root drive.
    example
        >>> for i in range(4):print(delevel(r'c:/users/admin',i))
        c:/users/admin
        c:/users
        c:/
        c:/
    dependencies: os.sep
    """
    while steps and (len(path.split(os.sep))-1):
        path = os.sep.join((path.split(os.sep)[:-1]))
        steps -= 1
    return path if not path.endswith(':') else path+os.sep


def namespacer(path:str, sep:str='_', start:int=2) -> str:
    """
    Returns a unique version of a given string by appending an integer
    
    example:
        tree:
            /folder
                /file.ext
                /file_2.ext
        
        >>> nameSpacer('file', sep='-', start=2)
        file-2.ext
        >>> nameSpacer('file', sep='_', start=2)
        file_3.ext
        >>> nameSpacer('file', sep='_', start=0)
        file_0.ext
    """
    id = start
    oldPath = path[:]
    while os.path.exists(path): ##for general use
        newPath = list(os.path.splitext(path))
        if sep in newPath[0]:
            if newPath[0].split(sep)[-1].isnumeric():
                # print('case1a')
                id = newPath[0].split(sep)[-1]
                newPath[0] = newPath[0].replace(f'{sep}{id}', f'{sep}{str(int(id)+1)}')
                path = ''.join(newPath)
            else:
                # print('case1b')
                newPath[0] += f'{sep}{id}'
                path = ''.join(newPath)
                id += 1
        else:
            # print('case2')
            newPath[0] += f'{sep}{id}'
            path = ''.join(newPath)
            id += 1
    return path
nameUpdater = nameSpacer = name_spacer = namespacer


def mcd(args:Iterable[str], go_back:bool=False, recursive:bool=True, overwrite:bool=False) -> str:
    """
    recursively create and enter directories.
    
    go_back:
        if set to True, the process will return to the starting directory
    recursive:
        if set to false, all directories will be created in the starting directory
            
    eg
        each of the following calls create the following tree:
            dir-1
                dir0: starting directory
                    dir1
                        dir2
                        dir3
                    dir4
            dir5
        
        >>> mcd('dir1 dir2 .. dir3 .. .. dir4 .. .. dir5'.split())
        >>> mcd('dir1/dir2 ../dir3 ../../dir4 ../../dir5'.split())
    """
    home = os.getcwd()
    for arg in args:
        arg = nameSpacer(arg) if arg!='..' and not overwrite else arg
        os.makedirs(arg, exist_ok=True)
        os.chdir(arg if recursive else home)
    last_stop = home if go_back else os.getcwd()
    os.chdir(last_stop)
    return last_stop


if __name__ == "__main__":
    here, this = os.path.split(__file__)
    this_2 = nameSpacer(this)
    if not os.path.exists(this_2):
        with open(this_2, 'x') as f:
            print(nameUpdater(this, '-', 2))
            print(nameUpdater(this, '_', 2))
            print(nameUpdater(this, '_', 0))
        os.remove(this_2)
    # [*map(os.remove, (this, this_2))]