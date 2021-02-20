from typing import Sequence, Iterable
import re, os, subprocess

import filetype as ft

from ..types import generator
from ..iteration import shuffle


def search(keyword:str, directory:str, extension:str='', walk=True, **kwargs) -> generator:
    """
    Find files matching the given keyword within a directory
    """
    if re.search('\s', keyword):
        keyword = map(lambda x: x.strip(), keyword.split())
    if not isinstance(keyword, str):
        keyword = '|'.join(map(re.escape, keyword))
    else:
        keyword = re.escape(keyword)
    return filter(
        lambda file:re.search(keyword, file.split(os.sep)[-1], re.I),
        gather(directory, ext=extension, names=False, walk=walk, **kwargs)
    )


def sortbysize(files:Iterable[str]=None) -> list:
    """
    Sort a collection of file paths by the size of the corresponding files (largest to smallest)
    """
    files = [os.getcwd(), list(files)][bool(files)]
    size = lambda file: os.stat(file).st_size
    out = []
    while len(files)>0:
        sizes = set(size(file) for file in files)
        for file in files:
            if size(file) == max(sizes):
                out.append(file)
                files.remove(file)
    return out


def gather(folder:str=None, names:bool=False, walk:bool=True, ext:str=None) -> generator:
    """
    Generate an iterable of the files rooted in a given folder
    """
    folder = [os.getcwd(), folder][bool(folder)]
    if walk:
        if ext:
            ext = ext.replace('.', '')
            pred = [i for i in ',`* ' if i in ext]
            pattern = '|'.join(f'\.{i}$' for i in ext.split(pred[0] if pred else None))
            pat = re.compile(pattern, re.I)
            for root, folders, files in os.walk(folder):
                for file in files:
                    if os.path.isfile(p:=os.path.join(root, file)) and pat.search(file) and file!='NTUSER.DAT':
                        yield file if names else p
        else:
            for root, folders, titles in os.walk(folder):
                for t in titles:
                    if os.path.exists(p:=os.path.join(root, t)):
                        yield t if names else p
    else:
        if ext:
            ext = ext.replace('.', '')
            pred = [i for i in ',`* ' if i in ext]
            pattern = '|'.join(f'\.{i}$' for i in ext.split(pred[0] if pred else None))
            pat = re.compile(pattern, re.I)
            for file in os.listdir(folder):
                if os.path.isfile(p:=os.path.join(folder, file)) and pat.search(file) and file!='NTUSER.DAT':
                    yield file if names else p
        else:
            for file in os.listdir(folder):
                if os.path.isfile(p:=os.path.join(folder, file)):
                    yield file if names else p


def straw(path:str, text:bool=True, lines:bool=False) -> [str, list]:
    """
    Extract the text, or bytes if the keyword is set to false, from a file
    ::text::
        text or bytes?
    ::lines::
        split text by line or return raw?
    """
    if os.path.isfile(path):
        mode = "rb r".split()[text]
        with open(path, mode) as f:
            return f.readlines() if lines else f.read()


def unarchive(path:str, destination:str=None, app:str='rar') -> None:
    """
    Extract an archive to a chosen destination, or one generated based on the name of the archive
    App refers to the comandlet you wish to invoke via subprocess.run
    """
    options = {
        'tar':'-x -f',
        'rar':'e -or -r',
        'winrar':'',
    }
    if destination != None:
        os.makedirs(destination, exist_ok=True)
        os.chdir(destination)
        subprocess.run(f'{app} {options[app]} "{path}" ')
    else:
        destination = os.path.splitext(path)[0]
        src = os.path.join('.', os.path.split(path)[1])
        print(destination, path, src)
        os.makedirs(destination, exist_ok=True)
        os.chdir(destination)
        subprocess.run(f'{app} {options[app]} "{src}" ')

extractRar = unarchive


def empty(path:str, make:bool=False) -> bool:
    """
    Check if a given file or folder is empty or not with the option to create it if it doesn't exit 
    """
    if os.path.exists(path):
        if os.path.isfile(path):
            with open(path, 'rb') as f:
                return not bool(len(tuple(i for i in f)))
        elif os.path.isdir(path):
            return not bool(len(os.listdir(file)))
    elif make:
        if os.path.splitext(path)[-1]:
            x = open(path, 'x')
            x.close()
        else:
            os.makedirs(path, exist_ok=True)
        return True


def ffplay(files:Sequence[str], hide:bool=True, fullscreen:bool=True, loop:bool=True, quiet:bool=True, randomize:bool=True, silent:bool=False) -> None:
    """
    Play a collection of files using ffmpeg's "ffplay" cli
    
    If entering files as a string, separate each path by an asterisk (*), othewise feel free to use any iterator
    -loop {f"-loop {loop}" if loop else ""}
    """
    
    # fullscreen = False if hide else fullscreen
    namext = lambda file: os.path.split(file)[1]
    nome = lambda file: os.path.splitext(namext(file))[0]
    ext = lambda file: os.path.splitext(file)[1]
    isvid = lambda file: ft.match(file) in ft.video_matchers
    vidtitle = lambda vid: '-'.join(i.strip() for i in vid.split('-')[:-1])
    albumtrack = lambda file: bool(re.search(f'\d+\s.+{ext(file)}', file, re.I))
    attitle = lambda file: ' '.join(i.strip() for i in nome(file).split(' ')[1:])
    aov = lambda file: albumtrack(file) or isvid(file)
    title = lambda file: ''.join(i for i in os.path.splitext(namext(file)[1])[0] if i not in '0123456789').strip()
    windowtitle = lambda file: [namext(file), [attitle(file), vidtitle(file)][isvid(file)]][aov(file)]
    play = lambda file: subprocess.run(f'ffplay {("", "-nodisp")[hide]} -window_title "{windowtitle(file)}" -autoexit {"-fs" if fullscreen else ""} {"-v error" if quiet else ""} "{file}"')
    files = files.split('*') if isinstance(files,str) else files
    if loop:
        while (1 if loop==True else loop+1):
            files = shuffle(files) if randomize else files
            for i,f in enumerate(files, 1):
                if os.path.isdir(f):
                    fls = [os.path.join(f, i) for i in gather(f, names=False)]
                    for j,file in enumerate(fls, 1):
                        name = os.path.split(file)[1]
                        print(f'{j} of {len(fls)}:\t{name}') if not silent else None
                        ffplay(file, hide, fullscreen, False, quiet, randomize, True)
                else:
                    folder,name = os.path.split(f)
                    print(f'{i} of {len(files)}:\t{name}') if not silent else None
                    play(f)
            loop -= 1
    else:
        files = shuffle(files) if randomize else files
        for i, f in enumerate(files, 1):
            if os.path.isdir(f):
                fls = [os.path.join(f, i) for i in gather(f, names=False)]
                for j, file in enumerate(fls, 1):
                    name = os.path.split(file)[1]
                    print(f'{j} of {len(fls)}:\t{name}') if not silent else None
                    ffplay(file, hide, fullscreen, False, quiet, randomize, True)
            else:
                print(f'{i} of {len(files)}:\t{title(f)}') if not silent else None
                play(f)


size = lambda file: os.stat(file).st_size