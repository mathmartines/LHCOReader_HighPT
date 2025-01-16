"""
    Defines all the cuts for the analysis of the atlas_ditau_13TEV channel.

    Experimental paper: https://arxiv.org/abs/2002.12223.

    If a cut function returns True, it means that the event passed the cut.
"""

from LHCOReader_HighPT.src.EventInfo import Event
import math


def leptons_veto(event: Event) -> bool:
    """Veto events with leptons."""
    return len(event.electrons + event.muons) == 0


def ditauhad_event(event: Event) -> bool:
    """
    - Event is required to have at least two hadronic taus;
    - Leading tau pt > 165 GeV;
    - Leading and subleading tau must have opposite charge
    - |Delta phi| > 2.7
    """
    # At least two taus
    if len(event.tauhads) < 2:
        return False

    # Leading tau pT cut
    if event.tauhads[0].pt < 165 or event.tauhads[1].pt < 65:
        return False

    # Opposite charge cut
    if event.tauhads[0].ntrk * event.tauhads[1].ntrk > 0:
        return False

    # Back to back in the transverse plane
    dphi = event.tauhads[0].phi - event.tauhads[1].phi
    if abs(dphi) > math.pi:
        dphi = dphi - 2 * math.pi if dphi > 0 else dphi + 2 * math.pi

    return abs(dphi) > 2.7


def btag_veto(event: Event) -> bool:
    """Veto events with b-tagged jets"""
    return not any([jet.btag for jet in event.jets])
