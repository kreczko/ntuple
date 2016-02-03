from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals
)

import unittest
from ntuple.tests._objects import Event, Electron
from ntuple.content import NTupleVariable, NTupleCollection
from rootpy.stl import vector


class TestNTupleCollection(unittest.TestCase):

    def setUp(self):
        e1 = Electron(50, 0.8)
        e2 = Electron(30, 0.001)
        e3 = Electron(23, 0.001)
        self.e1, self.e2, self.e3 = e1, e2, e3

        self.event1 = Event(1, 13700, [e1, e2, e3])
        self.event2 = Event(2000, 64000, [e1, e3])

        self.electrons = NTupleCollection(
            'electrons', source=lambda event: event.electrons,
            help_doc='extract some info from event.electrons',
            variables=[
                NTupleVariable('pt', vtype='float',
                               extract_function=lambda e: e.pt),
                NTupleVariable('hoE', vtype='float',
                               extract_function=lambda e: e.hadronicOverEm),
            ])

        self.nice_electrons = NTupleCollection(
            'electrons', source=lambda event: event.nice_electrons(),
            help_doc='extract some info from event.electrons',
            variables=[
                NTupleVariable('pt', vtype='float',
                               extract_function=lambda e: e.pt),
                NTupleVariable('hoE', vtype='float',
                               extract_function=lambda e: e.hadronicOverEm),
            ])

    def __compare_electrons__(self, eles1, eles2):
        self.assertEqual(len(eles1), 3)
        self.assertEqual(len(eles2), 2)

        e1, e2, e3 = eles1
        self.assertEqual(e1['electrons.pt'], self.e1.pt)
        self.assertEqual(e2['electrons.pt'], self.e2.pt)
        self.assertEqual(e3['electrons.pt'], self.e3.pt)

        self.assertEqual(e1['electrons.hoE'], self.e1.hadronicOverEm)
        self.assertEqual(e2['electrons.hoE'], self.e2.hadronicOverEm)
        self.assertEqual(e3['electrons.hoE'], self.e3.hadronicOverEm)

    def test_collection(self):
        eles1 = self.electrons.extract(self.event1)
        eles2 = self.electrons.extract(self.event2)

        self.__compare_electrons__(eles1, eles2)

    def test_collection_from_function(self):
        eles1 = self.nice_electrons.extract(self.event1)
        eles2 = self.nice_electrons.extract(self.event2)

        self.__compare_electrons__(eles1, eles2)

    def test_branches(self):
        branches = {'electrons.pt': 'vec:float', 'electrons.hoE': 'vec:float'}
        e_branches =  self.electrons.branches
        self.assertDictEqual(e_branches, branches)

    def tearDown(self):
        pass
