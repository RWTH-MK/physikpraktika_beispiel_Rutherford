import uncertainties.unumpy as unp
from uncertainties.umath import *
import physikpraktika as fp

# Globale Variablen und Fehlerparameter
DELTA_z = 1e-3  # m
DELTA_t = 2  # %
KONSTANTE_sx_dx = 2.3e-2  # m
KONSTANTE_sz_dz = 4.7e-2  # m
def alpha(z: float):
    return atan(KONSTANTE_sx_dx / (2 * z - KONSTANTE_sz_dz))
def theta_halbe(z: float):
    return 90-alpha(z)
def sin_4(z: float):
    return sin(theta_halbe(z))**(-4)
def r2(z: float):
    r = KONSTANTE_sx_dx / sin(alpha(z))
    return r**2
def r_2_sin_4(z: float):
    return sin_4(z)/r2(z)

def rate(counts: int, sekunden: int):
    return counts/sekunden


# === Messwerte ===
rohdaten_counts = [154, 178, 181, 144, 126]
rohdaten_zeit = [1009, 1610, 2565, 2782, 3930]  # s
rohdaten_abstand = [0.035, 0.04, 0.045, 0.05, 0.055]  # m

# === Auswertung ===
# Unsicherheiten verrechnen
werte_zeit = fp.relativer_fehler(rohdaten_zeit, DELTA_t)
werte_abstand = fp.absoluter_fehler(rohdaten_abstand, DELTA_z)

# Größen zur Auftragung bestimmen
werte_rate = [rate(c, t) for c, t in zip(rohdaten_counts, werte_zeit)]
werte_rsina = [r_2_sin_4(z) for z in werte_abstand]

# Graphische Auswertung
plotten = fp.PlotParameter(titel='Rutherford-Streuung', x_achse=r'$r^{-2}sin^{-4}(\theta /2) ~[m^{-2}]$',
                           y_achse=r'$Zählrate ~[s^{-1}]$', datei='fit.svg')
proto_ergebnis = fp.odr_fit(gleichung = lambda B, x: B[0]*x + B[1],
                            x_uarray=[werte_rsina], y_uarray=[werte_rate],
                            guess = [1, 0], plot=plotten)
ergebnis = fp.fit_to_uarray(proto_ergebnis)
print(ergebnis)
