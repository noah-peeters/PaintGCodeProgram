"""
G-code generation dialog. (opened by MainWindow)
"""
import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw


# Label with Slider with SpinBox widget (only containing numbers)
class NumberSliderWidget(qtw.QWidget):
    def __init__(self, labelText, lowVal, highVal, defaultVal):
        super().__init__()

        self.label = qtw.QLabel(labelText)

        self.slider = qtw.QSlider(qtc.Qt.Orientation.Horizontal)
        self.slider.setSingleStep(1)
        self.slider.setMinimum(lowVal)
        self.slider.setMaximum(highVal)
        self.slider.setValue(defaultVal)
        self.slider.valueChanged.connect(self.value_changed)

        self.spinBox = qtw.QSpinBox()
        self.spinBox.setMinimum(lowVal)
        self.spinBox.setMaximum(highVal)
        self.spinBox.setValue(defaultVal)
        self.spinBox.valueChanged.connect(self.value_changed)

        horizontalLayout = qtw.QHBoxLayout()
        horizontalLayout.addWidget(self.label)
        horizontalLayout.addWidget(self.slider)
        horizontalLayout.addWidget(self.spinBox)

        self.setLayout(horizontalLayout)

    # Value of slider or spinbox changed --> make sure they both display the new value
    def value_changed(self, newValue):
        if self.slider.value() != newValue:
            self.slider.setValue(newValue)
        elif self.spinBox.value() != newValue:
            self.spinBox.setValue(newValue)


class Dialog(qtw.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("G-code generation")
        self.setModal(True)

        v_layout = qtw.QVBoxLayout()
        self.max_length = NumberSliderWidget("Max. working length (mm):", 10, 2000, 250)
        self.dot_diameter = NumberSliderWidget("Dot diameter (mm):", 1, 5, 3)
        self.xy_speed = NumberSliderWidget(
            "XY movement speed (mm/min):", 100, 4000, 3000
        )
        self.z_speed = NumberSliderWidget(
            "Z movement speed (mm/min):", 100, 4000, 1700
        )
        v_layout.addWidget(self.max_length)
        v_layout.addWidget(self.dot_diameter)
        v_layout.addWidget(self.xy_speed)
        v_layout.addWidget(self.z_speed)

        buttonBox = qtw.QDialogButtonBox(self)
        buttonBox.addButton("Cancel", qtw.QDialogButtonBox.RejectRole)
        buttonBox.addButton("Apply", qtw.QDialogButtonBox.AcceptRole)
        buttonBox.rejected.connect(self.close)
        buttonBox.accepted.connect(self.generate_gcode)
        v_layout.addWidget(buttonBox)

        self.setLayout(v_layout)

    def generate_gcode(self):
        print("Generate G-code using the chosen settings")