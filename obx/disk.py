# This file is placed in the Public Domain.


"read/write"


import datetime
import json
import os
import pathlib
import threading


from .json   import dump, load
from .object import update
from .path   import path


lock = threading.RLock()
p = os.path.join


class Error(Exception):

    pass


def cdir(pth) -> None:
    path = pathlib.Path(pth)
    path.parent.mkdir(parents=True, exist_ok=True)


def fqn(obj) -> str:
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = f"{obj.__module__}.{obj.__name__}"
    return kin


def ident(obj) -> str:
    return p(fqn(obj),*str(datetime.datetime.now()).split())


def read(obj, pth) -> str:
    with lock:
        with open(pth, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                raise Error(pth) from ex
    return pth


def write(obj, pth=None) -> str:
    with lock:
        if pth is None:
            pth = path(obj)
        cdir(pth)
        with open(pth, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        return pth


def __dir__():
    return (
        'cdir',
        'fqn',
        'getpath',
        'ident',
        'last',
        'long',
        'read',
        'search',
        'write'
    )
