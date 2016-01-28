'''
Created on 27 Jan 2016

@author: kreczko
'''

from rootpy.tree import Tree
from rootpy.io import root_open
from collections import Counter


class NTupleVariable(object):
    '''
    Class for mapping a TTree branch to a value

    Example:
        isRealData = NTupleVariable = (
                output_name = "isRealData",
                vtype = 'bool',
                extract_function = lambda event: event.isRealData(),
                help_doc = 'Maps event.isRealData() to event.isRealData')
    '''

    def __init__(self, output_name, vtype, extract_function,
                 help_doc='I am helping'):
        '''
        Constructor
        '''
        self._extract_function = extract_function

    def extract(self, event):
        return self._extract_function(event)


class NTupleCollection(object):
    '''
    classdocs
    '''

    def __init__(self, output_name, source, help_doc, variables=()):
        '''
        Constructor
        '''


class NTupleContent(object):
    '''
    classdocs
    '''

    def __init__(self, tree_name, output_file):
        '''
        Constructor
        '''
        self._tree_name = tree_name
        self._output_file = output_file
        self._file = root_open(output_file)
        self._tree = Tree(tree_name)

        self._variables = []

        self._counter = Counter()

    def add_variable(self, variable):
        pass

    def add_collection(self, collection):
        pass

    def fill(self, event):
        self._counter['processed events'] += 1

    def save(self):
        self._tree.write()
        self._file.close()
