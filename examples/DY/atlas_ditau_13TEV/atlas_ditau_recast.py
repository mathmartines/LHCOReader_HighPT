"""
    Analyses for the channel atlas_ditau_13TEV.
    Experimental paper: https://arxiv.org/abs/2002.12223.

    The analysis is launched on the simulations for the heavy higgs production via gluon fusion.
    The calculated efficiencies are stored into a .json file.
"""

from LHCOReader_HighPT.src.Analysis import EventAnalysis, EventLoop
from LHCOReader_HighPT.examples.DY.atlas_ditau_13TEV.ParticleSelections import (electron_candidates, muon_candidates,
                                                                                jet_candidates, hadtau_candidates)
from LHCOReader_HighPT.examples.DY.atlas_ditau_13TEV.Cuts import leptons_veto, ditauhad_event, btag_veto


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


if __name__ == "__main__":
    # Path to the folder where the .lhco files are stores
    folder_path = "/Users/martines/Dropbox/HighPT-Data/atlas-ditau-13TEV/recast/lhco_files"

    # Masses of the heavy mediator
    heavy_scalar_masses = [200, 300, 400, 600, 1000, 1500, 2000, 2500]

    # Analysis to run on the files
    event_analyses = {
        "atlas-ditauhad-bveto": atlas_ditauhad_bveto()
        # @TODO: include the other analyses as well
    }

    # Dictionary to store the efficiencies
    efficiencies = {}

    # Responsible to iterate over the events in the file
    event_loop = EventLoop()

    # Launches the event loop in each .lhco file
    for heavy_scalar_mass in heavy_scalar_masses:
        lhco_file = f"{folder_path}/atlas-ditau-13TEV-m{heavy_scalar_mass}.lhco"
        # Computes the efficiencies
        efficiencies[heavy_scalar_mass] = event_loop.analyse_events(
            lhco_file=lhco_file, event_analyses=event_analyses
        )
