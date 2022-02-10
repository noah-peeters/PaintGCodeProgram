"""
G-code generation dialog. (opened by MainWindow)
"""
import PySide6.QtWidgets as qtw


class Dialog(qtw.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("G-code generation")
        self.setModal(True)

        time_taken_label = qtw.QLabel("Operation took: HH:MM:SS")
        stat2 = qtw.QLabel("Stat 2 test label")

        # Button box
        button_box = qtw.QDialogButtonBox()
        button_box.clicked.connect(lambda: self.close())
        button_box.addButton(qtw.QDialogButtonBox.Ok)

        v_layout = qtw.QVBoxLayout()
        v_layout.addWidget(time_taken_label)
        v_layout.addWidget(stat2)
        v_layout.addWidget(button_box)

        self.setLayout(v_layout)
