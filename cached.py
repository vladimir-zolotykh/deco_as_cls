#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


import weakref


class Cached(type):
    # instances = weakref.WeakValueDictionary()
    instances = {}

    def __init__(cls, *args, **kwargs):
        # cls.instances = weakref.WeakValueDictionary()
        # cls.instances = {}
        type(cls).instances[cls] = {}

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
