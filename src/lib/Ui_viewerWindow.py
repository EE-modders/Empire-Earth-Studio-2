# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/bene/Windows_Daten/Programmierung_Modding/Empire Earth/GitHub/Empire-Earth-Studio-2/src/lib/viewerWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(760, 448)
        Dialog.setAcceptDrops(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.view_image_alpha = CImageLabel(Dialog)
        self.view_image_alpha.setMinimumSize(QtCore.QSize(256, 256))
        self.view_image_alpha.setText("")
        self.view_image_alpha.setAlignment(QtCore.Qt.AlignCenter)
        self.view_image_alpha.setObjectName("view_image_alpha")
        self.gridLayout.addWidget(self.view_image_alpha, 1, 1, 1, 1)
        self.view_image_rgb = CImageLabel(Dialog)
        self.view_image_rgb.setMinimumSize(QtCore.QSize(256, 256))
        self.view_image_rgb.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0.993, y1:0.993, x2:1, y2:1, stop:0.505164 rgba(88, 88, 88, 255), stop:0.55493 rgba(172, 172, 172, 255), stop:1 rgba(172, 172, 172, 255))")
        self.view_image_rgb.setText("")
        self.view_image_rgb.setAlignment(QtCore.Qt.AlignCenter)
        self.view_image_rgb.setObjectName("view_image_rgb")
        self.gridLayout.addWidget(self.view_image_rgb, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.view_res_rgb = QtWidgets.QLabel(Dialog)
        self.view_res_rgb.setMaximumSize(QtCore.QSize(16777215, 30))
        self.view_res_rgb.setAlignment(QtCore.Qt.AlignCenter)
        self.view_res_rgb.setObjectName("view_res_rgb")
        self.gridLayout.addWidget(self.view_res_rgb, 2, 0, 1, 1)
        self.view_res_alpha = QtWidgets.QLabel(Dialog)
        self.view_res_alpha.setMaximumSize(QtCore.QSize(16777215, 30))
        self.view_res_alpha.setAlignment(QtCore.Qt.AlignCenter)
        self.view_res_alpha.setObjectName("view_res_alpha")
        self.gridLayout.addWidget(self.view_res_alpha, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.view_prevTile = QtWidgets.QPushButton(Dialog)
        self.view_prevTile.setMaximumSize(QtCore.QSize(16777215, 25))
        self.view_prevTile.setObjectName("view_prevTile")
        self.horizontalLayout.addWidget(self.view_prevTile)
        self.view_label_tiles = QtWidgets.QLabel(Dialog)
        self.view_label_tiles.setMinimumSize(QtCore.QSize(40, 0))
        self.view_label_tiles.setMaximumSize(QtCore.QSize(16777215, 30))
        self.view_label_tiles.setAlignment(QtCore.Qt.AlignCenter)
        self.view_label_tiles.setObjectName("view_label_tiles")
        self.horizontalLayout.addWidget(self.view_label_tiles)
        self.view_nextTile = QtWidgets.QPushButton(Dialog)
        self.view_nextTile.setMaximumSize(QtCore.QSize(16777215, 25))
        self.view_nextTile.setObjectName("view_nextTile")
        self.horizontalLayout.addWidget(self.view_nextTile)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Empire Earth Studio II - Image Viewer"))
        self.label.setText(_translate("Dialog", "RGBA image"))
        self.label_2.setText(_translate("Dialog", "alpha channel"))
        self.view_res_rgb.setText(_translate("Dialog", "0 x 0"))
        self.view_res_alpha.setText(_translate("Dialog", "0 x 0"))
        self.view_prevTile.setText(_translate("Dialog", "<--"))
        self.view_label_tiles.setText(_translate("Dialog", "0 / 0"))
        self.view_nextTile.setText(_translate("Dialog", "-->"))
from .customwidgets import CImageLabel
