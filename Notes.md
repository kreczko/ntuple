# Dev Notes

 - CMSSW FWLite with MiniAOD: https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD2015
 - cppyy bug: if you import `unicode_literals` the use of cppyy (or rootpy.stl in layer above) will fail
 - rootpy.Tree: `__setitem__` sets the actual buffer while `__setattr__` just changes its value. This is an important distinction since the objects used as buffer are special, but their values are basic types