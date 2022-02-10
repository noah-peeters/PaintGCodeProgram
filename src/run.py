import os, sys
import PySide6.QtWidgets as qtw
import qt_material

# Hack to allow imports from src/
# src: https://codeolives.com/2020/01/10/python-reference-module-in-parent-directory/
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import src.MainWindow as MainWindow
import src.settings as settings

settings.init()

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow.MainWindow()

    qt_material.apply_stylesheet(app, theme="dark_cyan.xml")

    window.show()
    sys.exit(app.exec())
