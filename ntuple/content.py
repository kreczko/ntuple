'''
Created on 27 Jan 2016

@author: kreczko
'''

from rootpy.tree import Tree
from rootpy.io import root_open
from collections import Counter


def convert_type(ntuple_type, root_type):
    pass


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
        self._name = output_name
        self._type = vtype
        self._extract_function = extract_function
        self._help = help_doc

    def extract(self, event):
        return {self._name: self._extract_function(event)}

    @property
    def branch(self):
        return {self._name, self._type}


class NTupleCollection(object):
    '''
    classdocs
    '''

    def __init__(self, output_name, source, help_doc, variables=()):
        '''
        Constructor
        '''
        self._name = output_name
        self._source = source
        self._help = help_doc
        self._variables = NTupleCollection.prepend_name(self._name, variables)

    @staticmethod
    def prepend_name(col_name, variables):
        for var in variables:
            var._name = col_name + '.' + var._name
        return variables

    def extract(self, event):
        collection = self._source(event)
        result = []
        for c in collection:
            all_vars = {}
            for var in self._variables:
                all_vars.update(var.extract(c))
            result.append(all_vars)

        return result

    @property
    def branches(self):
        return 0


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
        self._file = root_open(output_file, 'recreate')
        self._tree = Tree(tree_name)

        self._variables = []

        self._counter = Counter()

        self._created_branches = False

    @property
    def branches(self):
        return 0

    def add_variable(self, variable):
        pass

    def add_collection(self, collection):
        pass

    def fill(self, event):
        self._counter['processed events'] += 1

        if not self._created_branches:
            self.__create_branches__()

    def __create_branches__(self):
        pass

    def save(self):
        self._tree.write()
        self._file.close()
