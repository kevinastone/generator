#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_generator
----------------------------------

Tests for `generator` module.
"""

import itertools
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import mock

from generator import generate, generator, GeneratorMixin, GeneratorTest


class AssertCalledWithInputs(object):
    def assert_called_with_inputs(self, spy, inputs):
        for call, expected in zip(spy.call_args_list, inputs):
            args, kwargs = call
            self.assertEqual(args, expected)


class TestGenerateDecorator(AssertCalledWithInputs, unittest.TestCase):

    def setUp(self):
        self.inputs = 1, 2, 3
        self.spy = mock.Mock(__name__='test_method')
        self.test_case = mock.Mock()
        decorator = generate(*self.inputs)
        self.generated = decorator(self.spy)

    def test_decorated_generator_test(self):
        self.assertIsInstance(self.generated, GeneratorTest)

    def test_decorated_callable(self):
        self.generated(self.test_case)
        self.assertEqual(self.spy.call_count, len(self.inputs))
        self.assert_called_with_inputs(
            self.spy,
            zip(itertools.repeat(self.test_case), self.inputs)
        )

    def test_decorated_iterator(self):
        methods = list(self.generated)
        self.assertEqual(len(methods), len(self.inputs))

        for method in methods:
            method(self.test_case)

        self.assertEqual(self.spy.call_count, len(self.inputs))
        self.assert_called_with_inputs(
            self.spy,
            zip(itertools.repeat(self.test_case), self.inputs)
        )


class TestGenerator(AssertCalledWithInputs, unittest.TestCase):
    def setUp(self):
        self.inputs = 1, 2, 3
        self.spy = mock.Mock()

        class Example(object):
            @generate(*self.inputs)
            def test_method(me, arg):
                self.spy(arg)

        self.klass = Example
        self.generated = generator(self.klass)

    def test_generator_naming(self):
        tests = unittest.TestLoader().getTestCaseNames(self.generated)
        for test in tests:
            self.assertTrue(test.startswith('test_method'))

    def test_generator_count(self):
        tests = unittest.TestLoader().getTestCaseNames(self.generated)
        self.assertEqual(len(tests), len(self.inputs))

    def test_generator_methods(self):
        tests = unittest.TestLoader().getTestCaseNames(self.generated)
        example = self.generated()
        for test in tests:
            method = getattr(example, test)
            method()
        self.assertEqual(self.spy.call_count, len(self.inputs))
        self.assert_called_with_inputs(
            self.spy,
            zip(self.inputs),
        )


class TestGeneratorMixin(AssertCalledWithInputs, unittest.TestCase):
    def setUp(self):
        self.inputs = 1, 2, 3
        self.spy = mock.Mock()
        self.other_spy = mock.Mock()

        class Example(GeneratorMixin, unittest.TestCase):
            @generate(*self.inputs)
            def test_method(me, arg):
                self.spy(arg)

        class DerivedExample(Example):
            @generate(*self.inputs)
            def test_another_method(me, arg):
                self.other_spy(arg)

        self.Example = Example
        self.DerivedExample = DerivedExample

    def test_generator_test_case_base_count(self):
        suite = unittest.TestLoader().loadTestsFromTestCase(self.Example)
        result = unittest.TestResult()
        suite.run(result)
        self.assertEqual(result.testsRun, len(self.inputs))
        self.assertEqual(self.spy.call_count, len(self.inputs))

    def test_generator_test_case_derived_count(self):
        suite = unittest.TestLoader().loadTestsFromTestCase(self.DerivedExample)
        result = unittest.TestResult()
        suite.run(result)
        self.assertEqual(result.testsRun, 2 * len(self.inputs))
        self.assertEqual(self.spy.call_count, len(self.inputs))
        self.assertEqual(self.other_spy.call_count, len(self.inputs))
