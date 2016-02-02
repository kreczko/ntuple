from random import gauss
from rootpy.io import root_open
from rootpy.tree import Tree, TreeChain
from rootpy.plotting import Hist
from rootpy import stl

# Make two files, each with a Tree called "test"

print "Creating test tree in chaintest1.root"
f = root_open("chaintest1.root", "recreate")

tree = Tree("test")
branches = {
     'x': 'F',
     'y': 'F',
     'z': 'F',
     'i': 'I',
     'vi': stl.vector('int')}
tree.create_branches(branches)

for i in xrange(10000):
    tree.x = gauss(.5, 1.)
    tree.y = gauss(.3, 2.)
    tree.z = gauss(13., 42.)
    tree.i = i
    for vi in range(4):
        tree.vi.push_back(vi**2)
    tree.fill()
    
    
tree.write()
f.close()