"""
    Script that sets up QActions for mainWindow QMainWindow.
"""
import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw

import src.settings as settings


def setup_actions():
    mainWindow = settings.globalVars["MainWindow"]
    # Load images action; user selects images from a QFileDialog
    def load_images_from_file():
        new_loaded_images, _ = qtw.QFileDialog.getOpenFileNames(
            mainWindow, "Select images to load.", mainWindow.current_image_directory
        )
        mainWindow.set_new_loaded_image_files(new_loaded_images)

    menubar = mainWindow.menuBar()

    """ File menu/toolbar """
    file_menu = menubar.addMenu("&File")

    load_images = qtg.QAction("&Load images", mainWindow)
    load_images.setShortcut("Ctrl+D")
    load_images.setStatusTip("Load images from disk.")
    load_images.triggered.connect(load_images_from_file)
    file_menu.addAction(load_images)

    clear_images = qtg.QAction("&Clear images", mainWindow)
    clear_images.setShortcut("Ctrl+F")
    clear_images.setStatusTip("Clear all loaded images.")
    clear_images.triggered.connect(mainWindow.clear_all_images)
    file_menu.addAction(clear_images)

    export_image = qtg.QAction("E&xport image", mainWindow)
    export_image.setShortcut("Ctrl+E")
    export_image.setStatusTip("Export output image.")
    export_image.triggered.connect(mainWindow.export_output_image)
    file_menu.addAction(export_image)

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

    # align = qtg.QAction("&Align images", mainWindow)
    # align.setShortcut("Ctrl+A")
    # align.setStatusTip("Align loaded images.")
    # align.triggered.connect(mainWindow.load_images_from_file)
    # processing.addAction(align)

    align_and_stack = qtg.QAction("&Align and stack images", mainWindow)
    align_and_stack.setShortcut("Ctrl+A")
    align_and_stack.setStatusTip("Align and stack loaded images.")
    align_and_stack.triggered.connect(mainWindow.align_and_stack_loaded_images)
    processing_menu.addAction(align_and_stack)

    stack = qtg.QAction("&Stack images", mainWindow)
    stack.setShortcut("Ctrl+Alt+C")
    stack.setStatusTip("Stack loaded images.")
    stack.triggered.connect(mainWindow.stack_loaded_images)
    processing_menu.addAction(stack)

    """ Help menu """
    help = menubar.addMenu("&Help")

    qt = qtg.QAction("About &Qt", mainWindow)
    qt.setStatusTip("Information on Qt, the UI framework.")
    qt.triggered.connect(qtw.QApplication.aboutQt)
    help.addAction(qt)
