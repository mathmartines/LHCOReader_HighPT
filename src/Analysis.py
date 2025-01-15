"""Classes responsible for performing iteration over the events and event analysis"""

from LHCOReader_HighPT.src.LHCOReader import read_LHCO
from LHCOReader_HighPT.src.EventInfo import Event
import copy
from typing import Tuple, Dict, List, Callable


class EventAnalysis:
    """
    Performs the analysis of a single event.
    Holds information about particle selections and event selection cuts.
    """

    def __init__(self, particle_selections: List[Callable], cuts: List[Callable]):
        """
        :param particle_selections:
            A list of functions or callables that define the particle requirements for the analysis.
            Particles that do not satisfy a requirement are removed from the event by the corresponding function.
            The functions must return an Event object excluding particles that do not satisfy the requirements.
        :param cuts:
            List of functions that represent the selection cuts.
            Each function must return True if the event passes the cut and False otherwise.
        """
        self._particle_selections = particle_selections
        self._cuts = cuts

    def launch_analysis(self, event: Event) -> Tuple[bool, Event]:
        """
        Launches the analysis on the event.
        Returns a tuple, where the first item is a boolean indicating whether the event should be selected,
        and the second is the modified event after all the particle selections.
        This is done in case the modified event is needed by the EventLoop object for histogram booking.
        """
        # Selects the particles for the analysis
        for selection in self._particle_selections:
            # Updates the event with the particle selection
            event = selection(event)
        # Applies the event selection cuts
        passed_event = all(cut(event) for cut in self._cuts)
        # Returns the boolean and the modified event
        return passed_event, event


class EventLoop:
    """
    Iterates over all the events in a .lhco file, calculates the acceptance x efficiencies,
    and manages the histogram booking with the selected events.

    @TODO: implement histogram booking.
    """

    def __init__(self, lhco_reader=None):
        # Function responsible to read the events
        self._lhco_reader = lhco_reader if lhco_reader is not None else read_LHCO

    def analyse_events(self, lhco_file: str, event_analyses: Dict[str, EventAnalysis]):
        """
        Runs the analysis on the events from the .lhco and returns a dictionary
        holding the efficiency value for each analysis.

        :param lhco_file: path to the .lhco file.
        :param event_analyses: dictionary with all the analysis that must be performed.
        """
        # Holds the number of event that passed all the cuts in each analysis
        efficiencies = {analysis_name: 0 for analysis_name in event_analyses}
        # Counts the total number of events
        number_evts = 0

        print(f"Reading events from file: {lhco_file}")

        # Iterates over all the events
        for event in self._lhco_reader(lhco_file):
            if number_evts > 0 and number_evts % 10000 == 0:
                print(f"INFO: Reached {number_evts} events")
            # Launch the analyses
            for analysis_name, event_analysis in event_analyses.items():
                # Copy the event (original event must remain the same for all analysis)
                current_event = copy.deepcopy(event)
                # Checks if the event survived all the cuts and updates the counter
                passed_cuts, _ = event_analysis.launch_analysis(event=current_event)
                if passed_cuts:
                    efficiencies[analysis_name] += 1
                    # @TODO: Histogram booking

            number_evts += 1

        for analysis_name, survived_evts in efficiencies.items():
            print(f"{analysis_name}: {survived_evts}/{number_evts} events passed")

        # Divide by the total number of events to obtain the efficiencies
        efficiencies = {analysis_name: efficiencies[analysis_name] / number_evts for analysis_name in efficiencies}

        return efficiencies
