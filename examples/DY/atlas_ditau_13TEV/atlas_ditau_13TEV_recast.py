"""
    Analyses for the channel atlas_ditau_13TEV.
    Experimental paper: https://arxiv.org/abs/2002.12223.

    The analysis is launched on the simulations for the heavy higgs production via gluon fusion.
    The calculated efficiencies are stored into a .json file.
"""

from LHCOReader_HighPT.src.Analysis import EventLoop
from LHCOReader_HighPT.examples.DY.atlas_ditau_13TEV import atlas_ditau_13TEV_analyses
import json


if __name__ == "__main__":
    # Path to the folder where the .lhco files are stores
    folder_path = "/Users/martines/Dropbox/HighPT-Data/atlas-ditau-13TEV/recast/lhco_files"

    # Masses of the heavy mediator
    heavy_scalar_masses = [200, 300, 400, 600, 1000, 1500, 2000, 2500]

    # Analysis to run on the files
    event_analyses = {
        "atlas-ditauhad-bveto": atlas_ditau_13TEV_analyses.atlas_ditauhad_bveto()
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
        efficiencies[heavy_scalar_mass], _ = event_loop.analyse_events(
            lhco_file=lhco_file, event_analyses=event_analyses
        )

    # Saves the json file
    with open(f"{folder_path}/eff_LHCOReader_HighPT.json", "w") as file_:
        json.dump(efficiencies, file_, indent=4)
