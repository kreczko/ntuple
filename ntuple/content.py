'''
Created on 27 Jan 2016

@author: kreczko
'''

from rootpy.tree import Tree
from rootpy.io import root_open
from collections import Counter
from rootpy.tree.treetypes import IntCol, UIntCol, BoolCol, FloatCol
from rootpy  import stl
from rootpy.tree.model import TreeModelMeta, TreeModel

__type_map__ = {
    'int': IntCol,
    'uint': UIntCol,
    'bool': BoolCol,
    'float': FloatCol,
    'vec:int': stl.vector,
    'vec:uint': stl.vector,
    'vec:bool': stl.vector,
    'vec:float': stl.vector,
}


def convert_type(ntuple_type):
    '''
        converts an NTuple type ('int', 'uint', 'float', 'vec:int', etc)
        into the equivalent ROOT type
    '''
    try:
        root_type = __type_map__.get(ntuple_type)
        if 'vec' in ntuple_type:
            basic_type = ntuple_type.split(':')[-1]
            return root_type(basic_type)
        else:
            return root_type()
    except KeyError:
        # @TODO: change this into logger
        print('Unknown ntuple type "{}"'.format(ntuple_type))

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
        return {self._name: self._type}


class NTupleCollection(object):
    '''
    classdocs
    '''

    def __init__(self, output_name, source, help_doc, variables=[]):
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
            var._type = 'vec:' + var._type
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
        b = {}

        for variable in self._variables:
            b.update(dict(variable.branch))
        return b

    @property
    def variables(self):
        return self._variables


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
        self._tree = None

        self._variables = []
        self._collections = []

        self._counter = Counter()

        self._created_branches = False
        self._branches = {}
        self._model = None

    @property
    def branches(self):
        return self._branches

    def __add__branches__(self, branches):
        for name, b_type in branches.items():
            if name in self._branches:
                raise ValueError(
                    'Branch with name="{}" already exists!'.format(name))
            else:
                self._branches[name] = convert_type(b_type)
                print name, self._branches[name]

    def add_variable(self, variable):
        if isinstance(variable, NTupleVariable):
            self._variables.append(variable)
            self.__add__branches__(variable.branch)
        else:
            raise ValueError(
                'Cannot add variable that is not of type NTupleVariable')

    def add_collection(self, collection):
        if isinstance(collection, NTupleCollection):
            self._collections.append(collection)
#             self.__add__branches__(collection.branches)
            for variable in collection.variables:
                self.add_variable(variable)
        else:
            raise ValueError(
                'Cannot add collection that is not of type NTupleCollection')

    def fill(self, event):
        self._counter['processed events'] += 1

        if not self._created_branches:
            self.__create_branches__()
#         self._tree.fill(reset=True)

    def __create_branches__(self):
        self._model = TreeModelMeta('MyTreeModel', (TreeModel,), self._branches)
        self._tree = Tree(self._tree_name, model=self._model)
        self._created_branches = True

    def save(self):
        self._tree.write()
        self._file.close()
