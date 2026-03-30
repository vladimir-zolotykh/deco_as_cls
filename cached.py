#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


import weakref


class Cached(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls.instances = weakref.WeakValueDictionary()

    def __call__(cls, *args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if not (key in cls.instances):

            # A WeakValueDictionary does not keep objects alive. It
            # only holds weak references. If there is no strong
            # reference (`obj') to an object elsewhere, it is immediately
            # eligible for garbage collection.

            obj = super().__call__(*args, **kwargs)
            cls.instances[key] = obj

        return cls.instances[key]


class Spam(metaclass=Cached):
    def __init__(self, name):
        print(f"Initialize({name})")


def test_cached(capsys):
    s = Spam("Vladimir")
    t = Spam("Tysch")
    q = Spam("Tysch")
    cap = capsys.readouterr().out.splitlines()
    assert cap[0] == "Initialize(Vladimir)"
    assert cap[1] == "Initialize(Tysch)"
    assert not (s is t)
    assert t is q


if __name__ == "__main__":
    import sys
    import pytest

    pytest.main(sys.argv)
