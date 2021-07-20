# -*- coding: utf-8 -*-

"""This module provides the Renamer main window."""

from collections import deque
from pathlib import Path
from inspect import getsourcefile
from os.path import abspath
import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QMovie
import imghdr

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QFileDialog, QWidget

from PyQt5 import QtWidgets, QtGui, QtCore

from .ui.window import Ui_Window

FILTERS = ";;".join(
    (
        "JPG Files (*.jpg)",
        "PNG Files (*.png)",
        "JPEG Files (*.jpeg)",
        "GIF Files (*.gif)",
    )
)

class Window(Ui_Window, QtWidgets.QWidget):
    selectedMediums = []
    selectedStyles = []
    selectedSubjects = []
    selectedAspects = []
    selectedCreators = []
    selectedInspiring = []
    selectedNSFW = []
    selectedNewTags = []
    selectedCreatorsName = ""

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self._current_index = 0
        self._files = deque()
        self._filesCount = len(self._files)
        self._extension = ""
        self._setupUI()
        self._connectSignalsSlots()
        self.addTagButton.clicked.connect(self.newTagName.clear)
        self.checkBoxes = self.mediumsBox.findChildren(QtWidgets.QCheckBox) + self.stylesBox.findChildren(QtWidgets.QCheckBox) + self.subjectsBox.findChildren(QtWidgets.QCheckBox) + self.aspectsBox.findChildren(QtWidgets.QCheckBox) + self.creatorsBox.findChildren(QtWidgets.QCheckBox) + self.inspiringBox.findChildren(QtWidgets.QCheckBox) + self.nsfwBox.findChildren(QtWidgets.QCheckBox) + self.newTagsBox.findChildren(QtWidgets.QCheckBox)

    def addCheckbox(self):
        if self.newTagName.text() == "":
            return
        checkBox = QtWidgets.QCheckBox(self.newTagName.text())
        checkBox.clicked.connect(self.newTagsClicked)
        self.checkBoxes.append(checkBox)
        self.gridLayout_9.addWidget(checkBox)

    def clearCheckboxes(self, false):
        for checkBox in self.checkBoxes:
            checkBox.setChecked(false)
        self.selectedMediums = []
        self.selectedStyles = []
        self.selectedSubjects = []
        self.selectedAspects = []
        self.selectedCreators = []
        self.selectedInspiring = []
        self.selectedNSFW = []
        self.selectedNewTags = []
        self.setNewFilename()

    def _setupUI(self):
        self.setupUi(self)
        self._updateStateWhenNoFiles()

    def _updateStateWhenNoFiles(self):
        self._filesCount = len(self._files)
        self.loadFilesButton.setEnabled(True)
        self.loadFilesButton.setFocus(True)

    def mediumsClicked(self):
        self.selectedMediums = []
        for w in self.mediumsBox.findChildren(QtWidgets.QCheckBox):
            if w.isChecked():
                self.selectedMediums.append(w.text().replace("&", ""))
        self.setNewFilename()

    def stylesClicked(self):
        self.selectedStyles = []
        for w in self.stylesBox.findChildren(QtWidgets.QCheckBox):
            if w.isChecked():
                self.selectedStyles.append(w.text().replace("&", ""))
        self.setNewFilename()

    def subjectsClicked(self):
        self.selectedSubjects = []
        for w in self.subjectsBox.findChildren(QtWidgets.QCheckBox):
            if w.isChecked():
                self.selectedSubjects.append(w.text().replace("&", ""))
        self.setNewFilename()

    def aspectsClicked(self):
        self.selectedAspects = []
        for w in self.aspectsBox.findChildren(QtWidgets.QCheckBox):
            if w.isChecked():
                self.selectedAspects.append(w.text().replace("&", ""))
        self.setNewFilename()

    def creatorsClicked(self):
        self.selectedCreators = []
        for w in self.creatorsBox.findChildren(QtWidgets.QCheckBox):
            if w.isChecked():
                self.selectedCreators.append(w.text().replace("&", ""))
        self.setNewFilename()

    def inspiringClicked(self):
        self.selectedInspiring = []
        for w in self.inspiringBox.findChildren(QtWidgets.QCheckBox):
            if w.isChecked():
                self.selectedInspiring.append(w.text().replace("&", ""))
        self.setNewFilename()

    def nsfwClicked(self):
        self.selectedNSFW = []
        for w in self.nsfwBox.findChildren(QtWidgets.QCheckBox):
            if w.isChecked():
                self.selectedNSFW.append(w.text().replace("&", ""))
        self.setNewFilename()

    def newTagsClicked(self):
        self.selectedNewTags = []
        for w in self.newTagsBox.findChildren(QtWidgets.QCheckBox):
            if w.isChecked():
                self.selectedNewTags.append(w.text().replace("&", ""))
        self.setNewFilename()

    def _connectSignalsSlots(self):
        self.loadFilesButton.clicked.connect(self.loadFiles)
        self.renameButton.clicked.connect(self.renameFiles)
        self.addTagButton.clicked.connect(self.addCheckbox)
        self.uncheckAllTagsButton.clicked.connect(self.clearCheckboxes)
        self.previousImageButton.clicked.connect(self.handle_previous)
        self.nextImageButton.clicked.connect(self.handle_next)
        #self.nextImageButton.clicked.connect(self.createNewFilename)
        #self.nextImageButton.clicked.connect(self.getExtension)
        #self.prefixEdit.textChanged.connect(self._updateStateWhenReady)
        for w in self.mediumsBox.findChildren(QtWidgets.QCheckBox):
            w.clicked.connect(self.mediumsClicked)
        for w in self.stylesBox.findChildren(QtWidgets.QCheckBox):
            w.clicked.connect(self.stylesClicked)
        for w in self.subjectsBox.findChildren(QtWidgets.QCheckBox):
            w.clicked.connect(self.subjectsClicked)
        for w in self.aspectsBox.findChildren(QtWidgets.QCheckBox):
            w.clicked.connect(self.aspectsClicked)
        for w in self.creatorsBox.findChildren(QtWidgets.QCheckBox):
            w.clicked.connect(self.creatorsClicked)
        for w in self.inspiringBox.findChildren(QtWidgets.QCheckBox):
            w.clicked.connect(self.inspiringClicked)
        for w in self.nsfwBox.findChildren(QtWidgets.QCheckBox):
            w.clicked.connect(self.nsfwClicked)
        for w in self.newTagsBox.findChildren(QtWidgets.QCheckBox):
            w.clicked.connect(self.newTagsClicked)
        self.creatorsName.textChanged.connect(self.creatorsNameChanged)

    def creatorsNameChanged(self):
        self.selectedCreatorsName = self.creatorsName.text()
        self.setNewFilename()

    def setNewFilename(self):
        self.newFileName.setText(self.createNewFilename())

    def loadFiles(self):
        if self.sourceDirectory.text():
            initDir = self.sourceDirectory.text()
        else:
            initDir = str(Path.home())
        files, filter = QFileDialog.getOpenFileNames(
            self, "Choose Files to Rename", initDir, filter=FILTERS
        )
        if len(files) > 0:
            sourceDirectory = str(Path(files[0]).parent)
            self.sourceDirectory.setText(sourceDirectory)
            for file in files:
                self._files.append(Path(file))
            self._filesCount = len(self._files)
            self._filenames = files
            self.current_index = 0
            fullpath, extension = os.path.splitext(files[0])
            self._extension = extension
            self.setNewFilename()

    def handle_next(self):
        self.current_index += 1

    def handle_previous(self):
        self.current_index -= 1

    @property
    def current_index(self):
        return self._current_index

    @current_index.setter
    def current_index(self, index):
        if index <= 0:
            self._update_button_status(False, True)
        elif index >= (len(self._filenames) - 1):
            self._update_button_status(True, False)
        else:
            self._update_button_status(True, True)

        if 0 <= index < len(self._filenames):
            self._current_index = index
            filename = self._filenames[self._current_index]
            if  imghdr.what(filename) == "gif":
                self.movie = QMovie(filename)
                self.imageFrameLabel.setMovie(self.movie)
                self.imageFrameLabel.setMinimumSize(1, 1)
                self.movie.start()
            else:
                pixmap = QPixmap(filename)
                pixmap = pixmap.scaled(self.imageFrameLabel.size(), QtCore.Qt.KeepAspectRatio)
                self.pixmap = QtGui.QPixmap(filename)
                self.imageFrameLabel.setPixmap (pixmap)
                self.imageFrameLabel.setMinimumSize(1, 1)
            basename = os.path.basename(filename)
            currentFileName = basename
            self.currentFileName.setText(currentFileName)
            self._currentFilename = currentFileName

    def renameFiles(self):
        path = os.path.dirname(self._filenames[self._current_index])
        newFilename = self.newFileName.text()
        if len(newFilename) > 5:
            newFilename = os.path.join(path, newFilename)
            existingfilenames = os.listdir(path)

            newFileCounter = 0

            for justFilename in existingfilenames:
              filename = os.path.join(path, justFilename)
              if not os.path.isfile(filename):
                continue
              splittedFilename = filename.split(".")
              maybeFileCounter = splittedFilename[len(splittedFilename) - 2]
              print("=> filename: " + filename + " (maybeFileCounter: " + maybeFileCounter + ")")
              testFilename = filename
              fileCounter = 0
              if maybeFileCounter.isnumeric():
                print("  => hasNumber")
                extension = splittedFilename[len(splittedFilename) - 1]
                skipLastCharsNo = len(extension) + 1 + len(maybeFileCounter) + 1
                print("  => skipChars: " + str(skipLastCharsNo))
                testFilename = filename[:-skipLastCharsNo] + "." + extension
                fileCounter = int(maybeFileCounter)
              print("=> testname: " + testFilename + " (fileCounter: " + str(fileCounter) + ")")
              if testFilename == newFilename and fileCounter >= newFileCounter:
                  newFileCounter = fileCounter + 1
                  print("=> newCounter: " + str(newFileCounter))

            if newFileCounter > 0:
              splittedFilename = newFilename.split(".")
              extension = splittedFilename[len(splittedFilename) - 1]
              newFilename = newFilename[:-(len(extension))] + str(newFileCounter) + "." + extension

            print("=> newFilename: " + newFilename)
        else:
            print("Too few letters in the filename, try again.")


        filename = self._filenames[self._current_index]
        filenamestatus = os.path.basename(newFilename)

        if filenamestatus.startswith('.'):
            self.currentFileName.setText("Creator's name needs to be inserted, try again.")
        else:
            if len(newFilename) > 5:
                onlyfilename = os.path.basename(newFilename)
                self.currentFileName.setText(onlyfilename)
                os.replace(filename,newFilename)
                self._filenames[self._current_index] = newFilename
                #self.creatorsName.setText("")
            else:
                self.currentFileName.setText("Too few letters in the filename, try again.")


    def createNewFilename(self):
        extension = self._extension
        newFilename = self.selectedCreatorsName.replace(" ", "_")
        if len(self.selectedMediums) > 0 or len(self.selectedStyles) > 0 or len(self.selectedSubjects) > 0 or len(self.selectedAspects) > 0 or len(self.selectedCreators) > 0 or len(self.selectedInspiring) > 0 or len(self.selectedNSFW) > 0 or len(self.selectedNewTags) > 0:
            newFilename = newFilename + "."
        newFilename = newFilename + "_".join(self.selectedMediums + self.selectedStyles + self.selectedSubjects + self.selectedAspects + self.selectedCreators + self.selectedInspiring + self.selectedNSFW + self.selectedNewTags)
        return newFilename + extension

    def _update_button_status(self, previous_enable, next_enable):
        self.previousImageButton.setEnabled(previous_enable)
        self.nextImageButton.setEnabled(next_enable)
