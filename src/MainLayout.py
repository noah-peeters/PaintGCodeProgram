"""
    Center widget layout for MainWindow.
"""
from tkinter import Image
import PySide6.QtWidgets as qtw

import src.ImageViewer as ImageViewer


class CenterWidget(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.imageViewer = ImageViewer.ImageViewer()

        layout = qtw.QHBoxLayout(self)
        layout.addWidget(self.imageViewer)
        self.setLayout(layout)
