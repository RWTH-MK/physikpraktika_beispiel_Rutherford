import numpy as np
from uncertainties import unumpy as unp
"""Nützlich,  wenn alle Werte einer Reihe den gleichen Fehler aufweisen. Konstruiert vollständige ufloat-Arrays.
"""

def relativer_fehler(daten, prozent):
    """Wenn alle Messwerte die gleiche prozentuale Abweichung haben

    Parameters
    ----------
    daten : [float, integer]
        Liste oder Array von Messdaten
    prozent : float, integer
        Der prozentuale Fehler. Wenn 1% gilt, dann 1 übergeben. Bei 0,2% -> 0.2

    Returns
    -------
    uarray
        Komposition aus Daten und Fehler
    """
    return unp.uarray(daten, np.array(daten)/100*prozent)


def absoluter_fehler(daten, sigma):
    """Wenn alle Messwerte die gleiche absolute Abweichung haben.

    Parameters
    ----------
    daten : [float, integer]
        Liste oder Array von Messdaten
    sigma : float, integer
        Abweichung

    Returns
    -------
    uarray
        Komposition aus Daten und Fehler
    """
    return unp.uarray(daten, np.ones(len(daten))*sigma)
