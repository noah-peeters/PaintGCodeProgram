"""
    Script that houses the MainWindow class.
    It is the "root display".
"""
import os
import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw
import qt_material

import src.QActionsSetup as qt_actions_setup
import src.MainLayout as MainLayout
import src.settings as settings


class MainWindow(qtw.QMainWindow, qt_material.QtStyleTools):
    loaded_image_names = []
    # Reference dir for image loading/export
    current_image_directory = os.path.expanduser("~")

    def __init__(self):
        super().__init__()
        settings.globalVars["MainWindow"] = self

        self.statusbar_msg_display_time = 2000  # (ms)

        self.setWindowTitle("ChimpStackr")
        geometry = self.screen().availableGeometry()
        self.setMinimumSize(int(geometry.width() * 0.6), int(geometry.height() * 0.6))
        self.resize(geometry.width(), geometry.height())

        qt_actions_setup.setup_actions()
        self.setCentralWidget(MainLayout.MainLayout())

        # Stylesheet
        # TODO: Make setting toggle that saves stylesheet
        self.apply_stylesheet(self, "dark_blue.xml")

    # Export output image to file on disk
    def export_output_image(self):
        if self.LaplacianAlgorithm.output_image is not None:
            outputFilePath, usedFilter = qtw.QFileDialog.getSaveFileName(
                self,
                "Export stacked image",
                self.current_image_directory,
                "JPEG (*.jpg *.jpeg);; PNG (*.png);; TIFF (*.tiff *.tif)",
            )
            if outputFilePath:
                outputFilePath = os.path.abspath(outputFilePath)
                self.current_image_directory = os.path.dirname(outputFilePath)

                self.statusBar().showMessage(
                    "Exporting output image...", self.statusbar_msg_display_time
                )

                # Get used image type from filter
                imgType = None
                if usedFilter == "JPEG (*.jpg *.jpeg)":
                    imgType = "JPG"
                elif usedFilter == "PNG (*.png)":
                    imgType = "PNG"
                elif usedFilter == "TIFF (*.tiff *.tif)":
                    imgType = "TIFF"

                ImageSavingDialog.createDialog(
                    self.LaplacianAlgorithm.output_image, imgType, outputFilePath
                )

        else:
            # Display Error message
            msg = qtw.QMessageBox(self)
            msg.setStandardButtons(qtw.QMessageBox.Ok)
            msg.setIcon(qtw.QMessageBox.Critical)
            msg.setWindowTitle("Export failed")
            msg.setText("Failed to export!\nPlease load images first.\n")
            msg.show()

    # Clear all loaded images
    def clear_all_images(self):
        if len(self.LaplacianAlgorithm.image_paths) > 0:
            # Ask confirmation (if there are loaded images)
            reply = qtw.QMessageBox.question(
                self,
                "Clear images?",
                "Are you sure you want to clear all loaded images? Output image(s) will be cleared to!",
                qtw.QMessageBox.Cancel,
                qtw.QMessageBox.Ok,
            )
            if reply == qtw.QMessageBox.Ok:
                self.statusBar().showMessage(
                    "Clearing images...", self.statusbar_msg_display_time
                )
                # Clear loaded and processed images from list
                self.centralWidget().add_processed_image(None)
                return True
            else:
                return False
        else:
            # No images were originally loaded
            return True

    # TODO: Dragging a folder gives an error; use contents of folder (if valid images)
    # Update loaded image files
    def set_new_loaded_image_files(self, new_loaded_images):
        if len(new_loaded_images) > 0:
            if self.clear_all_images() == False:
                return

            # TODO: Check if valid (and same??) format; discard unsupported formats + show warning saying what images were discarded
            self.statusBar().showMessage(
                "Loading images...", self.statusbar_msg_display_time
            )
            self.current_image_directory = os.path.dirname(new_loaded_images[0])
            self.centralWidget().set_loaded_images(new_loaded_images)
            self.LaplacianAlgorithm.update_image_paths(new_loaded_images)

    # Shutdown all currently running processes, cleanup and close window
    def shutdown_application(self):
        self.close()