========
Usage
========

You can use Generator as either a decorator or a mixin.  The decorator is a
bit cleaner, but doesn't automatically generate any decorated methods in a
sub-class.


Decorator
---------

::

    import unittest
    from generator import generate, generator


    @generator
    class MyTestCase(unittest.TestCase):

        @generate(1, 2, 3):
        def test_is_positive(self, value):
            self.assertGreater(value, 0)


Mixin
-----

::

    import unittest
    from generator import generate, GeneratorMixin


    class MyTestCase(GeneratorMixin, unittest.TestCase):

        @generate(1, 2, 3):
        def test_is_positive(self, value):
            self.assertGreater(value, 0)


    class AnotherMyTestCase(MyTestCase):

        @generate(1, 3, 5):
        def test_is_odd(self, value):
            self.assertTrue(value % 2)
