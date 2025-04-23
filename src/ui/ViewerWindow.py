#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 10.11.2020 22:17 CET

@author: zocker_160
"""

import os
from io import BytesIO

from PIL import Image

from PyQt5.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent
from PyQt5.QtWidgets import QDialog, QMessageBox

from ui import Ui_viewerWindow
from lib.SST import SST

class ViewerWindow(QDialog, Ui_viewerWindow.Ui_Dialog):
    def __init__(self, parent, images: list, filename: str = "") -> None:
        super().__init__(parent)

        self.setupUi(self)
        self.view_nextTile.clicked.connect(self.nextIndex)
        self.view_prevTile.clicked.connect(self.prevIndex)

        self.currImageIndex = 0
        self.images = images

        self.initImage(images, filename)

    def initImage(self, images: list, filename: str):
        if filename:
            self.view_label_filename.setText(filename)
        else:
            self.view_label_filename.setText("DRAG & DROP the image!")

        if images:
            # convert 24bit images to 32bit (weird bugs otherwise)
            for i, img in enumerate(images):
                if img.mode == "RGB":
                    a_channel = Image.new('L', img.size, 255)
                    images[i].putalpha(a_channel)

            self.images = images
            self.showImage(images[0])  # show the first tile of the image list
            self.currImageIndex = 1
            self._setIndexLabel()

    def showImage(self, image: Image):
        # imagePath = os.path.join("/home/bene", "800px-TuxFlat.svg.png")
        # image = Image.open(imagepath)

        self.view_image_rgb.setImage(image)
        self.view_image_alpha.setImage(image.split()[-1])

        self._setResLabel(image)

    ### mouse move and drop events
    def dragEnterEvent(self, a0: QDragEnterEvent) -> None:
        if a0.mimeData().hasUrls():
            a0.accept()

    def dragMoveEvent(self, a0: QDragMoveEvent) -> None:
        a0.accept()

    def dropEvent(self, a0: QDropEvent) -> None:
        files = [u.toLocalFile() for u in a0.mimeData().urls()]
        imagepath = files[0]

        # check if file tye is SST
        if imagepath:
            imageList = list()
            if imagepath.endswith("sst"):
                SSText = SST()
                SSText.read_from_file(imagepath)
                imageData = SSText.unpack()
                imageTiles = imageData.get_Image_parts()

                for img in imageTiles:
                    if isinstance(img, tuple):
                        self.showErrorMSG("ERROR: SST Images from EE BETA are not supported in the viewer!")
                        return
                    imageList.append(Image.open(BytesIO(img)))
            else:
                imageList.append(Image.open(imagepath))
        else:
            imagepath = ""
            imageList = None

        self.initImage(images=imageList, filename=os.path.basename(imagepath))

    ###

    def _setResLabel(self, image):
        xRes, yRes = image.width, image.height

        self.view_res_rgb.setText(f"{xRes} x {yRes}")
        self.view_res_alpha.setText(f"{xRes} x {yRes}")

    def _setIndexLabel(self):
        self.view_label_tiles.setText(f"{self.currImageIndex} / {len(self.images)}")
        self._checkButtons()

    def _checkButtons(self):
        # check buttons
        if self.currImageIndex == 1:
            self.view_prevTile.setEnabled(False)
            self.view_nextTile.setEnabled(True)
        elif self.currImageIndex == len(self.images):
            self.view_prevTile.setEnabled(True)
            self.view_nextTile.setEnabled(False)
        else:
            self.view_prevTile.setEnabled(True)
            self.view_nextTile.setEnabled(True)

        # disable all buttons, when image has only one tile
        if len(self.images) == 1:
            self.view_prevTile.setEnabled(False)
            self.view_nextTile.setEnabled(False)

    def nextIndex(self):
        if self.currImageIndex + 1 <= len(self.images):
            self.currImageIndex += 1
            self.showImage(self.images[self.currImageIndex - 1])  # currImageIndex starts at 1 and the array starts at 0
            self._setIndexLabel()
        else:
            self._checkButtons()

    def prevIndex(self):
        if self.currImageIndex - 1 >= 1:
            self.currImageIndex -= 1
            self.showImage(self.images[self.currImageIndex - 1])  # currImageIndex starts at 1 and the array starts at 0
            self._setIndexLabel()
        else:
            self._checkButtons()

    def showErrorMSG(self, msg_str: str, title_msg="ERROR"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(msg_str)
        msg.setWindowTitle(title_msg)
        msg.setDefaultButton(QMessageBox.Close)
        msg.exec_()
