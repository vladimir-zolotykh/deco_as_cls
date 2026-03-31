#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
import functools
import logging


def log_it(clsname):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(clsname)
            logger.info(f"{func.__name__} called {args}, {kwargs}")
            res = func(*args, **kwargs)
            logger.info(f"{func.__name__} returns {res}")
            return res

        return wrapper

    return decorator


class AutoLogMeta(type):
    def __new__(mcls, clsname, bases, clsdict):

        logger = logging.getLogger(clsname)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            handler = logging.FileHandler(
                f".{os.path.splitext(os.path.basename(__file__))[0]}.log", mode="w"
            )
            formatter = logging.Formatter(
                "%(asctime)s %(name)s %(message)s", datefmt="%H:%M:%S"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        for attr, value in clsdict.items():
            if callable(value) and not attr.startswith("__"):
                clsdict[attr] = log_it(clsname)(value)
        return super().__new__(mcls, clsname, bases, clsdict)


class Mathbox(metaclass=AutoLogMeta):
    def add(self, x, y):
        return x + y

    def mul(self, a, b):
        return a * b


if __name__ == "__main__":
    import pytest
    import sys

    pytest.main(sys.argv)


def test_autolog(capsys):
    mb = Mathbox()
    assert mb.add(10, 5) == 15
    assert mb.mul(17.3, 19.7) == 340.81
