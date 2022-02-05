import os, sys, tempfile
import PySide6.QtWidgets as qtw

# Hack to allow imports from src/
# src: https://codeolives.com/2020/01/10/python-reference-module-in-parent-directory/
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import src.MainWindow.MainWindow as MainWindow
import src.settings as settings

settings.init()

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec())
