# lehramt-physik-praktika
Eine Sammlung von Funktionen zur Versuchsauswertung mit Python im Physik Lehramt an der RWTH Aachen.
Dieses Paket baut auf Numpy und Uncertainties auf, um gut händelbare Lösungen zu ermöglichen. Außerdem sind eine
handvoll Naturkonstanten hinterlegt (ausführlicher erhältlich in 
[scipy.constants](https://docs.scipy.org/doc/scipy/reference/constants.html)).

Dieses Paket ist nicht vollständig! Um Änderungen mitzubekommen, gerne das Repo beobachten.
### Einbinden ohne Git
Soll das ganze Paket genutzt werden: Das Repo in den eigenen Ordner der Versuchsauswertung kopieren -- Dazu oben 
rechts auf den grünen `Code` Button der Webseite und dort `Download ZIP` klicken. Diese .zip dann entpacken, dass 
in der Auswertung ein physikpraktika-Ordner liegt, in dem direkt alle Dateien zu sehen sind. 

Dieses Paket ist so aufgebaut, dass bei Bedarf auch einzelne Dateien entnommen werden können: Dazu die gewünschte 
Datei in das Verzeichnis legen, in dem auch die Auswertung stattfindet und 
`import <physikpraktika_einzeldatei_ohne_.py_endung>` schreiben.

### Einbinden mit Git
Wer Git beherrscht, kann dieses Repo als [Submodul](https://github.blog/2016-02-01-working-with-submodules/)
verwenden. Dazu im eigenen Repo für die Auswertung ``git submodule add https://github.com/RWTH-MK/physikpraktika.git`` 
ausführen und bei einem Update des Repos ``git submodule update --recursive --remote`` nutzen.

## Einsatz
Es empfiehlt es sich beim Arbeiten einen kürzeren Namespace zu wählen, z. B. `import physikpraktika as fp`. 
Bitte auf keinen Fall `as *` importieren, die Naturkonstanten sind leicht zu überschreiben.
Alle Befehle sind ausgiebig kommentiert und hoffentlich namentlich eindeutig. 

Ein Beispiel: Wir haben eine Reihe von Interferenzfiltern, die mangels Herstellerangabe zu 1% Fehler angenommen werden. Dazu 
folgender Code mit den nötigen Imports und unseren Filterdaten:
```python
from uncertainties import unumpy
import physikpraktika as fp

interferenzfilter = [420, 690, 1313]  # nm
```
Jetzt kann 
```python
filter = fp.relativer_fehler(interferenzfilter, 1)
```
genutzt werden, um direkt ein uarray (Array von ufloats) zu erzeugen. Um alle Funktionen kennenzulernen am besten kurz
in die Dateien schauen, die sind wirklich überschaubar.

Bei Fragen und Problemen bitte ein Issue eröffnen oder auf kurzem Dienstweg melden ;) 
