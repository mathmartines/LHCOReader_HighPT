"""
    Analyses for the channel atlas_ditau_13TEV.
    Experimental paper: https://arxiv.org/abs/2002.12223.

    File is used to obtain the SMEFT predictions
    The calculated efficiencies are stored into a .json file.
"""
from LHCOReader_HighPT.src.Utilities import read_xsection
from LHCOReader_HighPT.src.Analysis import EventLoop
from LHCOReader_HighPT.src.Histogram import ObservableHistogram
from LHCOReader_HighPT.examples.DY.atlas_ditau_13TEV import atlas_ditau_13TEV_analyses
import json
import copy


if __name__ == "__main__":
    # Folder where the .lhco and .lhe files are store
    folder_path = "/home/martines/work/MG5_aMC_v3_1_1/PhD/High-PT/atlas-ditau-13TEV-efficiencies"

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

    # Form-factors we need to analyse
    form_factors = [
        "FVLL_00_bb_tata_A_Reg",
        "FVLL_00_bb_tata_Z_Reg",
        "FVLL_00_bb_tata_Reg_Reg"
    ]
    form_factor_predictions = {}    # Stores the predictions for the form-factors

    # SMEFT predictions in terms of the form factors
    smeft_map = {
        "C1lq3333": [("FVLL_00_bb_tata_A_Reg", 1), ("FVLL_00_bb_tata_Z_Reg", 1)],
        "C3lq3333": [("FVLL_00_bb_tata_A_Reg", 1), ("FVLL_00_bb_tata_Z_Reg", 1)],
        "C1lq3333-C1lq3333": [("FVLL_00_bb_tata_Reg_Reg", 1)],
        "C3lq3333-C3lq3333": [("FVLL_00_bb_tata_Reg_Reg", 1)],
        "C1lq3333-C3lq3333": [("FVLL_00_bb_tata_Reg_Reg", 2)]
    }
    smeft_predictions = {}         # Stores the predictions for the SMEFT terms

    # Iterates over the form-factor
    for form_factor in form_factors:

        # Creates the histogram to store the predictions for the current form-factor
        form_factor_hist = copy.copy(transverse_mass_hist)

        # For each different simulation bin
        for bin_index in range(1, len(bin_edges)):
            lhco_filename = f"{folder_path}/lhco_files/{form_factor}-bin-{bin_index}.lhco"
            lhe_filename = f"{folder_path}/lhe_files/{form_factor}-bin-{bin_index}.lhe"

            # Run the analysis over all the events
            _, nevents = event_loop.analyse_events(lhco_file=lhco_filename, event_analyses=event_analyses)

            # Computes the prediction
            cross_section = read_xsection(lhe_filename)
            current_hist = event_loop.retrive_histogram("atlas-ditauhad-bveto")
            print(current_hist)
            # Updates the prediction
            weight = 2 * cross_section / nevents   # 2 because I'm simulating only b b~ > ta+ ta-
            form_factor_hist += current_hist * weight * 139 * 1000

        form_factor_predictions[form_factor] = form_factor_hist

    # Creates the SMEFT predictions out of the form factors
    for smeft_term in smeft_map:
        smeft_predictions[smeft_term] = copy.copy(transverse_mass_hist)
        for (form_factor, coef) in smeft_map[smeft_term]:
            smeft_predictions[smeft_term] += coef * form_factor_predictions[form_factor]
        # .json files only accept python lists
        smeft_predictions[smeft_term] = smeft_predictions[smeft_term].tolist()

    # Saves the .json file
    with open(f"{folder_path}/SMEFT/atlas-ditau-13TEV.json", "w") as file_:
        json.dump(smeft_predictions, file_, indent=4)

