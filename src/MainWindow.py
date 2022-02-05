"""
    Script that houses the MainWindow class.
    It is the "root display".
"""
import os
import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw
import qt_material

import src.QActionsSetup as qt_actions_setup
import ImageViewer as ImageViewer
import src.settings as settings


class MainWindow(qtw.QMainWindow, qt_material.QtStyleTools):
    loaded_image_names = []
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
        self.resize(geometry.width(), geometry.height())

        qt_actions_setup.setup_actions()
        self.setCentralWidget(ImageViewer.MainLayout())

        # Stylesheet
        # TODO: Make setting toggle that saves stylesheet
        self.apply_stylesheet(self, "dark_blue.xml")

    # Clear all loaded images
    def clear_all_images(self):
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

    # Shutdown all currently running processes, cleanup and close window
    def shutdown_application(self):
        self.close()