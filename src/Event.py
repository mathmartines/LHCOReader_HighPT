
from collections import UserList
from typing import List


class Particle:
    """
    Holds the information about the particle.
    The information about the particle is access as attributes.
    Example:
        particle.pt, particle.phi, etc
    """
    # Information avalilable about the particle
    _particle_info_attrs = "typ eta phi pt jmas ntrk btag had/em dum1 dum2".split()

    def __init__(self, particle_info: str):
        """
        Constructor of a particle object.
        The particle_info represents one line from the .lhco file
        """
        self.__dict__ = {
            info: float(info_value) for info_value, info in zip(particle_info.split()[1:], self._particle_info_attrs)
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
        display_info = [f"{info}:{self.__dict__[info]}" for info in "typ eta phi pt jmas ntrk btag".split()]
        return "Particle(" + ", ".join(display_info) + ")"


class Event(UserList):
    """
    Stores all the particles that belong to the event.
    It behaves like a usual python list.
    """

    # Particles types
    _particles_type = {
        "photons": 0, "electrons": 1, "muons": 2, "tauhads": 3, "jets": 4, "met": 6
    }

    def __init__(self, list_particles_info: List[str]):
        """
        Each entry of list_particles_info stores the information about a particle in the same way as in the .lhco
        file.
        """
        super().__init__([Particle(particle_info) for particle_info in list_particles_info])

    def __getattr__(self, particles_type: str):
        """Returns only the particles of a given type"""
        return [particle for particle in self if particle.typ == self._particles_type[particles_type]]


