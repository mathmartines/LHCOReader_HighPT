"""Builder functions for all the event analyses for the different channels."""

from LHCOReader_HighPT.examples.DY.atlas_ditau_13TEV.ParticleSelections import (electron_candidates, muon_candidates,
                                                                                jet_candidates, hadtau_candidates)
from LHCOReader_HighPT.examples.DY.atlas_ditau_13TEV.Cuts import leptons_veto, ditauhad_event, btag_veto
from LHCOReader_HighPT.src.Analysis import EventAnalysis
from LHCOReader_HighPT.src.EventInfo import Event
import numpy as np


def transverse_mass(event: Event) -> float:
    """Calculates the transverse mass observable for the event."""
    # Taus (leading and subleading only)
    taus = event.tauhads[:2]
    # Missing energy
    met = event.met
    # Total transverse pT
    pt_total = np.sum([particle.pt for particle in taus + met])

    # Momentum in the x and y-directions
    px_total = np.sum([particle.pt * np.cos(particle.phi) for particle in taus + met])
    py_total = np.sum([particle.pt * np.sin(particle.phi) for particle in taus + met])

    # Total transverse momentum
    return np.sqrt(np.power(pt_total, 2) - np.power(px_total, 2) - np.power(py_total, 2))


def atlas_ditauhad_bveto():
    """Builds the analysis for the ditau-had b-veto channel"""
    # All the particle selections for the analysis
    particle_selections = [
        electron_candidates,  # Selects the electron candidates
        muon_candidates,  # Selects the muon candidates
        jet_candidates,  # Selects the jets
        hadtau_candidates  # Selects the hadronic tau candidates
    ]
    # All cuts for the analysis
    selection_cuts = [
        leptons_veto,  # Veto events with leptons
        ditauhad_event,  # Selects events for the ditau-had channel
        btag_veto  # Veto events with b-tagged jets
    ]
    # Builds the EventAnalysis object
    return EventAnalysis(particle_selections=particle_selections, cuts=selection_cuts)
