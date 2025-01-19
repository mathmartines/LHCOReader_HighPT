"""
    Simple classes to represent the event information:
    - Particle:
        Information can be extracted as simple attrs
    - Event:
        Behaves like a Python list of particles.
        Specific particles can be extracted using as attrs, e.g. event.electrons
"""

from collections import UserList
from typing import List
import copy


class Particle:
    """
    Holds information about the particle.
    The particle's information can be accessed as attributes.

    Example: particle.pt, particle.phi, etc.
    """
    # Information avalilable about the particle
    _particle_info_attrs = "typ eta phi pt jmas ntrk btag had/em dum1 dum2".split()

    def __init__(self, particle_info: str):
        """The particle_info param represents one line from the .lhco file with only the information on
        _particle_info_attrs"""
        self.__dict__ = {
            info: float(info_value) for info_value, info in zip(particle_info.split(), self._particle_info_attrs)
        }

    def __getattr__(self, info):
        """
        Handles the acess of the particle infos.
        Note: had/em ratio must be acess as had_em
        """
        if info == "had_em":
            return self.__getattribute__("had/em")
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{info}'")

    def __repr__(self):
        """For nice printing"""
        display_info = [f"{info}:{self.__dict__[info]}" for info in "typ eta phi pt jmas ntrk btag".split()]
        return "Particle(" + ", ".join(display_info) + ")"

    def __copy__(self):
        """Returns a copy of the object."""
        return self.__class__(" ".join([f"{self.__dict__[info]}" for info in self._particle_info_attrs]))


class Event(UserList):
    """Stores all the particles that belong to an event. Behaves like a usual python list."""

    # Particles types
    particles_type = {
        "photons": 0, "electrons": 1, "muons": 2, "tauhads": 3, "jets": 4, "met": 6
    }

    def __init__(self, list_particle: List[Particle]):
        # List with particles sorted by pT
        super().__init__(self._sort_by_pt(list_particle))

    @classmethod
    def from_str_particles_info(cls, list_particles_info: List[str]):
        """
        Each entry of list_particles_info stores the information about a particle in the same way as in the .lhco
        file, but without the firt character (contains no information about the particle).
        """
        return cls([Particle(particle_info) for particle_info in list_particles_info])

    def __getattr__(self, part_type: str):
        """Returns only the particles of a given type."""
        if part_type not in self.particles_type:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{part_type}'")
        # Ensures that particles are sorted by pT
        return self._sort_by_pt([particle for particle in self.data if particle.typ == self.particles_type[part_type]])

    @staticmethod
    def _sort_by_pt(part_list: List[Particle]):
        return sorted(part_list, key=lambda particle: particle.pt, reverse=True)

    def __deepcopy__(self, memodict=None):
        """
        Returns a copy of the object.
        It needs to be deepcopy because the Event class holds references to Particle objects.
        A simple copy of the Event class would still have the same references as the original object.
        """
        if memodict is None:
            memodict = {}
        # Creates a copy of all the particles
        particles = [copy.copy(particle) for particle in self.data]
        # Returns a copy of event
        return self.__class__(particles)

    def remove_particles(self, parts_type: str):
        """Removes the particles of a given type."""
        if parts_type in self.particles_type:
            self.data = [particle for particle in self.data if particle.typ != self.particles_type[parts_type]]
