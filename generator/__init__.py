from __future__ import absolute_import

import inspect

from .version import __version__    # noqa


class GeneratorTest(object):
    def __init__(self, func, *args):
        self.args = args
        self.func = func

    def __iter__(self):
        for arg in self.args:
            def test_arg(func, *arg):
                def wrapper_func(test_case):
                    return func(test_case, *arg)
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


class GeneratorTestCaseMeta(type):
    def __new__(metaclass, name, bases, attributes):
        cls = super(GeneratorTestCaseMeta, metaclass).__new__(metaclass, name, bases, attributes)
        return generator(cls)


class GeneratorTestCase(object):
    __metaclass__ = GeneratorTestCaseMeta

    generate = staticmethod(generate)
