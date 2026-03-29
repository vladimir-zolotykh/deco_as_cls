#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> add(2, 3)
5
>>> add(4, 5)
9
>>> add.ncalls
2
>>> s = Spam()
>>> s.bar(1)
<...> 1
>>> s.bar(2)
<...> 2
>>> s.bar(3)
<...> 3
>>> Spam.bar.ncalls
3

"""
# import sys
import os
import logging
import types
from functools import wraps

logging.basicConfig(
    # stream=sys.stderr,
    filemode="w",
    filename=f".{os.path.splitext(os.path.basename(__file__))[0]}.log",
    format="%(asctime)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)
logger = logging.getLogger(name=__name__)


class Profiled:
    def __init__(self, func):
        # logger.info("__init__")
        wraps(func)(self)
        self.ncalls = 0

    def __call__(self, *args, **kwargs):
        logger.info(f"{self.__wrapped__.__name__}({args}, {kwargs})")
        self.ncalls += 1
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, owner=None):
        # logger.info("__get__")
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)


@Profiled
def add(x, y):
    return x + y


class Spam:
    @Profiled
    def bar(self, x):
        print(self, x)


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
