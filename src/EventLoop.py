"""Class responsible to iterate over the events in a single .lhco file"""


class EventLoop:
    """
    Iterates over all the events in a .lhco file, applies the object selections, and
    selects the events that satisfy all the analysis cuts.

    @TODO: implement histogram booking as well.

    Main method:
        def run (analysis: EventAnalysis): Launches the event analysis in all the events and
                                           returns the acceptance x efficiency
    """

    def __init__(self, lhco_reader):
        self._lhco_reader = lhco_reader     # reads the events
        self._event_data = None             # stores the information required for the event analysis
        self._lhe_filname = None            # path to the .lhe file
        self._events = []                   # stores the events

    @property
    def lhe_file(self):
        """Returns the .lhe file path"""
        return self._lhe_filname

    @lhe_file.setter
    def lhe_file(self, filename: str):
        """Reads the .lhe file."""
        # Verifies that the file is open and call the lhco reader to read the event
        pass


