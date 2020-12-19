#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#! /usr/bin/env python3

"""
Created on 10.11.2020 22:17 CET

@author: zocker_160
"""

import os
import sys
import webbrowser
from io import BytesIO
from PIL import Image
from PyQt5.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QGraphicsScene, QListWidget, QMainWindow, QMessageBox

#import qdarkstyle

from lib import Ui_mainWindow, Ui_viewerWindow, Ui_aboutWindow

from lib.SSTtool.src.lib.SST import SST
from lib.SSAtool.src import SSAtool
from lib.SSTtool.src import SSTtool
from lib.SSTslicer.src import SSTslicer

VERSION = "v0.2.1"
PLACEHOLDER_STR = "$$$"

class AboutWindow(QDialog, Ui_aboutWindow.Ui_Dialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.setupUi(self)

        self.about_maintext.setText( self.about_maintext.text().replace(PLACEHOLDER_STR, VERSION) )

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
            self.showImage(images[0]) # show the first tile of the image list
            self.currImageIndex = 1
            self._setIndexLabel()

    def showImage(self, image: Image):
        #imagePath = os.path.join("/home/bene", "800px-TuxFlat.svg.png")
        #image = Image.open(imagepath)

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
                    imageList.append( Image.open(BytesIO(img)) )
            else:
                imageList.append( Image.open(imagepath) )
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
            self.showImage(self.images[self.currImageIndex-1]) # currImageIndex starts at 1 and the array starts at 0
            self._setIndexLabel()
        else:
            self._checkButtons()

    def prevIndex(self):
        if self.currImageIndex - 1 >= 1:
            self.currImageIndex -= 1
            self.showImage(self.images[self.currImageIndex-1]) # currImageIndex starts at 1 and the array starts at 0
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

class MainWindow(QMainWindow, Ui_mainWindow.Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.gridMax = 10
        self.gridMin = 2

        self.setupUi(self)
        self.initGUIControls()
        self.SLCupdateGridview()
        self.main_infotext.setText( self.main_infotext.text().replace(PLACEHOLDER_STR, VERSION) )

    def initGUIControls(self):
        self.actionOpen_Image_Viewer.triggered.connect(self.showImageViewer)
        self.actionReport_Issue.triggered.connect(self.showReportIssue)
        self.actionHelp_from_GitHUb.triggered.connect(self.showHelp)
        self.actionAbout_Studio_II.triggered.connect(self.showAbout)

        self.tab_ssa_list.onDrop.connect(self.SSAinSelector)
        self.tab_ssa_select_in.clicked.connect(self.SSAinSelector)
        self.tab_ssa_select_out.clicked.connect(self.SSAoutSelector)
        self.tab_ssa_unpack.clicked.connect(self.SSAconvert)

        self.tab_sst_select_in.clicked.connect(self.SSTinSelector)
        self.tab_sst_select_out.clicked.connect(self.SSToutSelector)
        self.tab_sst_input_checkbox.clicked.connect(self.SSTcheckButton)
        self.tab_sst_convert.clicked.connect(self.SSTconvert)
        self.tab_sst_droplabel.onDrop.connect(self.SSTdropHandler)

        self.tab_slc_gridview.onResize.connect(self.SLCupdateGridview)

        self.tab_slc_row_plus.clicked.connect(self._SLCaddRow)            
        self.tab_slc_row_minus.clicked.connect(self._SLCsubRow)
        self.tab_slc_col_plus.clicked.connect(self._SLCaddCol)
        self.tab_slc_col_minus.clicked.connect(self._SLCsubCol)

        self.tab_slc_moveup.clicked.connect(self._SLCmoveItemUp)
        self.tab_slc_movedown.clicked.connect(self._SLCmoveItemDown)
        self.tab_slc_select_in.clicked.connect(self.SLCinSelector)
        self.tab_slc_select_out.clicked.connect(self.SLCoutSelector)
        self.tab_slc_join.clicked.connect(self.SLCjoiner)
        self.tab_slc_slice.clicked.connect(self.SLCslicer)

        #self.testbutton.clicked.connect(self.clickedTestButton)

    ### menu actions
    def showHelp(self):
        webbrowser.open("https://github.com/EE-modders/Empire-Earth-Studio-2")

    def showReportIssue(self):
        webbrowser.open("https://github.com/EE-modders/Empire-Earth-Studio-2/issues")

    ### windows
    def showErrorMSG(self, msg_str: str, title_msg="ERROR"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(msg_str)
        msg.setWindowTitle(title_msg)
        msg.setDefaultButton(QMessageBox.Close)
        msg.exec_()

    def showInfoMSG(self, msg_str: str, title_msg="INFO"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(msg_str)
        msg.setWindowTitle(title_msg)
        msg.setDefaultButton(QMessageBox.Close)
        msg.exec_()

    def showQuestionMSG(self, msg_str: str, title_msg="QUESTION"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText(msg_str)
        msg.setWindowTitle(title_msg)
        msg.addButton(QMessageBox.Yes)
        msg.addButton(QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        
        reply = msg.exec_()

        if reply == QMessageBox.Yes:
            return True
        else:
            return False

    def showImageViewer(self, imagepath: str):
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
                        raise TypeError("ERROR: SST Images from EE BETA are not supported in the viewer!")
                    imageList.append( Image.open(BytesIO(img)) )
            else:
                imageList.append( Image.open(imagepath) )
            filename = os.path.basename(imagepath)
        else:
            filename = ""
            imageList = None

        Viewer = ViewerWindow(self, images=imageList, filename=filename)
        Viewer.show()

    def showAbout(self):
        About = AboutWindow(self)
        About.show()

    ### SSA
    def SSAcheckButton(self):
        if self.tab_ssa_label_in.text() and self.tab_ssa_label_out.text():
            self.tab_ssa_unpack.setEnabled(True)
        else:
            self.tab_ssa_unpack.setEnabled(False)

    def SSAinSelector(self, event):
        # event is not False, when called from CDropWidget
        if not event:
            dlg = QFileDialog.getOpenFileName(
                self,
                caption="Select SSA file",
                filter="SSA Archive (*.ssa)",
            )
        else:
            dlg = event

        print(dlg)

        filepath = dlg[0]

        # add file list to listWidget
        try:
            if self.tab_ssa_kyrillicencode.isChecked():
                filelist = SSAtool.getFileList(filepath, encoding="CP1251")
            else:
                filelist = SSAtool.getFileList(filepath)
            #print(filelist)
        except ImportError as e:
            self.showErrorMSG(e.args[0])
            return
        except FileNotFoundError:
            return

        self.tab_ssa_label_in.setText(filepath)

        # add files to file list
        self.tab_ssa_list.clear()
        for file in filelist:
            self.tab_ssa_list.addItem(file[0])

        self.SSAcheckButton()

    def SSAoutSelector(self):
        dlg = QFileDialog.getExistingDirectory(
            self,
            caption="Select output folder"
        )

        self.tab_ssa_label_out.setText(dlg)
        print(dlg)

        self.SSAcheckButton()

    def SSAconvert(self):
        if self.tab_ssa_kyrillicencode.isChecked():
            encoding = "CP1251"
        else:
            encoding = None

        SSAtool.main(
            inputfile=self.tab_ssa_label_in.text(),
            outputfolder=self.tab_ssa_label_out.text(),
            decompress=self.tab_ssa_decompress.isChecked(),
            log=False,
            encoding=encoding
        )
        self.showInfoMSG("Done!")
        #self.tab_ssa_label_clear.click()


    ### SST
    def SSTinSelector(self):
        dlg = QFileDialog.getExistingDirectory(
            self,
            caption="Select source folder"
        )

        self.tab_sst_label_in.setText(dlg)
        print(dlg)

        self.SSTcheckButton()

    def SSToutSelector(self):
        dlg = QFileDialog.getExistingDirectory(
            self,
            caption="Select destination folder"
        )

        self.tab_sst_label_out.setText(dlg)
        print(dlg)

        self.SSTcheckButton()

    def SSTconvert(self):
        filelist = [ self.tab_sst_label_in.text() ]
        print(filelist)

        if self.tab_sst_radio_1.isChecked():
            selection = "1"
        else:
            selection = "2"

        output = self.SSTcheckOutput()

        try:
            SSTtool.main(
                inputfiles=filelist,
                outputlocation=output,
                selection=selection,
                overwrite=self.tab_sst_overwrite.isChecked(),
                single_res=self.tab_sst_firstonly.isChecked(),
                bundling=False
            )
        except Exception as e:
            self.showErrorMSG(e.args[0])
            return

        if not self.tab_sst_donemessage.isChecked():
            self.showInfoMSG("Done!")

    def _SSTdropConvert(self, filelist: list, ext: str):
        output = self.SSTcheckOutput()
        bundling = not self.tab_sst_bundling.isChecked()

        if ext == ".sst":
            selection = "1"
        else:
            selection = "2"

            if bundling:
                _msg = "Following files will get bundeled into one SST\n"
                _msg += "please confirm this order:\n\n"

                for i, file in enumerate(filelist):
                    _msg += f"[{i+1}] => {os.path.basename(file)}\n"

                if not self.showQuestionMSG(_msg):
                    return

        try:
            SSTtool.main(
                inputfiles=filelist,
                outputlocation=output,
                selection=selection,
                overwrite=self.tab_sst_overwrite.isChecked(),
                single_res=self.tab_sst_firstonly.isChecked(),
                bundling=bundling
            )
        except Exception as e:
            self.showErrorMSG(e.args[0])
            return

        if not self.tab_sst_donemessage.isChecked():
            self.showInfoMSG("Done!")

    def SSTdropHandler(self, event):
        print(event)

        # check if view only is set
        if self.tab_sst_viewonly.isChecked():
            try:
                self.showImageViewer(event[0]) # open only the first dropped file
            except Exception as e:
                self.showErrorMSG(e.args[0])
            finally:
                return

        # check if output is set
        if not self.tab_sst_input_checkbox.isChecked():
            if not self.tab_sst_label_out.text():
                self.showErrorMSG("No output destination specified!")
                return

        # check if all files have the same ext otherwise show error
        ext = os.path.splitext(event[0])[1]

        if any( os.path.splitext(f)[1] != ext for f in event ):
            self.showErrorMSG("All files have to have the same file type!")
            return
        elif ext not in [".sst", ".tga"]:
            self.showErrorMSG("only TGA and SST files are supported")
            return
        else:
            print(ext)

        self._SSTdropConvert(filelist=event, ext=ext)


    def SSTcheckButton(self):
        self.tab_sst_convert.setEnabled(False)
        if self.tab_sst_label_in.text():
            if self.tab_sst_input_checkbox.isChecked() or self.tab_sst_label_out.text():
                self.tab_sst_convert.setEnabled(True)

    def SSTcheckOutput(self):
        if not self.tab_sst_input_checkbox.isChecked():
            return self.tab_sst_label_out.text()
        else:
            return ""

    ### SST Slicer
    def SLCupdateGridview(self):
        maxX = self.tab_slc_gridview.width()
        maxY = self.tab_slc_gridview.height()

        #print(maxX, maxY)

        # update aspect ratio of the GridView, target is 4:3 # does not work for some reason :(
        #if maxX >= maxY:
        #    self.tab_slc_gridview.setMaximumSize(5000, round( (maxX / 4) * 3 ))
        #else:
        #    self.tab_slc_gridview.setMaximumSize(round( (maxY / 3) * 4 ))

        scene = QGraphicsScene(self)
        self.tab_slc_gridview.setScene(scene)

        rows = int(self.tab_slc_row_count.text())
        colums = int(self.tab_slc_col_count.text())

        boxH = maxY // rows
        boxB = maxX // colums

        #scene.addRect(100, -50, maxX, maxY)
        #scene.addLine(0, 0, 0, maxY)
        #scene.addLine(0, 0, 50, 50)
        #scene.addLine(50, 0, 0, 50)
        #scene.addLine(0, 0, 50, 50)

        for r in range(rows):
            scene.addLine( 0, r*boxH, maxX, r*boxH )

        for c in range(colums):
            scene.addLine( c*boxB, 0, c*boxB, maxY )

    def _SLCaddRow(self):
        c = int(self.tab_slc_row_count.text()) + 1
        if c >= self.gridMax:
            self.tab_slc_row_plus.setDisabled(True)
        self.tab_slc_row_minus.setEnabled(True)
        self.tab_slc_row_count.setNum(c)
        self.SLCupdateGridview()

    def _SLCsubRow(self):
        c = int(self.tab_slc_row_count.text()) - 1
        if c <= self.gridMin:
            self.tab_slc_row_minus.setDisabled(True)
        self.tab_slc_row_plus.setEnabled(True)
        self.tab_slc_row_count.setNum(c)
        self.SLCupdateGridview()

    def _SLCaddCol(self):
        c = int(self.tab_slc_col_count.text()) + 1
        if c >= self.gridMax:
            self.tab_slc_col_plus.setDisabled(True)
        self.tab_slc_col_minus.setEnabled(True)
        self.tab_slc_col_count.setNum(c)
        self.SLCupdateGridview()

    def _SLCsubCol(self):
        c = int(self.tab_slc_col_count.text()) - 1
        if c <= self.gridMin:
            self.tab_slc_col_minus.setDisabled(True)
        self.tab_slc_col_plus.setEnabled(True)
        self.tab_slc_col_count.setNum(c)
        self.SLCupdateGridview()

    def _SLCnewInfiles(self, files: list, filetype: str):

        if "tga" in filetype:
            self.tab_slc_label_in.setText(os.path.basename(files[0]))
        else:
            #self.tab_slc_label_in.setText('; '.join( [ os.path.basename(p) for p in files ] ) )
            # or maybe this is better
            pass

        # add files to the file list wiget
        self.tab_slc_list.clear()
        self.tab_slc_list.addItems(files)

        self.tab_slc_label_in.setText(f"{len(files)} file(s) imported")

    def SLCinSelector(self):
        dlg = QFileDialog.getOpenFileNames(
            self,
            caption="Select TGA / SST file(s)",
            filter="SST Image (*.sst);;TGA Image (*.tga)"
        )

        #print(dlg)
        print(dlg[1])

        self._SLCnewInfiles(files=dlg[0], filetype=dlg[1])
        self.SLCcheckButtons()

    def SLCoutSelector(self):
        dlg = QFileDialog.getExistingDirectory(
            self,
            caption="Select destination folder"
        )

        print(dlg)

        self.tab_slc_label_out.setText(dlg)
        self.SLCcheckButtons()

    def SLCjoiner(self):
        inputfiles = [ self.tab_slc_list.item(i).text() for i in range(self.tab_slc_list.count()) ]

        _msg = "Following files will be joined:\n"
        _msg += "Please confirm this order.\n\n"

        for i, file in enumerate(inputfiles):
            _msg += f"[{i+1}] => {os.path.basename(file)}\n"

        if not self.showQuestionMSG(msg_str=_msg, title_msg="Please confirm"):
            return
        else:
            self.SLCslicer()


    def SLCslicer(self):
        inputfiles = [ self.tab_slc_list.item(i).text() for i in range(self.tab_slc_list.count()) ]

        # all files have to have the same file type at this point, so we can do this
        if ".sst" in inputfiles[0]:
            fileType = "sst"
        else:
            fileType = "tga"

        try:
            SSTslicer.main(
                inputfiles=inputfiles,
                outputlocation=self.tab_slc_label_out.text(),
                filetype=fileType,
                xTiles=int(self.tab_slc_col_count.text()),
                yTiles=int(self.tab_slc_row_count.text())
            )
        except Exception as e:
            self.showErrorMSG(e.args[0])
            return

        self.showInfoMSG("Done!")

    def SLCcheckButtons(self):
        nListItems = self.tab_slc_list.count()

        if nListItems > 1:
            self.tab_slc_join.setEnabled(True)
            self.tab_slc_slice.setEnabled(False)
        elif nListItems == 1:
            self.tab_slc_join.setEnabled(False)
            self.tab_slc_slice.setEnabled(True)
        else:
            self.tab_slc_join.setEnabled(False)
            self.tab_slc_slice.setEnabled(False)

    def _SLCmoveItemDown(self):
        currRow = self.tab_slc_list.currentRow()
        currItem = self.tab_slc_list.takeItem(currRow)
        newRow = currRow + 1
        self.tab_slc_list.insertItem(newRow, currItem)
        self.tab_slc_list.setCurrentRow(newRow)

    def _SLCmoveItemUp(self):
        currRow = self.tab_slc_list.currentRow()
        currItem = self.tab_slc_list.takeItem(currRow)
        newRow = currRow - 1
        self.tab_slc_list.insertItem(newRow, currItem)
        self.tab_slc_list.setCurrentRow(newRow)

    ### CEM

    ### TEST
    def test(self, event=None):
        print("nice")
        print(event)


def main():
    app = QApplication(sys.argv)
    #app.setStyleSheet(qdarkstyle.load_stylesheet())

    main_Window = MainWindow()
    main_Window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    # this is only needed for the CI / CD
    try:
        testmode = sys.argv[1] == "-v"
    except:
        testmode = False

    if testmode:
        print("STARTED!")
        sys.exit()
    else:
        main()
