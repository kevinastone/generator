from __future__ import absolute_import

import functools
import inspect

from six import add_metaclass

from .util import copy_attributes
from .version import __version__    # noqa


copy_attributes = functools.partial(copy_attributes, ignore_patterns=['__*', 'func_*'])


class GeneratorTest(object):
    def __init__(self, func, *args):
        self.args = args
        self.func = func

    def __iter__(self):
        for arg in self.args:
            def test_arg(func, *arg):
                def wrapper_func(test_case):
                    return func(test_case, *arg)
                copy_attributes(self, wrapper_func)
                copy_attributes(self.func, wrapper_func)
                wrapper_func.__name__ = "{method}[{arg!r}]".format(method=func.__name__, arg=arg)
                wrapper_func.__test__ = True
                return wrapper_func

            if not isinstance(arg, tuple):
                arg = arg,
            yield test_arg(self.func, *arg)
        pass

    def __call__(self, test_case):
        for arg in self.args:
            if not isinstance(arg, tuple):
                arg = arg,
            self.func(test_case, *arg)


def generate(*args):
    def decorator(func):
        return GeneratorTest(func, *args)
    return decorator


def generator(klass):
    for name, member in inspect.getmembers(klass):
        if not isinstance(member, GeneratorTest):
            continue

        delattr(klass, name)
        for method in member:
            setattr(klass, method.__name__, method)
    return klass


class GeneratorMeta(type):
    def __new__(metaclass, name, bases, attributes):
        cls = super(GeneratorMeta, metaclass).__new__(metaclass, name, bases, attributes)
        return generator(cls)


@add_metaclass(GeneratorMeta)
class GeneratorMixin(object):
    generate = staticmethod(generate)
