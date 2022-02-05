"""
    Script that sets up QActions for mainWindow QMainWindow.
"""
import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw

import src.settings as settings


def setup_actions():
    mainWindow = settings.globalVars["MainWindow"]
    # Load images action; user selects images from a QFileDialog
    def load_image_from_file():
        new_loaded_images, _ = qtw.QFileDialog.getOpenFileName(
            mainWindow, "Select image to load.", mainWindow.current_image_directory
        )
        mainWindow.set_new_loaded_image_files(new_loaded_images)

    menubar = mainWindow.menuBar()

    """ File menu/toolbar """
    file_menu = menubar.addMenu("&File")

    load_images = qtg.QAction("&Load image", mainWindow)
    load_images.setShortcut("Ctrl+D")
    load_images.setStatusTip("Load image from disk.")
    load_images.triggered.connect(load_image_from_file)
    file_menu.addAction(load_images)

    clear_images = qtg.QAction("&Clear image", mainWindow)
    clear_images.setShortcut("Ctrl+F")
    clear_images.setStatusTip("Clear loaded image.")
    clear_images.triggered.connect(mainWindow.clear_all_images)
    file_menu.addAction(clear_images)

    save_file = qtg.QAction("&Save project", mainWindow)
    save_file.setShortcut(qtg.QKeySequence("Ctrl+S"))
    save_file.setStatusTip("Save a project file to disk.")
    save_file.triggered.connect(mainWindow.save_project_to_file)

    exit = qtg.QAction("&Exit", mainWindow)
    exit.setShortcut(qtg.QKeySequence("Ctrl+W"))
    exit.setStatusTip("Exit from application. You might lose unsaved work!")
    exit.triggered.connect(mainWindow.shutdown_application)
    file_menu.addAction(exit)

    """ Processing menu/toolbar """
    processing_menu = menubar.addMenu("&Processing")

    generate_gcode = qtg.QAction("&Generate G-code", mainWindow)
    generate_gcode.setShortcut("Ctrl+A")
    generate_gcode.setStatusTip("Generate G-code for image.")
    generate_gcode.triggered.connect(mainWindow.generate_gcode)
    processing_menu.addAction(generate_gcode)

    """ Help menu """
    help = menubar.addMenu("&Help")

    qt = qtg.QAction("About &Qt", mainWindow)
    qt.setStatusTip("Information on Qt, the UI framework.")
    qt.triggered.connect(qtw.QApplication.aboutQt)
    help.addAction(qt)
