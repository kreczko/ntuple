#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ntuple` module."""

from ntuple.content import convert_type
import unittest
from rootpy.tree.treetypes import IntCol, BoolCol, UIntCol, FloatCol
from rootpy.stl import vector


class NtupleTestCase(unittest.TestCase):

    def setUp(self):
        self.ntuple_types = ['int', 'bool', 'uint', 'float']
        self.ntuple_vtypes = ['vec:{}'.format(t) for t in self.ntuple_types]
        # from
        # https://github.com/rootpy/rootpy/blob/master/rootpy/tree/treetypes.py
        self.root_types = [IntCol, BoolCol, UIntCol, FloatCol]
        self.root_vtypes = [
            vector('int'), vector('bool'), vector('uint'), vector('float')]

    def test_scalars(self):
        for nt, rt in zip(self.ntuple_types, self.root_types):
            self.assertIsInstance(convert_type(nt), rt)

    def test_vectors(self):
        for nt, rt in zip(self.ntuple_vtypes, self.root_vtypes):
            self.assertEqual(convert_type(nt), rt)

    def test_multiple(self):
        variables = []
        for _ in range(5):
            variables.append(convert_type('vec:float'))
        for v in variables:
            self.assertEqual(v, vector('float'))

    def tearDown(self):
        pass
