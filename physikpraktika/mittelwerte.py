import numpy as np
from uncertainties import ufloat
from uncertainties import unumpy as unp


def mittelwert(messreihe):
    """Nützlich, wenn eine Messgröße mehrfach erfasst wurde.

    Parameters
    ----------
    messreihe: [integer, float]
        Liste oder Array der Messdaten

    Returns
    -------
    ufloat
        Arithmetisches Mittel und Standardabweichung der Messdaten
    """
    reihe = np.array(messreihe)
    return ufloat(reihe.mean(), reihe.std())


def gewichteter_mittelwert(daten):
    """Bestimme den gewichteten Mittelwert. Sollte ein Fehler von 0 vorliegen, wird dies in der Konsole geschrieben
    und zum Weiterlaufen des Programms der kleinste Fehler ungleich Null verwendet.

    Parameters
    ----------
    daten : uarray
        Die Daten und Fehler müssen zusammen als uarray vorliegen

    Returns
    -------
    ufloat
        Gesamtergebnis
    """
    sum_mittelwert, sum_std = 0, 0

    min_std = 1
    for i in unp.std_devs(daten):
        if i == 0:
            print("Problem in physikpraktika.gewichteter_mittelwert: Der Messwert mit Index %i hat einen "
                  "Fehler von 0 -- setze diesen gleich dem kleinsten sonstigen Fehler, um weiterzurechnen" % i)
        if 0 < i < min_std:
            min_std = i

    for wert in daten:
        sigma = wert.std_dev if wert.std_dev != 0 else min_std
        gewicht = 1 / sigma**2
        sum_std += gewicht
        sum_mittelwert += wert.nominal_value * gewicht
    mittelwert = sum_mittelwert / sum_std
    std = 1 / np.sqrt(sum_std)
    return ufloat(mittelwert, std)
