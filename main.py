import sys
import ctypes
from ctypes import wintypes
from datetime import datetime
from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QFont, QColor, QPainter, QPen, QAction
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QSystemTrayIcon, QMenu, QSlider, QFrame, QPushButton, QGraphicsDropShadowEffect
)

class ClockOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.drag_pos = None
        self.opacity_value = 92
        self.compact = False
        self.setWindowTitle("ChronoOverlay")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.resize(390, 190)
        self.build_ui()
        self.apply_opacity()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(250)
        self.update_clock()

        self.apply_windows_glass()

        self.tray = QSystemTrayIcon(self)
        self.tray.setToolTip("ChronoOverlay — horloge flottante")
        menu = QMenu()
        show_action = QAction("Afficher / masquer", self)
        show_action.triggered.connect(self.toggle_visibility)
        compact_action = QAction("Mode compact", self)
        compact_action.triggered.connect(self.toggle_compact)
        quit_action = QAction("Quitter", self)
        quit_action.triggered.connect(QApplication.quit)
        menu.addAction(show_action)
        menu.addAction(compact_action)
        menu.addSeparator()
        menu.addAction(quit_action)
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self.tray_activated)
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray.show()

    def apply_windows_glass(self):
        """Active le matériau Acrylic de Windows 11 derrière la fenêtre, si disponible."""
        if sys.platform != "win32":
            return
        try:
            hwnd = int(self.winId())
            # DWMWA_SYSTEMBACKDROP_TYPE = 38 ; DWMSBT_TRANSIENTWINDOW = 3 (Acrylic)
            value = ctypes.c_int(3)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                wintypes.HWND(hwnd), 38, ctypes.byref(value), ctypes.sizeof(value)
            )
            # Coins arrondis natifs lorsque Windows le permet.
            corner = ctypes.c_int(2)  # DWMWCP_ROUND
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                wintypes.HWND(hwnd), 33, ctypes.byref(corner), ctypes.sizeof(corner)
            )
        except Exception:
            # Le style translucide Qt reste actif en cas d'indisponibilité de DWM.
            pass

    def build_ui(self):
        self.panel = QFrame(self)
        self.panel.setObjectName("panel")
        self.panel.setStyleSheet("""
            QFrame#panel {
                background-color: rgba(225, 239, 255, 34);
                border: 1px solid rgba(255, 255, 255, 112);
                border-top: 1px solid rgba(255, 255, 255, 190);
                border-radius: 25px;
            }
            QLabel { background: transparent; }
            QPushButton {
                color: rgba(255,255,255,235);
                background: rgba(255,255,255,32);
                border: 1px solid rgba(255,255,255,90);
                border-radius: 11px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background: rgba(255,255,255,75);
                border: 1px solid rgba(255,255,255,160);
            }
        """)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(42)
        shadow.setOffset(0, 12)
        shadow.setColor(QColor(5, 18, 40, 95))
        self.panel.setGraphicsEffect(shadow)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(8, 8, 8, 8)
        outer.addWidget(self.panel)

        layout = QVBoxLayout(self.panel)
        layout.setContentsMargins(22, 15, 22, 16)
        layout.setSpacing(2)

        top = QHBoxLayout()
        self.brand = QLabel("◈  CHRONO / LIVE")
        self.brand.setStyleSheet("color:rgba(255,255,255,220); letter-spacing:3px; font-size:10px; font-weight:700;")
        top.addWidget(self.brand)
        top.addStretch()
        self.pin_label = QLabel("●  ALWAYS ON TOP")
        self.pin_label.setStyleSheet("color:rgba(218,255,245,225); font-size:9px; letter-spacing:1px;")
        top.addWidget(self.pin_label)
        layout.addLayout(top)

        self.time_label = QLabel("--:--:--")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setFont(QFont("Segoe UI", 43, QFont.Weight.DemiBold))
        self.time_label.setStyleSheet("color:rgba(255,255,255,248);")
        layout.addWidget(self.time_label)

        self.date_label = QLabel("...")
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date_label.setFont(QFont("Segoe UI", 11))
        self.date_label.setStyleSheet("color:rgba(238,247,255,205); letter-spacing:2px;")
        layout.addWidget(self.date_label)

        self.controls = QWidget()
        controls_layout = QHBoxLayout(self.controls)
        controls_layout.setContentsMargins(0, 8, 0, 0)
        controls_layout.setSpacing(8)
        hint = QLabel("GLISSER POUR DÉPLACER")
        hint.setStyleSheet("color:rgba(240,248,255,155); font-size:8px; letter-spacing:1px;")
        controls_layout.addWidget(hint)
        controls_layout.addStretch()
        compact_btn = QPushButton("—")
        compact_btn.setToolTip("Mode compact")
        compact_btn.setFixedWidth(30)
        compact_btn.clicked.connect(self.toggle_compact)
        close_btn = QPushButton("×")
        close_btn.setToolTip("Quitter")
        close_btn.setFixedWidth(30)
        close_btn.clicked.connect(QApplication.quit)
        controls_layout.addWidget(compact_btn)
        controls_layout.addWidget(close_btn)
        layout.addWidget(self.controls)

    def update_clock(self):
        now = datetime.now()
        self.time_label.setText(now.strftime("%H:%M:%S"))
        # French date, independent of the Windows display language.
        weekdays = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
        months = ["janvier", "février", "mars", "avril", "mai", "juin",
                  "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
        date_text = f"{weekdays[now.weekday()]}  {now.day:02d} {months[now.month-1]} {now.year}"
        self.date_label.setText(date_text.upper())

    def apply_opacity(self):
        self.setWindowOpacity(self.opacity_value / 100)

    def toggle_compact(self):
        self.compact = not self.compact
        self.date_label.setVisible(not self.compact)
        self.controls.setVisible(not self.compact)
        self.brand.setVisible(not self.compact)
        self.pin_label.setVisible(not self.compact)
        self.time_label.setFont(QFont("Segoe UI", 35 if self.compact else 43, QFont.Weight.DemiBold))
        self.resize(300, 100 if self.compact else 190)

    def toggle_visibility(self):
        self.setVisible(not self.isVisible())

    def tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.toggle_visibility()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.drag_pos is not None and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        compact = menu.addAction("Quitter / restaurer le mode compact")
        opacity = menu.addMenu("Transparence")
        for value in (100, 92, 80, 65):
            action = opacity.addAction(f"{value} %")
            action.triggered.connect(lambda checked=False, v=value: self.set_opacity(v))
        quit_action = menu.addAction("Quitter")
        chosen = menu.exec(event.globalPos())
        if chosen == compact:
            self.toggle_compact()
        elif chosen == quit_action:
            QApplication.quit()

    def set_opacity(self, value):
        self.opacity_value = value
        self.apply_opacity()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("ChronoOverlay")
    clock = ClockOverlay()
    clock.show()
    sys.exit(app.exec())