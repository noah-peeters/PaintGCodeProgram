"""
    Center widget layout for MainWindow.
    Parent of loaded images widget, ImageViewer and splitter layout(s).
"""
import PySide6.QtWidgets as qtw


class MainLayout(qtw.QWidget):
    def __init__(self):
        super().__init__()
