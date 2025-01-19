"""Interface to construct a binning histogram."""

from abc import ABC, abstractmethod
import numpy as np
from LHCOReader_HighPT.src.EventInfo import Event
from typing import List, Callable


class Histogram(ABC):
    """Defines the interface for a histogram class."""

    @abstractmethod
    def update_hist(self, event: Event):
        """Updates the histogram with a given Event."""
        raise RuntimeError("Trying to use a method from a abstract class.")

    @abstractmethod
    def __copy__(self):
        """Clones an empty histogram"""
        pass


class ObservableHistogram(Histogram, np.ndarray):
    """
    One-dimensional histogram for a given observable.
    It behaves like a numpy array.
    The histogram is updated by the method:

    def update_hist (event)

    where it takes a single event as the argument.
    """

    def __new__(cls, bin_edges: List[float], observable: Callable):
        """
        The two necessary parameters for the construction are

        :param bin_edges: respective bin-edges for the histogram.
        :param observable: function or Callable object that can compute
                           the observable for a single Event object.
        """
        # Creates an empty histogram
        hist = np.zeros(shape=len(bin_edges) - 1).view(cls)
        # Stores the bin_edges and observalble as attrs
        hist.bin_edges = bin_edges
        hist.observable = observable
        # Returns the histogram
        return hist

    def __array_finalize__(self, hist):
        if hist is None:
            return
        # Adds the infos
        self.observable = getattr(hist, "observable", None)
        self.bin_edges = getattr(hist, 'bin_edges', None)

    def update_hist(self, event: Event):
        """Updates the histogram using the Event object."""
        # Calculates the observable
        obs_value = self.observable(event)
        # Finds the bin index
        bin_index = self._find_bin_index(observable_value=obs_value)
        # Updates the histogram if the observable is inside the histogram limits
        if 0 <= bin_index < len(self):
            self[bin_index] += 1

    def __copy__(self):
        """Shallow coppy of the current histogram."""
        return self.__new__(self.__class__, bin_edges=self.bin_edges, observable=self.observable)

    def _find_bin_index(self, observable_value: float) -> int:
        """Finds the respective bin index for the given value of the observable."""
        # Looks for the right bin number
        for bin_index in range(len(self.data)):
            if self.bin_edges[bin_index] <= observable_value < self.bin_edges[bin_index + 1]:
                return bin_index
        return -1
