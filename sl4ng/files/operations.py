import os, subprocess

from send2trash import send2trash
from tqdm import tqdm

from .paths import nameUpdater


def convert(file:str, format:str='.wav', bitRate:int=450, delete:bool=False, options:str='') -> str:
    """
    Convert an audio file
    """
    trash = discard
    os.chdir(os.path.split(file)[0])
    
    _title = lambda file: file.split(os.sep)[-1].split('.')[0]
    _new = lambda file, format: nameUpdater(_title(file)+format)
    _name = lambda file: file.split(os.sep)[-1]
    format = '.' + format if '.' != format[0] else format
    
    name = _title(file)
    new = _new(file, format)
    cmd = f'ffmpeg -y -i "{file}" -ab {bitRate*1000} "{new}"' if bitRate != 0 else f'ffmpeg {options} -y -i "{file}" "{new}"'
    announcement = f"Converting:\n\t{file} --> {new}\n\t{cmd=}"
    print(announcement)
    subprocess.run(cmd)
    print('Conversion is complete')
    if delete:
        trash(file)
        print(f'Deletion is complete\n\t{new}\n\n\n')
    return new


def move(file:str, destination:str) -> None:
    """
    Move a file to a given directory
    """
    nmxt = os.path.split(file)[-1]
    ext = os.path.splitext(nmxt)[-1].replace('.', '')
    with open(file, 'rb') as src:
        src = tuple(i for i in src)
        with open(destination, 'wb') as dst:
            print(f'moving {nmxt.split(".")[0]} to the "{ext}" directory')
            for datum in tqdm(src):
                dst.write(datum)


def discard(path:str, recycle:bool=True) -> None:
    """
    Remove an address from the file-system
    """
    fb = (os.remove, send2trash)
    first, backup = fb if not recycle else fb[::-1]
    try:
        first(path)
    except PermissionError:
        backup(path)