from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals
)

import unittest
from ntuple.tests._objects import Event, Electron
from ntuple.content import NTupleVariable


class TestNTupleVariable(unittest.TestCase):

    def setUp(self):
        e1 = Electron(50, 0.8)
        e2 = Electron(30, 0.001)
        e3 = Electron(23, 0.001)
        self.e1, self.e2, self.e3 = e1, e2, e3

        self.event1 = Event(1, 13700, [e1, e2, e3])
        self.event2 = Event(2000, 64000, [e1, e3])

    def test_simple_var_access(self):
        run_number = NTupleVariable(
            'run_number', vtype='uint',
            extract_function=lambda event: event.getRun())
        self.assertEqual(run_number.extract(self.event1), self.event1.getRun())
        self.assertEqual(run_number.extract(self.event2), self.event2.getRun())

        event_number = NTupleVariable(
            'event_number', vtype='uint',
            extract_function=lambda event: event.id())
        self.assertEqual(event_number.extract(self.event1), self.event1.id())
        self.assertEqual(event_number.extract(self.event2), self.event2.id())

    def test_collection_var_access(self):
        first_e_pt = NTupleVariable(
            'first_e_pt', vtype='float',
            extract_function=lambda event: event.electrons[0].pt)
        self.assertEqual(first_e_pt.extract(self.event1), self.e1.pt)

    def tearDown(self):
        pass
