"""
    Defines all the particle selections for the analysis of the atlas_ditau_13TEV channel.

    Experimental paper: https://arxiv.org/abs/2002.12223.
"""

from LHCOReader_HighPT.src.EventInfo import Event


def electron_candidates(event: Event) -> Event:
    """Electrons are required to have |eta| < 2.47 and not with in 1.37 < |eta| < 1.52."""
    # Select the electrons
    selected_electrons = [
        electron for electron in event.electrons if abs(electron.eta) < 1.37 or (1.52 < abs(electron.eta) < 2.47)
    ]

    # Removes all electrons
    event.remove_particles("electrons")

    # Adds only the selected electrons to the event
    event.extend(selected_electrons)

    return event


def muon_candidates(event: Event) -> Event:
    """Muons are required to have |eta| < 2.5."""
    # Muons that satisfy the requirement
    selected_muons = [muon for muon in event.muons if abs(muon.eta) < 2.5]

    # Removes all muons
    event.remove_particles("muons")

    # Adds the selected muons
    event.extend(selected_muons)

    return event


def jet_candidates(event: Event) -> Event:
    """Jets are required to have pT > 20 GeV and |eta| < 2.5"""
    selected_jets = [jet for jet in event.jets if jet.pt > 20 and abs(jet.eta) < 2.5]

    # Exclude all jets
    event.remove_particles("jets")

    # Adds the selected jets
    event.extend(selected_jets)

    return event


def hadtau_candidates(event: Event) -> Event:
    """
    Hadronic tau candidates must satisfy:
        - Tagged as a tau jet
        - charge equals +/- 1
        - 1 or 3 associated tracks
        - |eta| < 2.5 and not in 1.37 < |eta| < 1.52
        - pT > 65 GeV (only for the tauhad-tauhad channel)
    """
    # Stores the selected tau
    selected_taus = []

    for tau in event.tauhads:
        # Charge cut
        if abs(tau.ntrk) != 1:
            continue
        # Rapitity window
        if abs(tau.eta) >= 2.5 or (1.37 > abs(tau.eta) < 1.52):
            continue
        # pT cut
        if tau.pt < 65:
            continue
        selected_taus.append(tau)

    # Exclude all taus from the event
    event.remove_particles("tauhads")

    # Adds only the selected taus
    event.extend(selected_taus)

    return event
