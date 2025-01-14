"""
    Clases reponsible to perform the iteration over the events and the
    event analysis
"""

from LHCOReader_HighPT.src.LHCOReader import read_LHCO
from LHCOReader_HighPT.src.EventInfo import Event
import copy
from typing import Tuple, Dict, List, Callable


class EventAnalysis:
    """
    Performs the analysis of a single event.
    It holds the information about the particle selections and the event selection Cuts.
    """

    def __init__(self, particle_selections: List[Callable], cuts: List[Callable]):
        """
        :param particle_selections:
            List of functions or callables that selects the particles for the analysis and returns an event
            with the selected particles
        :param cuts:
            List of functions that represent the selection Cuts. The function must return True if the
            event passed the cut and False otherwise.
        """
        self._particle_selections = particle_selections
        self._cuts = cuts

    def launch_analysis(self, event: Event) -> Tuple[bool, Event]:
        """
        Launches the analysis on the event.
        Returns a tuple, where the first item is a boolean that indicates wether the event must
        be selected or not, and the second the modified event due to the particle selections.
        """
        # Select the particles for the analysis
        for selection in self._particle_selections:
            # Updates the event with the particle selection
            event = selection(event)

        # Apply the Cuts
        passed_event = all(cut(event) for cut in self._cuts)

        return passed_event, event


class EventLoop:
    """
    Iterates over all the events in a .lhco file, applies the object selections, and
    selects the events that satisfy all the analysis Cuts.

    @TODO: implement histogram booking as well.

    Main method:
        def run (analysis: EventAnalysis): Launches the event analysis in all the events and
                                           returns the acceptance x efficiency
    """

    def __init__(self, lhco_reader=None):
        # Function responsible to read the events
        self._lhco_reader = lhco_reader if lhco_reader is not None else read_LHCO

    def analyse_events(self, lhco_file: str, event_analyses: Dict[str, EventAnalysis]):
        """Runs the analysis on the events from the file .lhco_file"""
        # Holds the number of event that passed all the Cuts in each analysis
        efficiencies = {analysis_name: 0 for analysis_name in event_analyses}
        # Counts the total number of events
        number_evts = 0

        print(f"Reading events from file: {lhco_file}")

        # Iterates over all the events
        for event in self._lhco_reader(lhco_file):
            if number_evts > 0 and number_evts % 10000 == 0:
                print(f"INFO: Reached {number_evts} events")
            # Launches the analyses
            for analysis_name, event_analysis in event_analyses.items():
                # Copy the event
                current_event = copy.deepcopy(event)
                # Checks if the event survived all the Cuts
                passed_cuts, _ = event_analysis.launch_analysis(event=current_event)
                # Updates the counter if the event passed all Cuts
                if passed_cuts:
                    efficiencies[analysis_name] += 1
                    # @TODO: Histogram booking
            number_evts += 1

        for analysis_name, survived_evts in efficiencies.items():
            print(f"{analysis_name}: {survived_evts}/{number_evts} events passed")

        # Divides by the total number of events to obtain the efficiencies
        efficiencies = {analysis_name: efficiencies[analysis_name] / number_evts for analysis_name in efficiencies}

        return efficiencies
