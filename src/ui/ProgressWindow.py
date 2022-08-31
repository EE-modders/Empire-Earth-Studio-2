#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 31.08.2022 00:49 CET

@author: zocker_160
"""

from ui import Ui_progressWindow

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal

class ProgressWindow(QDialog, Ui_progressWindow.Ui_Dialog):

    onShow = pyqtSignal()
    onClose = pyqtSignal()
    onNewProgress = pyqtSignal(int, int, str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)

        self.onShow.connect(self.show)
        self.onClose.connect(self.close)
        self.onNewProgress.connect(self.setProgress)

    def setProgress(self, current: int, total: int, filename: str):
        self.progressBar.setValue(int((current / total)*100))
        self.label_filename.setText(filename)
