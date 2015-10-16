===============================
Generator
===============================

.. image:: https://img.shields.io/travis/kevinastone/generator.svg
        :target: https://travis-ci.org/kevinastone/generator

.. image:: https://img.shields.io/pypi/v/generator.svg
        :target: https://pypi.python.org/pypi/generator


Generator is a helper for generating test methods for nose while still using unittest.

* Free software: ISC license
* Documentation: https://generator.readthedocs.org.


Installation
------------

::

    pip install test-generator


Introduction
------------

Have you ever written tests that loop through a list of inputs to validate the functionality?

Something like?

.. code-block:: python

    from mything import thingy

    class MyTestCase(unittest.TestCase):
        def test_thingy(self):
            for input in [
                'a',
                'b',
                'cccc',
                'ddd'
                'eeeeee',
                'f',
                'g'
            ]:
                self.assertTrue(thingy(input))


But running in a loop limits all the functionality in ``TestCase`` like per-
test setUp or tearDown.  It also fails on the first input and you can't run a
single test input, you have to run them all?  (Doesn't work well when each
test is more complicated than this toy case).

Instead, what if you wrote your test like:

.. code-block:: python

    from generator import generator, generate
    from mything import thingy

    @generator
    class MyTestCase(unittest.TestCase):

        @generate('a', 'b', 'cccc', 'ddd', 'eeeeee', 'f', 'g'):
        def test_thingy(self, input):
            self.assertTrue(thingy(input))


And when you run your tests, you see:

.. code-block:: shell

    ----------------------------------------------------------------------
    Ran 7 tests in 0.001s

    OK

Generator gives you simple decorators to mulitply your test methods based on
an argument list.  It's great for checking a range of inputs, a list of error
conditions or expected status codes.


Examples
--------

API Client Error Handling
^^^^^^^^^^^^^^^^^^^^^^^^^

Let's make sure our API client properly handles error conditions and raises a
generic APIError under the conditions.  We'll use mock to patch out the actual
API call to return our response.

.. code-block:: python

    import mock
    from generator import generator, generate
    from example import client, APIError

    @generator
    class TestAPIErrorHandling(unittest.TestCase):

        @generate(400, 401, 403, 404, 500, 502, 503)
        def test_error(self, status_code):
            with mock.patch(client, '_request') as _request_stub:
                _request_stub.return_value.status_code = status_code

                self.assertRaises(APIError):
                    client.get('/path/')


Test Fixtures
^^^^^^^^^^^^^

Let's make sure our API client properly handles error conditions and raises a
generic APIError under the conditions.  We'll use mock to patch out the actual
API call to return our response.

.. code-block:: python

    from generator import generator, generate
    from example.sanitize import strip_tags

    @generator
    class TestStripTags(unittest.TestCase):

        @generate(
            ('<h1>hi</h1>', 'hi'),
            ('<script></script>something', 'something'),
            ('<div class="important"><p>some text</p></div>', 'some text'),
        )
        def test_strip_tags(self, input, expected):
            self.assertEqual(strip_tags(input), expected)
