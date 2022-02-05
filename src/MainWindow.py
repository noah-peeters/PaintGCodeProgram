"""
    Script that houses the MainWindow class.
    It is the "root display".
"""
import os
import cv2
import PySide6.QtWidgets as qtw
import qt_material

import src.QActionsSetup as qt_actions_setup
import src.MainLayout as MainLayout
import src.settings as settings


class MainWindow(qtw.QMainWindow, qt_material.QtStyleTools):
    # Reference dir for image loading/export
    current_image_directory = os.path.expanduser("~")
    loaded_image = None

    def __init__(self):
        super().__init__()
        settings.globalVars["MainWindow"] = self

        self.statusbar_msg_display_time = 2000  # (ms)

        self.setWindowTitle("GCode generator")
        geometry = self.screen().availableGeometry()
        self.setMinimumSize(int(geometry.width() * 0.6), int(geometry.height() * 0.6))

        qt_actions_setup.setup_actions()
        self.setCentralWidget(MainLayout.MainLayout())

        # Stylesheet
        # TODO: Make setting toggle that saves stylesheet
        self.apply_stylesheet(self, "dark_blue.xml")

    # Clear loaded image
    def clear_loaded_image(self):
        if self.loaded_image != None:
            # Ask confirmation (if there is an image loaded)
            reply = qtw.QMessageBox.question(
                self,
                "Clear image?",
                "Are you sure you want to clear the loaded image?",
                qtw.QMessageBox.Cancel,
                qtw.QMessageBox.Ok,
            )
            if reply == qtw.QMessageBox.Ok:
                self.statusBar().showMessage(
                    "Clearing image...", self.statusbar_msg_display_time
                )
                # Remove from display
                self.loaded_image = None
                self.centralWidget().imageViewer.set_displayed_image(self.loaded_image)
                return True
            else:
                return False

    # TODO: Allow save to file
    def save_project_to_file(self):
        print("Saving project to file.")

    # TODO: Open dialog for gcode generation/saving
    def generate_gcode(self):
        print("Opening dialog")

    # TODO: Support for "svg" format
    def load_image_from_path(self, path):
        newImage = None
        stackTrace = None
        try:
            newImage = cv2.imread(path)
        except Exception as e:
            stackTrace = e
        
        if newImage is not None:
            self.loaded_image = newImage
            self.centralWidget().imageViewer.set_displayed_image(self.loaded_image)
        else:
            # Display Error message
            msg = qtw.QMessageBox(self)
            msg.setStandardButtons(qtw.QMessageBox.Ok)
            msg.setIcon(qtw.QMessageBox.Critical)
            msg.setWindowTitle("Image loading failed")
            msg.setText(
                "Failed to load image!\nPlease ensure the image's format is supported.\n"
            )
            if stackTrace != None:
                msg.setDetailedText(stackTrace)
            msg.show()

    # Shutdown all currently running processes, cleanup and close window
    def shutdown_application(self):
        self.close()