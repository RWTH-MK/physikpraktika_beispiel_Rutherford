import numpy as np
from uncertainties import unumpy as unp


def _multimeter_fehler(daten, messbereich, einheitenpotenz, grundgenauigkeit, dgts, counts):
    """ Eine allgemeine Funktion für Multimeterfehler. Gibt die Daten samt Fehler in Basiseinheit zurück

    Parameters
    ----------
    daten : array_like
        Der Datensatz, der vermessen wurde
    messbereich : int
        Der Messbereich der Daten ohne Faktor (200mA Messbereich -> 200)
    einheitenpotenz : float
        Der Vorfaktor der Messgröße, z. B. milli -> 1e-3
    grundgenauigkeit : float
        Prozentuale Abweichung lt. Hersteller
    dgts : integer
        Anzahl der Digits lt. Hersteller
    counts : integer
        Counts lt. Hersteller

    Returns
    -------
    uarray
        Die Messwerte mit Fehler in Basiseinheit, z. B. wird aus Milliampere -> Ampere
    """
    schleife = len(daten)
    fehler_liste = np.empty(schleife)
    fehlerD = messbereich / counts * dgts
    for i in range(schleife):
        fehlerG = daten[i] * grundgenauigkeit / 100
        fehler_liste[i] = (fehlerD + fehlerG) * einheitenpotenz
    daten_konvert = np.array(daten)*einheitenpotenz
    return unp.uarray(daten_konvert, fehler_liste)


def _voltcraft220(daten, messbereich, einheitenpotenz, grundgenauigkeit, dgts):
    return _multimeter_fehler(daten, messbereich, einheitenpotenz, grundgenauigkeit, dgts, 2000)
def voltcraft220_200mVgleich(daten):
    """Gibt einen uarray zurück mit den Messwerten und den Fehlern des Voltcraft 220 für den Messbereich 2V Gleichstrom.
    Herstellerangaben entnommen aus (06.05.24):
    https://www.manualslib.de/manual/349243/Voltcraft-Vc-220.html?page=14#manual

    Parameters
    ----------
    daten : array_like
        Liste oder Array der Messwerte in der abgelesenen Einheit

    Returns
    -------
    uarray
        In der Basiseinheit
    """
    return _voltcraft220(daten, 200, 1e-3, 0.6, 5)
def voltcraft220_2Vgleich(daten):
    return _voltcraft220(daten, 2, 1, 0.6, 5)
def voltcraft220_20Vgleich(daten):
    return _voltcraft220(daten, 20, 1, 0.6, 5)
def voltcraft220_200Vgleich(daten):
    return _voltcraft220(daten, 200, 1, 0.6, 5)
def voltcraft220_1000Vgleich(daten):
    return _voltcraft220(daten, 1000, 1, 1, 5)
def voltcraft220_2Vwechsel(daten):
    return _voltcraft220(daten, 2, 1, 1, 5)
def voltcraft220_20Vwechsel(daten):
    return _voltcraft220(daten, 20, 1, 1, 5)
def voltcraft220_200Vwechsel(daten):
    return _voltcraft220(daten, 200, 1, 1, 5)
def voltcraft220_750Vwechsel(daten):
    return _voltcraft220(daten, 750, 1, 1.2, 5)
def voltcraft220_200muA(daten):
    return _voltcraft220(daten, 200, 1e-6, 1, 2)
def voltcraft220_2mA(daten):
    return _voltcraft220(daten, 2, 1e-3, 1, 2)
def voltcraft220_20mA(daten):
    return _voltcraft220(daten, 20, 1e-3, 1, 2)
def voltcraft220_200mA(daten):
    return _voltcraft220(daten, 200, 1e-3, 1, 2)
def voltcraft220_20A(daten):
    return _voltcraft220(daten, 0, 1, 1.2, 8)