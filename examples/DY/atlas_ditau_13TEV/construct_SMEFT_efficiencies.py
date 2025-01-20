"""Computes the efficiency matrices for the atlas-ditau-13TEV channel."""

from LHCOReader_HighPT.src.Analysis import EventLoop
from LHCOReader_HighPT.src.Histogram import ObservableHistogram
from LHCOReader_HighPT.src.Utilities import read_xsection
from LHCOReader_HighPT.src.EfficiencyMatrixBuilder import EfficiencyFileBuilder
from LHCOReader_HighPT.examples.DY.atlas_ditau_13TEV import atlas_ditau_13TEV_analyses
import numpy as np

if __name__ == "__main__":
    # Folder where the .lhco files are store
    folder_path = "/home/martines/work/MG5_aMC_v3_1_1/PhD/High-PT/atlas-ditau-13TEV-efficiencies"

    # Form-factors names and properties
    form_factors = [
        "FVLL_00_bb_tata_A_Reg",
        "FVLL_00_bb_tata_Z_Reg",
        "FVLL_00_bb_tata_Reg_Reg"
    ]
    form_factors_xy = {
        "FVLL_00_bb_tata_A_Reg": "LL LR RL RR",
        "FVLL_00_bb_tata_Z_Reg": "LL RR",
        "FVLL_00_bb_tata_Reg_Reg": "LL RR"
    }
    form_factors_term_type = {
        "FVLL_00_bb_tata_A_Reg": "A*Reg",
        "FVLL_00_bb_tata_Z_Reg": "Z*Reg",
        "FVLL_00_bb_tata_Reg_Reg": "Reg*Reg"
    }

    # Bin edges for the mTtot distribution (and the ones that defined the parton level mtt bins)
    bin_edges = [150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1150, 15000]

    # Histogram for the observable value mTtot
    transverse_mass_hist = ObservableHistogram(
        bin_edges=bin_edges, observable=atlas_ditau_13TEV_analyses.transverse_mass
    )

    # Analysis to run on the files
    event_analyses = {
        "atlas-ditauhad-bveto": atlas_ditau_13TEV_analyses.atlas_ditauhad_bveto()
    }

    # Responsible to iterate over the events in one .lhco file and construct the histogram using
    # the transverse_mass_hist as a template
    event_loop = EventLoop(histogram=transverse_mass_hist)

    # Constructs the efficiency file
    eff_file_builder = EfficiencyFileBuilder()
    # Same properties for all the files
    eff_file_builder.Experiment = "ATLAS"
    eff_file_builder.Search = "2002_12223"
    eff_file_builder.llbar = "tata"
    eff_file_builder.Nevs = "50000"
    eff_file_builder.bin_edges = bin_edges
    eff_file_builder.FF = "vector"
    eff_file_builder.coef = "0 0"

    # Iterates over the form-factor
    for form_factor in form_factors:

        # Stores the cross-sections for each bin
        cross_sections = np.empty(shape=len(bin_edges) - 1)
        # Stores the efficiency matrix
        efficiency_matrix = np.empty(shape=(len(bin_edges) - 1, len(bin_edges) - 1))

        # Initial quarks of the file
        _, _, initial_quarks, *_ = form_factor.split("_")
        eff_file_builder.qqbar = f"{initial_quarks}~"
        # Other infos to add to the file
        eff_file_builder.XY = form_factors_xy[form_factor]
        eff_file_builder.type = form_factors_term_type[form_factor]

        # For each different simulation bin
        for bin_index in range(1, len(bin_edges)):
            lhco_filename = f"{folder_path}/lhco_files/{form_factor}-bin-{bin_index}.lhco"
            lhe_filename = f"{folder_path}/lhe_files/{form_factor}-bin-{bin_index}.lhe"

            # Run the analysis over all the events
            _, nevents = event_loop.analyse_events(lhco_file=lhco_filename, event_analyses=event_analyses)

            # Updates the efficiency matrix and the cross-section arrays
            iarr = bin_index - 1
            efficiency_matrix[iarr] = event_loop.retrive_histogram("atlas-ditauhad-bveto").view(np.ndarray) / nevents
            cross_sections[iarr] = read_xsection(lhe_filename)

        # Sets the efficiency matrix and the cross-sections
        eff_file_builder.kernel = efficiency_matrix
        eff_file_builder.xsections = 2 * cross_sections * 1000

        # Saves the file
        with open(f"{folder_path}/SMEFT/{form_factor}.dat", "w") as file:
            file.write(eff_file_builder.build_file())
