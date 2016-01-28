# ntuple
Python package for ntuple production

## What is an n-tuple?
In its broad sense an n-tuple is a sequence (or ordered list) of n elements, where n is a non-negative integer (see [Wikipedia](https://en.wikipedia.org/wiki/Tuple)).
In the case of High Energy Particle Physics (HEP) an n-tuple is considered a 'flat' [TTree](https://root.cern.ch/doc/master/classTTree.html) as defined by the [ROOT framework](https://root.cern.ch/). This is an ordered list of elements (we call them events), where each event property is defined as a 'leaf':
```
tree
	- property1
	- property2
	...
```
In an n-tuple the properties are either basic types (and string) or sequences of them (e.g. `vector<int>`).
From a programming perspective, the Tree behaves much like a list of [Python's namedtuple](https://docs.python.org/2/library/collections.html#collections.namedtuple):
```
for event in tree:
    print event.property1
    for e in event.collection1:
    	print e.pt()
```

## What can I do with this package.
The main goal of this package is to translate a TTree with C++ object elements into a TTree with basic types (or sequences of them).
This module provides three components to implement that goal:
 - n-tuple map: a simple way to map functions and properties of C++ objects in a TTree to simple types
 - converter for input files and their content
 - a summary component for bookkeeping
 

# The n-tuple map
The n-tuple map relies on the three classes `NTupleContent`, `NTupleVariable` and `NTupleCollection`.
`NTupleContent` is a container that represents the final content of your n-tuple and constists of one or more `NTupleVariable`/`NTupleCollection`.
`NTupleVariable` defines a simple 1:1 mapping between original content for basic types and string. The `NTupleCollection` constists of one or more `NTupleVariable` and maps a vector of objects onto vectors of basic types (n:m mapping, where n can be equal to m).

For clarification an example is provided:

```python
n = NTupleContent(tree_name = 'events', output_file = 'ntuple.root')
isRealData = NTupleVariable = (output_name = "isRealData", 
					   vtype = 'bool', extract_function = lambda event: event.isRealData(), help_doc = 'Maps event.isRealData() to event.isRealData')
# this will produce the vectors electron.pt, electron.eta and electron.charge
electrons = NTupleCollection('electron', source = 'slimmedElectrons', 
							help_doc = 'maps event.slimmedElectrons.<> onto event.electron.<> where <> mappings are defined by added NTupleVariables',
							variables = [
							NTupleVariable = ("pt", vtype = 'float', extract_function = lambda e: e.pt(), help_doc = 'electron transverse momentum (pt)'),
					   		NTupleVariable = ("eta", vtype = 'float', extract_function = lambda e: e.eta(), help_doc = 'electron pseudorapidity'),
					   		NTupleVariable = ("charge", vtype = 'int', extract_function = lambda e: e.charge(), help_doc = 'electron charge'),
							]
							)
n.add_variable(isRealData)
n.add_collection(electrons)
```


### Converters
Converters are meant to normalise the input to the ntuple component. The following is an example of the CMS software (CMSSW) converter.

The `CMSSWConverter` is a wrapper for the n-tuple component which maps
 - file input using `edmFileUtil` which will translate a global path, i.e. a path starting with `/store` into a local path (`file://`) if the file is available at the local storage element or into a remote file path (`root://`) if it is not. Paths on the local file system are not changed
 - `event._event.getRun()` to `event.getRun()` (also `isRealData`, `bunchCrossing`, `luminosityBlock`, `orbitNumber`, `time`)
 - `handle  = Handle ('std::vector<pat::Muon>');label = ("slimmedMuons");event.getByLabel (label, handle);muons = handle.product()` to `event.slimmedMuons`
 
 In a full example (taking the NTupleContent definition from the previous section) is shown below:
 ```python
 events = CMSSWConverter(file_to_process)
 events.prepare_sources(n.get_sources())
 map(n.fill, events)
 # write new tree to file
 n.save()
 
 # summary over
 summary = n.summary()
 summary.extend(events.summary())
 summary.save()
 ```

 
 