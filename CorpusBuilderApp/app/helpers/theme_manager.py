from PyQt6.QtWidgets import QApplication, QSystemTrayIcon
from PyQt6.QtCore import QFile, QTextStream, QUrl
from PyQt6.QtMultimedia import QSoundEffect
import os

class ThemeManager:
    LIGHT_THEME_PATH = os.path.join("app", "resources", "styles", "theme_light.qss")
    DARK_THEME_PATH = os.path.join("app", "resources", "styles", "theme_dark.qss")

    @staticmethod
    def apply_theme(theme: str = "light"):
        if theme == "dark":
            path = ThemeManager.DARK_THEME_PATH
        else:
            path = ThemeManager.LIGHT_THEME_PATH

        file = QFile(path)
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            qss = stream.readAll()
            QApplication.instance().setStyleSheet(qss)
            file.close()
        else:
            print(f"[ThemeManager] Failed to load theme from {path}")