import unittest
from ntuple.tests._objects import Event, Electron
from ntuple.content import NTupleVariable, NTupleCollection, NTupleContent
from rootpy.io.file import File
import tempfile


class TestNTupleContent(unittest.TestCase):

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

        self.run_number = NTupleVariable(
            'run_number', vtype='uint',
            extract_function=lambda event: event.getRun()
        )
        self.event_number = NTupleVariable(
            'event_number', vtype='uint',
            extract_function=lambda event: event.id()
        )
        self.DATA_ROOT = tempfile.mkdtemp()
        self.output_file = self.DATA_ROOT + '/TestNTupleContent.root'
        self.content = NTupleContent('events', self.output_file)
        self.content.add_collection(self.electrons)
        self.content.add_variable(self.run_number)
        self.content.add_variable(self.event_number)
        map(self.content.fill, [self.event1, self.event2])
        self.content.save()

    def test_file_creation(self):
        import os
        self.assertTrue(os.path.exists(self.output_file))

    def test_tree_branches(self):
        with File.open(self.output_file) as f:
            self.assertTrue(f.__contains__('events'))
            tree = f.get('events')
            branches = ['run_number', 'event_number',
                        'electrons.pt', 'electrons.hoE']
            for branch in branches:
                error_msg = "Branch '{}' does not exist".format(branch)
                self.assertTrue(tree.has_branch(branch), error_msg)

    def test_tree_content(self):
        with File.open(self.output_file) as f:
            tree = f.get('events')
            for i, event in enumerate(tree):
                if i == 0:
                    self.assertEqual(event.run_number, self.event1.getRun())
                    self.assertEqual(event.event_number, self.event1.id())
                if i == 1:
                    self.assertEqual(event.run_number, self.event2.getRun())
                    self.assertEqual(event.event_number, self.event2.id())

    def tearDown(self):
        import shutil
        del self.content
#         print self.DATA_ROOT
        shutil.rmtree(self.DATA_ROOT)
