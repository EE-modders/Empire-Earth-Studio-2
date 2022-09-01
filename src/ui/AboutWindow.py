#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 10.11.2020 22:17 CET

@author: zocker_160
"""

from ui import Ui_aboutWindow
from lib import Util

from PyQt5.QtWidgets import QDialog


class AboutWindow(QDialog, Ui_aboutWindow.Ui_Dialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setupUi(self)
        self.icon_label.setPixmap(Util.getLogoPixmap())
        self.about_maintext.setText(Util.setPlaceholders(self.about_maintext.text()))
