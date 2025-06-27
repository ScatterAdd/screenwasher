import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer, QRect, Qt
from PyQt5.QtGui import QPainter, QColor, QBrush

class Bildschirmputzer(QWidget):
    def close_window(self):
        self.close()
    def keyPressEvent(self, event):
        self.close()

    def mousePressEvent(self, event):
        self.close()

    def mouseMoveEvent(self, event):
        if self._last_mouse_pos is None:
            self._last_mouse_pos = event.pos()
        else:
            if (event.pos() - self._last_mouse_pos).manhattanLength() > 5:
                self.close()
        self._last_mouse_pos = event.pos()
    def __init__(self):
        super().__init__()
        # Fenster auf Vollbild, ohne Rahmen, immer im Vordergrund
        try:
            from PyQt5.QtCore import Qt
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            self.setAttribute(Qt.WA_TranslucentBackground)
        except Exception:
            FRAMELESS = 0x00000800
            ONTOP = 0x00040000
            TRANSLUCENT = 86
            self.setWindowFlags(self.windowFlags() | FRAMELESS | ONTOP)
            self.setAttribute(TRANSLUCENT)
        self.showFullScreen()
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.geometry()
            self.screen_width = screen_geometry.width()
            self.screen_height = screen_geometry.height()
        else:
            self.screen_width = 1920
            self.screen_height = 1080
        self.lappen_breite = int(self.screen_width * 0.275)
        self.lappen_hoehe = int(self.screen_height * 0.16)
        self.anim_time = 0.0
        self.anim_duration = 2.0  # Sekunden (schneller)
        self.fps = 60
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_lappen)
        self.putzt = False
        self._last_mouse_pos = None
        # Bewegungsmuster-Namen (werden später als Closures umgesetzt)
        self.patterns = [
            "horizontal_lr",
            "horizontal_rl",
            "vertical_tb",
            "vertical_bt",
            "diagonal_tl_br",
            "diagonal_tr_bl",
            "diagonal_bl_tr",
            "diagonal_br_tl",
            "ellipse",
            "circle",
            "zigzag",
            "zigzag_bt"
        ]
        self.current_pattern = None
        self.pattern_func = None
        self.looping = True
        # Putzspur-Fläche (persistent)
        from PyQt5.QtGui import QImage
        self.spur_image = QImage(self.screen_width, self.screen_height, QImage.Format_ARGB32_Premultiplied)
        self.spur_image.fill(0)  # komplett transparent
        self.lappen_x = -self.lappen_breite
        self.lappen_y = -self.lappen_hoehe
        self._animation_started = False
        self.choose_new_pattern()
        self.start_putzen()

    def start_putzen(self):
        self.anim_time = 0.0
        self.putzt = True
        # self.spur_image.fill(0)  # Putzspur bleibt erhalten
        # Zufällige Putzspur-Parameter generieren
        import random
        self.spur_count = 7
        self.spur_offsets = [random.randint(-int(self.lappen_hoehe*0.18), int(self.lappen_hoehe*0.18)) for _ in range(self.spur_count)]
        self.spur_widths = [random.randint(int(self.lappen_hoehe*0.13), int(self.lappen_hoehe*0.28)) for _ in range(self.spur_count)]
        # Zufällige kräftige Grundfarbe für diese Bewegung
        def random_color():
            import colorsys
            h = random.random()
            s = 0.7 + 0.3 * random.random()
            v = 0.7 + 0.3 * random.random()
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            return int(r*255), int(g*255), int(b*255)
        self.spur_basecolor = random_color()
        self.timer.start(int(1000 / self.fps))

    def move_lappen(self):
        self.anim_time += 1.0 / self.fps
        t = min(self.anim_time / self.anim_duration, 1.0)
        # Bewegungsmuster anwenden
        if self.pattern_func:
            x, y = self.pattern_func(t)
            self.lappen_x = x
            self.lappen_y = y
        # Bei jedem Frame: aktuelle Lappenposition auf die Spurfläche malen
        if (self.lappen_x > -self.lappen_breite and self.lappen_x < self.screen_width and
            self.lappen_y > -self.lappen_hoehe and self.lappen_y < self.screen_height):
            from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
            import random
            painter = QPainter(self.spur_image)
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            # Jede Bewegung hat eine eigene kräftige Grundfarbe
            base_r, base_g, base_b = self.spur_basecolor
            grundfarbe = QColor(base_r, base_g, base_b, 110)
            painter.setBrush(QBrush(grundfarbe))
            painter.setPen(QPen(QColor(0,0,0,0)))
            rect = QRect(self.lappen_x, self.lappen_y, self.lappen_breite, self.lappen_hoehe)
            painter.drawRoundedRect(rect, 32, 32)
            for i in range(self.spur_count):
                offset = self.spur_offsets[i]
                width = self.spur_widths[i]
                # Leichte Variation der Grundfarbe für Streifen
                dr = random.randint(-30, 60)
                dg = random.randint(-30, 60)
                db = random.randint(-30, 60)
                color = QColor(
                    min(255, max(0, base_r + dr)),
                    min(255, max(0, base_g + dg)),
                    min(255, max(0, base_b + db)),
                    random.randint(60, 120)
                )
                painter.setBrush(QBrush(color))
                rect2 = QRect(self.lappen_x + offset, self.lappen_y + offset, self.lappen_breite - width, self.lappen_hoehe - width)
                painter.drawRoundedRect(rect2, 24, 24)
            painter.end()
        self.update()
        if t >= 1.0:
            self.timer.stop()
            self._animation_started = True
            self.putzt = False
            if self.looping:
                self.choose_new_pattern()
                QTimer.singleShot(400, self.start_putzen)
            else:
                QTimer.singleShot(800, self.close_window)

    # Die Methode male_spur_auf_image entfällt, da die Spur jetzt direkt in move_lappen gemalt wird

    def choose_new_pattern(self):
        import random
        pattern = random.choice(self.patterns)
        self.current_pattern = pattern
        # Zufällige Start-/Endpunkte für generische Richtungen
        if pattern == "horizontal_lr":
            y_offset = random.randint(-self.lappen_hoehe, self.lappen_hoehe)
            y = random.randint(0, self.screen_height - self.lappen_hoehe) + y_offset
            x_offset = random.randint(-self.lappen_breite, self.lappen_breite)
            def func(t):
                x = int(-self.lappen_breite + x_offset + t * (self.screen_width + self.lappen_breite*2))
                return x, y
            self.pattern_func = func
        elif pattern == "horizontal_rl":
            y_offset = random.randint(-self.lappen_hoehe, self.lappen_hoehe)
            y = random.randint(0, self.screen_height - self.lappen_hoehe) + y_offset
            x_offset = random.randint(-self.lappen_breite, self.lappen_breite)
            def func(t):
                x = int(self.screen_width + self.lappen_breite + x_offset - t * (self.screen_width + self.lappen_breite*2))
                return x, y
            self.pattern_func = func
        elif pattern == "vertical_tb":
            x_offset = random.randint(-self.lappen_breite, self.lappen_breite)
            x = random.randint(0, self.screen_width - self.lappen_breite) + x_offset
            y_offset = random.randint(-self.lappen_hoehe, self.lappen_hoehe)
            def func(t):
                y = int(-self.lappen_hoehe + y_offset + t * (self.screen_height + self.lappen_hoehe*2))
                return x, y
            self.pattern_func = func
        elif pattern == "vertical_bt":
            x_offset = random.randint(-self.lappen_breite, self.lappen_breite)
            x = random.randint(0, self.screen_width - self.lappen_breite) + x_offset
            y_offset = random.randint(-self.lappen_hoehe, self.lappen_hoehe)
            def func(t):
                y = int(self.screen_height + self.lappen_hoehe + y_offset - t * (self.screen_height + self.lappen_hoehe*2))
                return x, y
            self.pattern_func = func
        elif pattern == "diagonal_tl_br":
            # Diagonale von oben links nach unten rechts, mit großem Offset-Bereich
            x_offset = random.randint(-self.screen_width, self.screen_width)
            y_offset = random.randint(-self.screen_height, self.screen_height)
            def func(t):
                x = int(-self.lappen_breite + x_offset + t * (self.screen_width + self.lappen_breite*2))
                y = int(-self.lappen_hoehe + y_offset + t * (self.screen_height + self.lappen_hoehe*2))
                return x, y
            self.pattern_func = func
        elif pattern == "diagonal_tr_bl":
            x_offset = random.randint(-self.screen_width, self.screen_width)
            y_offset = random.randint(-self.screen_height, self.screen_height)
            def func(t):
                x = int(self.screen_width + self.lappen_breite + x_offset - t * (self.screen_width + self.lappen_breite*2))
                y = int(-self.lappen_hoehe + y_offset + t * (self.screen_height + self.lappen_hoehe*2))
                return x, y
            self.pattern_func = func
        elif pattern == "diagonal_bl_tr":
            x_offset = random.randint(-self.screen_width, self.screen_width)
            y_offset = random.randint(-self.screen_height, self.screen_height)
            def func(t):
                x = int(-self.lappen_breite + x_offset + t * (self.screen_width + self.lappen_breite*2))
                y = int(self.screen_height + self.lappen_hoehe + y_offset - t * (self.screen_height + self.lappen_hoehe*2))
                return x, y
            self.pattern_func = func
        elif pattern == "diagonal_br_tl":
            x_offset = random.randint(-self.screen_width, self.screen_width)
            y_offset = random.randint(-self.screen_height, self.screen_height)
            def func(t):
                x = int(self.screen_width + self.lappen_breite + x_offset - t * (self.screen_width + self.lappen_breite*2))
                y = int(self.screen_height + self.lappen_hoehe + y_offset - t * (self.screen_height + self.lappen_hoehe*2))
                return x, y
            self.pattern_func = func
        elif pattern == "ellipse":
            # Spiral-Ellipse: von innen nach außen oder außen nach innen
            spiral_out = random.choice([True, False])
            from math import sin, cos, pi
            center_x = self.screen_width // 2
            center_y = self.screen_height // 2
            a_max = (self.screen_width + self.lappen_breite) // 2 - 2
            b_max = (self.screen_height + self.lappen_hoehe) // 2 - 2
            a_min = int(a_max * 0.12)
            b_min = int(b_max * 0.12)
            def func(t):
                # Spiral: Radius wächst oder schrumpft
                if spiral_out:
                    f = t
                else:
                    f = 1.0 - t
                a = int(a_min + (a_max - a_min) * f)
                b = int(b_min + (b_max - b_min) * f)
                theta = 4 * pi * t  # 2 Umdrehungen
                x = int(center_x + a * cos(theta) - self.lappen_breite // 2)
                y = int(center_y + b * sin(theta) - self.lappen_hoehe // 2)
                return x, y
            self.pattern_func = func
        elif pattern == "circle":
            def func(t):
                from math import sin, cos, pi
                center_x = self.screen_width // 2
                center_y = self.screen_height // 2
                r = (min(self.screen_width + self.lappen_breite, self.screen_height + self.lappen_hoehe)) // 2 - 2
                theta = 2 * pi * t
                x = int(center_x + r * cos(theta) - self.lappen_breite // 2)
                y = int(center_y + r * sin(theta) - self.lappen_hoehe // 2)
                return x, y
            self.pattern_func = func
        elif pattern == "zigzag":
            # Zickzack von links nach rechts, y deckt gesamte Fläche ab
            y = random.randint(0, self.screen_height - self.lappen_hoehe)
            def func(t):
                from math import sin, pi
                x = int(-self.lappen_breite + t * (self.screen_width + self.lappen_breite))
                amplitude = self.screen_height // 2
                freq = 7
                y2 = int(y + amplitude * sin(2 * pi * freq * t))
                return x, min(max(y2, 0), self.screen_height - self.lappen_hoehe)
            self.pattern_func = func
        elif pattern == "zigzag_bt":
            # Zickzack von rechts nach links, y deckt gesamte Fläche ab
            y = random.randint(0, self.screen_height - self.lappen_hoehe)
            def func(t):
                from math import sin, pi
                x = int(self.screen_width + self.lappen_breite - t * (self.screen_width + self.lappen_breite))
                amplitude = self.screen_height // 2
                freq = 7
                y2 = int(y - amplitude * sin(2 * pi * freq * t))
                return x, min(max(y2, 0), self.screen_height - self.lappen_hoehe)
            self.pattern_func = func

    # Bewegungsmuster-Methoden entfallen, alles läuft jetzt über pattern_func

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        # 1. Persistente Putzspur-Fläche zeichnen
        painter.drawImage(0, 0, self.spur_image)
        # 2. Aktuelle Spur (nur während putzt) als Overlay
        if self.putzt:
            from PyQt5.QtGui import QPen
            import random
            painter.setPen(QPen(QColor(0, 0, 0, 0)))
            grundfarbe = QColor(180, 80, 255, 120)
            painter.setBrush(QBrush(grundfarbe))
            rect = QRect(self.lappen_x, self.lappen_y, self.lappen_breite, self.lappen_hoehe)
            painter.drawRoundedRect(rect, 32, 32)
            for i in range(self.spur_count):
                offset = self.spur_offsets[i]
                width = self.spur_widths[i]
                color = QColor(180, 80, 255, random.randint(80, 140))
                painter.setBrush(QBrush(color))
                rect2 = QRect(self.lappen_x + offset, self.lappen_y + offset, self.lappen_breite - width, self.lappen_hoehe - width)
                painter.drawRoundedRect(rect2, 24, 24)
        # 3. Giftgrüner Lappen als abgerundetes Rechteck
        lappen_color = QColor(180, 80, 255)
        rand_color = QColor(120, 40, 180)
        painter.setBrush(QBrush(lappen_color))
        painter.setPen(rand_color)
        rect = QRect(self.lappen_x, self.lappen_y, self.lappen_breite, self.lappen_hoehe)
        painter.drawRoundedRect(rect, 32, 32)

from PyQt5.QtCore import Qt

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenster = Bildschirmputzer()
    fenster.show()
    sys.exit(app.exec_())
