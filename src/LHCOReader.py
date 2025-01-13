from typing import List
from LHCOReader_HighPT.src.Event import Event


class LHCOReader:
    """Reads the .lhco file and returns a list with all the events in the file."""

    @staticmethod
    def read_events_generator(filename: str) -> List:
        """Yields one event at time."""
        # Holds all the events
        with open(filename) as lhco_file:
            event_particles = []

            # Searches the event information
            for line in lhco_file:
                # Strip whitespace and skip comments
                current_line = line.strip()
                if current_line.startswith("#"):
                    continue

                # Signal a new event
                if current_line.startswith("0"):
                    if event_particles:
                        yield Event(event_particles)
                    # Reset event for the next particles
                    event_particles = []

                else:
                    event_particles.append(current_line)

            # Add last event if it exists
            if event_particles:
                yield Event(event_particles)

    def read_event(self, filaname: str):
        """Returns a list with all the events."""
        return [event for event in self.read_events_generator(filaname)]


if __name__ == "__main__":
    reader = LHCOReader()
    events = reader.read_event("/Users/martines/Desktop/PhD/HighPT/atlas-ditau-13tev/RecastFR/m1000_delphes_events.lhco")
