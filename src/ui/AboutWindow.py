#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 10.11.2020 22:17 CET

@author: zocker_160
"""

from lib import constants as c
from ui import Ui_aboutWindow

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon, QPixmap


class AboutWindow(QDialog, Ui_aboutWindow.Ui_Dialog):
    def __init__(self, parent, icon: QIcon = None, logo: QPixmap = None):
        super().__init__(parent)

        self.setupUi(self)
        self.setWindowIcon(icon)
        self.icon_label.setPixmap(logo)
        self.about_maintext.setText(self.about_maintext.text().replace(c.PLACEHOLDER_STR, c.VERSION))
