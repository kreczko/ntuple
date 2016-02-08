from random import gauss
from rootpy.io import root_open
from rootpy.tree import Tree, TreeModel, FloatCol, IntCol
from rootpy.tree.model import TreeModelMeta
from rootpy import stl
from rootpy.vector import LorentzVector
from rootpy.tree.treetypes import FloatArrayCol, IntArrayCol
import tempfile

class Event(TreeModel):
    # properties of particle "a"
    a_x = FloatCol()
    a_y = FloatCol()
    a_z = FloatCol()
    # properties of particle "b"
    b_x = FloatCol()
    b_y = FloatCol()
    b_z = FloatCol()
    # a collection of particles
    col_x = stl.vector("float")
    col_y = stl.vector("float")
    col_z = stl.vector("float")
    col_n = IntCol()
    # a TLorentzVector
    p = LorentzVector
    i = IntCol()
# Make two files, each with a Tree called "test"

print "Creating test tree in chaintest1.root"
tmp_dir = tempfile.mkdtemp()
f = root_open(tmp_dir+ "/chaintest1.root", "recreate")


branches = {
    'x': FloatCol(),
    'y': FloatCol(),
    'z': FloatCol(),
    'i': FloatCol(),
    'vi': stl.vector('float'),
    'vx': FloatArrayCol(4),
    'vy': stl.vector('float'),}
# print branches
MyTreeModel = TreeModelMeta('MyTreeModel', (TreeModel,), branches)
tree = Tree("test", model=MyTreeModel)
# tree.create_branches(branches)

for i in xrange(10000):
    tree.x = gauss(.5, 1.)
    tree.y = gauss(.3, 2.)
    tree.z = gauss(13., 42.)
    tree.i = i
    for vi in range(4):
        tree.vi.push_back(vi**2)
        tree.vy.push_back(vi**3)
        tree.vx[vi] = vi**2
    tree.fill(reset=True)


tree.write()
f.close()
# from random import randint
# tree = Tree("test", model=Event)
#
# # fill the tree
# for i in xrange(10):
#     tree.a_x = gauss(.5, 1.)
#     tree.a_y = gauss(.3, 2.)
#     tree.a_z = gauss(13., 42.)
#
#     tree.b_x = gauss(.5, 1.)
#     tree.b_y = gauss(.3, 2.)
#     tree.b_z = gauss(13., 42.)
#
#     n = randint(1, 10)
#     for j in xrange(n):
#         tree.col_x.push_back(gauss(.5, 1.))
#         tree.col_y.push_back(gauss(.3, 2.))
#         tree.col_z.push_back(gauss(13., 42.))
#     tree.col_n = n
#
#     tree.p.SetPtEtaPhiM(gauss(.5, 1.),
#                         gauss(.5, 1.),
#                         gauss(.5, 1.),
#                         gauss(.5, 1.))
#
#     tree.i = i
#     tree.fill(reset=True)
# tree.write()
#
# f.close()
