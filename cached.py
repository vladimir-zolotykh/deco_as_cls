#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


import weakref


class Cached(type):
    instances = {}

    def __init__(cls, *args, **kwargs):
        type(cls).instances[cls] = weakref.WeakValueDictionary()

    def __call__(cls, *args):
        tup = tuple(args)
        D = type(cls).instances
        if tup not in D:
            D[tup] = super().__call__(*args)
        return D[tup]


class Spam(metaclass=Cached):
    def __init__(self, name):
        print(f"Initialize({name})")


if __name__ == "__main__":
    s = Spam("Vladimir")
    t = Spam("Tysch")
    q = Spam("Tysch")

    print(t is q)
