from collections import namedtuple
Electron = namedtuple('Electron', ['pt', 'hadronicOverEm'])


class Event(object):

    def __init__(self, run_number, event_number, electrons=()):
        self._electrons = electrons
        self._run_number = run_number
        self._event_number = event_number

    def getRun(self):
        return self._run_number

    def id(self):
        return self._event_number

    @property
    def electrons(self):
        return self._electrons

    def nice_electrons(self):
        """
            same as 'Event.electrons' but accessed via a function
        """
        return self._electrons


class CMSSWEvent(object):
    """
    Emulates a CMSSW event
    event number -> event._event.id().event()
    run number -> event._event.getRun()
    muons -> handle  = Handle ('std::vector<pat::Muon>')
             label = ("slimmedMuons");
             event.getByLabel (label, handle)
             muons = handle.product()
    """

    def __init__(self):
        pass
