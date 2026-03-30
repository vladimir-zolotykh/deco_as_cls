#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


import weakref


class Cached(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls.instances = weakref.WeakValueDictionary()
        # cls.instances = {}

    def __call__(cls, *args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key in cls.instances:
            instance = cls.instances[key]
        else:
            instance = cls.instances[key] = super().__call__(*args, **kwargs)
        # return cls.instances[key]
        return instance


class Spam(metaclass=Cached):
    def __init__(self, name):
        print(f"Initialize({name})")


if __name__ == "__main__":
    s = Spam("Vladimir")
    t = Spam("Tysch")
    q = Spam("Tysch")

    print(t is q)
