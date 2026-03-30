#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
import functools
import logging

logger = logging.getLogger(name=__name__)
logging.basicConfig(
    # stream=sys.stderr,
    filename=f".{os.path.splitext(os.path.basename(__file__))[0]}.log",
    format="%(asctime)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)


def log_it(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"{func.__name__} called {args}, {kwargs}")
        res = func(*args, **kwargs)
        logger.info(f"{func.__name__} returns {res}")

    return wrapper


class AutoLogMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        for attr, value in clsdict.items():
            if callable(value) and not attr.startswith("__"):
                clsdict[attr] = log_it(value)
        return super().__new__(mcls, clsname, bases, clsdict)


class Mathbox(metaclass=AutoLogMeta):
    def add(self, x, y):
        return x + y

    def mul(self, a, b):
        return a * b


# def test_qutolog(capsys):
#     mb = Mathbox()
#     mb.add(10, 5)
#     mb.mul(17.3, 19.7)


if __name__ == "__main__":
    mb = Mathbox()
    mb.add(10, 5)
    mb.mul(17.3, 19.7)
