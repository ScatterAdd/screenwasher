# screenwasher

    This project is licensed under the GNU General Public License v3.0. See the 
    LICENSE file for details.

# English

A useful and entertaining PyQt5 screensaver that animates a sponge across the screen. The sponge leaves a vibrant, semi-transparent cleaning trail, with a new color for every movement. Various movement patterns (horizontal, vertical, diagonal, zigzag, circle, ellipse, spiral) create a colorful, chaotic artwork.

## Features
- Fullscreen, always on top, transparent background
- Instantly closes on mouse movement or key press
- Sponge is violet, cleaning trail in random, vivid colors
- Movement patterns: horizontal, vertical, diagonal, zigzag, circle, ellipse (also spiral)
- Every movement a new color, trails mix
- Endless animation, perfect as a "screensaver"

## Installation
1. Install Python 3 and PyQt5:
   ```bash
   pip install PyQt5
   ```
2. Run the script `screenwasher.py`:
   ```bash
   python3 screenwasher.py
   ```

## Using as a screensaver

**Linux (e.g. xscreensaver):**
1. Make sure the script closes on mouse movement or key press (see code).
2. To add your own screensaver entry, edit the file `~/.xscreensaver` manually:
   - Open `~/.xscreensaver` in a text editor.
   - Find the line starting with `programs:`.
   - Add a new line, for example:
     ```
     "Screenwasher" python3 /path/to/screenwasher.py \\
     ```
     (Make sure to keep 2 backslash at the end of the previous line.)
   - Save the file and restart xscreensaver:
     ```bash
     xscreensaver-command -restart
     ```
   - Now you can select "Screenwasher" in the xscreensaver list.
   - Make sure the script is executable.

**Windows:**
1. Use PyInstaller to create an .exe:
   ```bash
   pip install pyinstaller
   pyinstaller --onefile --noconsole screenwasher.py
   ```
2. Rename the .exe to `screenwasher.scr`.
3. Copy the .scr file to `C:\Windows\System32` and select it as your screensaver.
4. (Optional) Adjust the code to react to the `/s` argument.

**General:**
- For screensaver use, the program should close immediately on mouse movement or key press.
- See code comments for how to add this.

---


# Bildschirmputzer (screenwasher)

Ein nützlicher und unterhaltsamer PyQt5-Bildschirmschoner, der einen animierten Schwamm über den Bildschirm bewegt. Der Schwamm hinterlässt eine bunte, halbtransparente Putzspur, die sich mit jeder Bewegung farblich ändert und sich mit anderen Spuren mischt. Verschiedene Bewegungsmuster (horizontal, vertikal, diagonal, Zickzack, Kreis, Ellipse, Spirale) sorgen für Abwechslung und ein farbenfrohes, chaotisches Kunstwerk.

## Features
- Vollbild, immer im Vordergrund, transparenter Hintergrund
- Sofortiges Beenden bei Mausbewegung oder Tastendruck
- Schwamm in violett, Putzspur in zufälligen, kräftigen Farben
- Bewegungsmuster: horizontal, vertikal, diagonal, Zickzack, Kreis, Ellipse (auch spiralförmig)
- Jede Bewegung eine neue Farbe, Spuren mischen sich
- Animation läuft endlos, ideal als "Bildschirmschoner"

## Installation
1. Python 3 und PyQt5 installieren:
   ```bash
   pip install PyQt5
   ```
2. Das Skript `screenwasher.py` ausführen:
   ```bash
   python3 screenwasher.py
   ```

## Als Bildschirmschoner nutzen

**Linux (z.B. mit xscreensaver):**
1. Stelle sicher, dass das Skript bei Mausbewegung oder Tastendruck beendet wird (siehe Code).
2. Um einen eigenen Bildschirmschoner-Eintrag hinzuzufügen, bearbeite die Datei `~/.xscreensaver` manuell:
   - Öffne `~/.xscreensaver` in einem Texteditor.
   - Suche die Zeile, die mit `programs:` beginnt.
   - Füge eine neue Zeile hinzu, zum Beispiel:
     ```
     "Screenwasher" python3 /pfad/zu/screenwasher.py \\
     ```
     (Achte darauf, dass am Ende der vorherigen Zeile 2 Backslash stehen.)
   - Speichere die Datei und starte xscreensaver neu:
     ```bash
     xscreensaver-command -restart
     ```
   - Nun kannst du "Screenwasher" in der xscreensaver-Liste auswählen.
   - Stelle sicher, dass das Skript ausführbar ist.

**Windows:**
1. Erzeuge mit PyInstaller eine .exe:
   ```bash
   pip install pyinstaller
   pyinstaller --onefile --noconsole screenwasher.py
   ```
2. Benenne die erzeugte .exe in `screenwasher.scr` um.
3. Kopiere die .scr-Datei nach `C:\Windows\System32` und wähle sie als Bildschirmschoner aus.
4. (Optional) Passe den Code an, um auf das `/s`-Argument zu reagieren.

**Allgemein:**
- Für Bildschirmschoner sollte das Programm sofort bei Mausbewegung oder Tastendruck schließen.

# License
   This project is licensed under the GNU General Public License v3.0. See the 
   LICENSE file for details.

## Third‑party libraries and licenses
   PyQt5 (Riverbank): GPL (see included license file or upstream)
   
   PyOpenGL (if used): BSD/MIT‑style (check upstream)
   
   All bundled third‑party license texts are retained in this repository. If you   
   include any external files or binaries, see the corresponding license files in the
   repo.

