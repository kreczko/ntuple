#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ntuple` module."""

from ntuple.content import convert_type
import unittest

class NtupleTestCase(unittest.TestCase):

    def setUp(self):
        self.ntuple_types = ['int', 'bool', 'uint', 'float']
        self.ntuples_vtypes = ['vec:{}'.format(t) for t in self.ntuple_types]
        # from https://github.com/rootpy/rootpy/blob/master/rootpy/tree/treetypes.py
        self.root_types = ['I', 'B' ,'U', 'F']
        

    def test_int(self):
        for nt, rt in zip(self.ntuple_types, self.root_types):
            self.assertEqual(convert_type(nt, rt))

    def tearDown(self):
        pass
