import matplotlib.pyplot as plt
import numpy as np
from uncertainties import ufloat
from uncertainties import unumpy as unp
from scipy.odr import ODR, Model, RealData
from ._plotten import PlotParameter


def odr_fit(gleichung, x_uarray, y_uarray, guess, plot: PlotParameter = None):
    """Nimmt einen scipy.odr Fit vor an Daten im uarray-Format.
    Sollte ein Problem auftreten, die uarrays als [x_uarray] und [y_uarray] übergeben

    Parameters
    ----------
    gleichung : Python-Funktion nach scipy Schema
        Diese Funktion muss gemäß scipy Doku aufgebaut sein: https://docs.scipy.org/doc/scipy/reference/odr.html
        (Basic Usage, Punkt 1). Hinweis: Kann als lambda-Funktion übergeben werden
    x_uarray : uarray
        Ggf. als [x_uarray] in den Funktionsaufruf schreiben
    y_uarray : uarray
        Ggf. als [y_uarray] in den Funktionsaufruf schreiben
    guess : [float]
        Liste der Schätz-Paramter
    plot : PlotParameter
        Optional. Falls die Daten & Fit mit Fehlerhülle geplottet werden soll; Beachte die Hinweise der Klasse.

    Returns
    -------
    odr.fit
        ein komplexer Datentyp. Nützlich allerdings zur graphischen Darstellung: Recycle die Funktion für <gleichung>:
        plt.plot(unp.nominal_values(x_uarray), <gleichung>(fit.beta, unp.nominal_values(x_uarray)))
    """

    x_wert, x_fehler = *unp.nominal_values(x_uarray), *unp.std_devs(x_uarray)
    y_wert, y_fehler = *unp.nominal_values(y_uarray), *unp.std_devs(y_uarray)

    fit_modell = Model(gleichung)
    daten = RealData(x=x_wert, sx=x_fehler, y=y_wert, sy=y_fehler)
    collage = ODR(daten, fit_modell, beta0=guess)
    fit_ergebnis = collage.run()

    if plot:
        # Der Fit soll über die x-Randwerte der Messung hinauslaufen, darum werden extra x-Werte aufgebaut. Beachte auch plt.xlim
        # Zusätzlich werden mehr Punkte mit np.linspace erstellt, um eine glatte Fitfunktion darzustellen.
        limit = 1.1 * max(x_fehler)
        x_fit = np.linspace(min(x_wert)-limit, max(x_wert)+limit, 100)*plot.x_faktor
        y_fit = gleichung(fit_ergebnis.beta, x_fit)*plot.y_faktor
        err_fit = fit_ergebnis.sd_beta[0]*plot.y_faktor
        
        limit *= plot.x_faktor
        x_plot = x_wert*plot.x_faktor
        plt.errorbar(x_plot, y_wert*plot.y_faktor,
                     xerr=x_fehler*plot.x_faktor, yerr=y_fehler*plot.y_faktor,
                     color='gray', linestyle='None', marker='None')
        plt.plot(x_fit, y_fit, color='orange', linestyle="--")
        plt.fill_between(x_fit, y_fit - err_fit, y_fit + err_fit, color='orange', alpha=0.2)
        plt.xlim(min(x_plot)-limit, max(x_plot)+limit)
        plt.xlabel(plot.x_achse)
        plt.ylabel(plot.y_achse)
        plt.title(plot.titel)
        plt.savefig(plot.datei)
        plt.show()
        plt.close()

    return fit_ergebnis


def fit_to_uarray(fit_ergebnis, print_complete_ODR_result = False):
    """
    Parameters
    ----------
    fit_para : odr_fit.return
        Der Rückgabetyp des scipy ODR-Fit Laufs
    print_complete_ODR_result : bool
        Nutzt die pprint Funktion aus scipy, die alle Ergebnisse des Fits ausgibt inkl. Kovarianzmatrix etc.
        Übersichtlicher kann man die Ergebnisse haben, wenn man den auf return dieser Funktion print() nutzt
    Returns
    -------
    uarray
        Die Fitparameter mit ihren Fehlern als uncertainty-Dateityp
    """
    if print_complete_ODR_result: fit_ergebnis.pprint()
        
    schleife = len(fit_ergebnis.beta)
    ergebnis = unp.uarray(np.zeros(schleife), np.zeros(schleife))
    for i in range(schleife):
        ergebnis[i] = ufloat(fit_ergebnis.beta[i], fit_ergebnis.sd_beta[i])
    return ergebnis
