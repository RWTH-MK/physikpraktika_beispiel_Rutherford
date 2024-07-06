import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from uncertainties import unumpy as unp
from ._plotten import PlotParameter


def peak_index(daten, erwartete_peak_zahl):
    """Diese Funktion kann genutzt werden, um die Punkte von Peaks zu bestimmen.

    Parameters
    ----------
    daten : [float]
        Die Werte, die auf der y-Achse aufgetragen würde. Diese Werte müssen fehlerfrei sein, also ggf.
        unp.nominal_values(<y_werte>) übergeben.
    erwartete_peak_zahl : int

    Returns
    -------
    [int]
        Die Indizes, an denen die Peaks liegen. Das heißt, mit daten[i] kann der y-Wert ausgelesen werden,
        analog dazu der Punkt auf der x-Achse.

    """
    prominenz = 42
    peak_indizes = find_peaks(daten, prominence=prominenz)
    if len(peak_indizes[0]) != erwartete_peak_zahl:
        while len(peak_indizes[0]) > erwartete_peak_zahl:
            prominenz += 1
            peak_indizes = find_peaks(daten, prominence=prominenz)
        while len(peak_indizes[0]) < erwartete_peak_zahl:
            prominenz -= 0.5
            peak_indizes = find_peaks(daten, prominence=prominenz)

    return peak_indizes[0]


def _gauss(x, a, x0, sigma):
    return a * np.exp(-(x - x0)**2 / (2 * sigma**2))


def peak_gauss(x_wert, y_wert, plot: PlotParameter = None):
    """

    Parameters
    ----------
    x_wert: [float]
        Die x-Werte als Array oder Liste
    y_wert: [float]
        Die y-Werte als Array oder Liste
    plot: PlotParameter
        Optional. Falls die Daten & Fit geplottet werden soll; Beachte die Hinweise der Klasse.

    Returns
    -------
    uarray
        Die Parameter des Gauß-Fits mit Fehler in der Reihenfolge
            a (Vor-/Normierungsfaktor),
            x_0 (Mittelwert),
            sigma (Std.abw.)

    """
    # Initiale Schätzparameter
    mean = np.mean(x_wert)
    sigma = np.std(x_wert)
    max_y = np.max(y_wert)

    popt, pcov = curve_fit(_gauss, x_wert, y_wert, p0=[max_y, mean, sigma])
    err = np.sqrt(np.diag(pcov))
    ergebnis = unp.uarray(popt, err)

    if plot:
        x_plot = x_wert * plot.x_faktor
        y_fit = _gauss(x_wert, *popt) * plot.y_faktor
        plt.plot(x_plot, y_wert * plot.y_faktor, color='gray', linestyle='None', marker='.')
        plt.plot(x_plot, y_fit, color='orange', linestyle="--")
        plt.xlabel(plot.x_achse)
        plt.ylabel(plot.y_achse)
        plt.title(plot.titel)
        plt.savefig(plot.datei)
        plt.show()
        plt.close()

    return ergebnis