#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 10.11.2020 22:17 CET

@author: zocker_160
"""

import os
import sys
from io import BytesIO
from PIL import Image

from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QGraphicsScene,
    QMainWindow
)

from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon, QPixmap

from ui import Ui_mainWindow
from ui.ViewerWindow import ViewerWindow
from ui.AboutWindow import AboutWindow
from ui.ProgressWindow import ProgressWindow

from lib.SSA.SSA import SSA
from lib.SSA.DCL import DCL

from lib.SSTtool.src.lib.SST import SST
from lib.SSTtool.src import SSTtool
from lib.SSTslicer.src import SSTslicer

from lib import Util
from lib import constants as c


class MainWindow(QMainWindow, Ui_mainWindow.Ui_MainWindow):
    def __init__(self, app: QApplication) -> None:
        super().__init__()

        self.app = app

        self.gridMax = 50
        self.gridMin = 2

        self.setupUi(self)
        self.setWindowIcon(QIcon(c.ICON_PATH))
        self.initGUIControls()
        self.SLCupdateGridview()
        self.main_infotext.setText(Util.setPlaceholders(self.main_infotext.text()))

        # fields for parsed data instances
        self.tab_ssa_SSA: SSA = None

    def initGUIControls(self):
        self.actionOpen_Image_Viewer.triggered.connect(self.showImageViewer)
        self.actionReport_Issue.triggered.connect(Util.showReportIssue)
        self.actionHelp_from_GitHUb.triggered.connect(Util.showHelp)
        self.actionAbout_Studio_II.triggered.connect(self.showAbout)
        self.actionabout_QT.triggered.connect(self.app.aboutQt)

        self.tab_ssa_list.onDrop.connect(self.SSAinSelector)
        self.tab_ssa_list_export.clicked.connect(self.SSAexportList)
        self.tab_ssa_select_in.clicked.connect(self.SSAinSelector)
        self.tab_ssa_select_out.clicked.connect(self.SSAoutSelector)
        self.tab_ssa_unpack_all.clicked.connect(self.SSAconvertAll)
        self.tab_ssa_unpack_one.clicked.connect(self.SSAconvertOne)

        self.subtab_ssa_keylist.itemSelectionChanged.connect(self.SSAmetadataUpdate)
        self.subtab_ssa_load.clicked.connect(self.SSAinSelector)

        self.tab_dcl_select_in.clicked.connect(self.DCLinSelector)
        self.tab_dcl_select_out.clicked.connect(self.DCLoutSelector)
        self.tab_dcl_decompress.clicked.connect(self.DCLdecompress)

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

        # self.testbutton.clicked.connect(self.clickedTestButton)

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
                    imageList.append(Image.open(BytesIO(img)))
            else:
                imageList.append(Image.open(imagepath))
            filename = os.path.basename(imagepath)
        else:
            filename = ""
            imageList = None

        Viewer = ViewerWindow(self, images=imageList, filename=filename)
        Viewer.show()

    def showAbout(self):
        AboutWindow(self, QIcon(c.LOGO_PATH), QPixmap(c.LOGO_PATH)).show()

    ### SSA
    def SSAcheckButton(self):
        if self.tab_ssa_label_in.text() and self.tab_ssa_label_out.text():
            self.tab_ssa_unpack_all.setEnabled(True)
        else:
            self.tab_ssa_unpack_all.setDisabled(True)

        if self.tab_ssa_list.count() > 0:
            self.tab_ssa_list_export.setEnabled(True)
            self.tab_ssa_unpack_one.setEnabled(True)
            self.subtab_ssa_save.setEnabled(True)
        else:
            self.tab_ssa_list_export.setDisabled(True)
            self.tab_ssa_unpack_one.setDisabled(True)
            self.subtab_ssa_save.setDisabled(True)

    def SSAinSelector(self, event):
        # event is not False, when called from CDropWidget
        if not event:
            dlg = QFileDialog.getOpenFileName(
                self,
                caption="Select SSA file",
                filter="SSA Archive (*.ssa)")
        else:
            dlg = event

        print(dlg)
        filepath = dlg[0]

        if not filepath:
            return

        # parse SSA file create instance
        try:
            self.tab_ssa_SSA = SSA.parseFile(filepath)

            if self.tab_ssa_kyrillicencode.isChecked():
                self.tab_ssa_SSA.encoding = c.RUS_ENCODING

        except FileNotFoundError:
            Util.showErrorMSG("File not found!")
            return
        except Exception as e:
            Util.showExceptionMSG(e)
            return

        self.tab_ssa_label_in.setText(filepath)

        # SSA file index to ListWidget
        self.tab_ssa_list.clear()
        self.tab_ssa_list.addItems(self.tab_ssa_SSA.getFileList())

        # fill SSA metadata
        self.subtab_ssa_keylist.clear()
        self.subtab_ssa_value.clear()
        self.subtab_ssa_label.setText(self.tab_ssa_SSA.archiveName)
        for (key, _) in self.tab_ssa_SSA.getMetadata():
            self.subtab_ssa_keylist.addItem(key)

        if self.subtab_ssa_keylist.count() > 0:
            self.subtab_ssa_keylist.setCurrentRow(0)

        self.SSAcheckButton()

    def SSAoutSelector(self):
        dlg = QFileDialog.getExistingDirectory(self, caption="Select output folder")

        self.tab_ssa_label_out.setText(dlg)
        print(dlg)

        self.SSAcheckButton()

    def SSAconvertAll(self):
        class Extractor(QThread):
            from PyQt5.QtCore import pyqtSignal
            onFinished = pyqtSignal()
            onError = pyqtSignal(Exception)

            def __init__(self, ssa: SSA, outputFolder: str, decompress: str, progress: ProgressWindow):
                QThread.__init__(self)

                self.ssa = ssa
                self.outputFolder = outputFolder
                self.decompress = decompress
                self.progressbar = progress

            def run(self):
                self.progressbar.onShow.emit()
                try:
                    self.ssa.extract(
                        self.outputFolder,
                        self.decompress,
                        progressCallback=self._updateProgress,
                        finishCallback=self._finished
                    )
                except Exception as e:
                    self.onError.emit(e)
                finally:
                    self.progressbar.onClose.emit()

            def _updateProgress(self, curr: int, total: int, filename: str):
                self.progressbar.onNewProgress.emit(curr, total, filename)

            def _finished(self):
                self.onFinished.emit()

        progressbar = ProgressWindow()
        self.extractor = Extractor(
            self.tab_ssa_SSA,
            self.tab_ssa_label_out.text(),
            self.tab_ssa_decompress.isChecked(),
            progressbar
        )
        self.extractor.onError.connect(Util.showExceptionMSG)
        self.extractor.onFinished.connect(lambda: Util.showInfoMSG("Done!"))
        self.extractor.start()

    def SSAconvertOne(self):
        try:
            itemIndex = self.tab_ssa_list.selectedIndexes()[0].row()
        except IndexError:
            Util.showInfoMSG("Please select a file to export", "NOTE")
            return

        if not (outputFolder := self.tab_ssa_label_out.text()):
            outputFolder = QFileDialog.getExistingDirectory(self, caption="Select output folder")
        print(outputFolder)

        if not outputFolder:
            return

        if not self.tab_ssa_SSA:
            Util.showErrorMSG("Failed to read filelist :(")
            return

        try:
            self.tab_ssa_SSA.extractSingle(outputFolder, itemIndex, self.tab_ssa_decompress.isChecked())
        except Exception as e:
            Util.showExceptionMSG(e)

    def SSAexportList(self):
        if self.tab_ssa_SSA:
            dlg = QFileDialog.getSaveFileName(
                self,
                caption="Save file",
                filter="CSV files (*.csv)"
            )
            if not (filename := dlg[0]):
                return

            try:
                with open(filename, "w") as csvfile:
                    csvfile.write(";".join(["filename", "start offset", "end offset", "size in B"]) + "\n")

                    for file in self.tab_ssa_SSA.file_index:
                        csvfile.write(";".join([
                            file.getPath(self.tab_ssa_SSA.encoding),
                            str(file.start_offset),
                            str(file.end_offset),
                            str(file.size)
                        ]) + "\n")

            except Exception as e:
                Util.showExceptionMSG(e)
                return
        else:
            Util.showErrorMSG("Could not read filelist, are there any elements?")

    def SSAmetadataUpdate(self):
        try:
            itemIndex = self.subtab_ssa_keylist.selectedIndexes()[0].row()
        except IndexError:
            return

        value = self.tab_ssa_SSA.getMetadata()[itemIndex][1]
        self.subtab_ssa_value.setPlainText(value)

    ### DCL
    def DCLinSelector(self):
        dlg = QFileDialog.getOpenFileName(self, caption="Select compressed file")
        if not (file := dlg[0]):
            return

        self.tab_dcl_label_in.setText(file)
        self.DCLcheckButtons()

    def DCLoutSelector(self):
        dlg = QFileDialog.getSaveFileName(self, caption="Save decompressed file")
        if not (file := dlg[0]):
            return

        self.tab_dcl_label_out.setText(file)
        self.DCLcheckButtons()

    def DCLdecompress(self):
        try:
            dcl = DCL.parseFile(self.tab_dcl_label_in.text())
            dcl.decompressToFile(self.tab_dcl_label_out.text())

            Util.showInfoMSG("Done")
        except AssertionError:
            Util.showErrorMSG("Selected file is not compressed or not supported!")
        except Exception as e:
            Util.showExceptionMSG(e)

    def DCLcheckButtons(self):
        if self.tab_dcl_label_in.text() and self.tab_dcl_label_out.text():
            self.tab_dcl_decompress.setEnabled(True)

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
        filelist = [self.tab_sst_label_in.text()]
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
            Util.showErrorMSG(e.args[0])
            return

        if not self.tab_sst_donemessage.isChecked():
            Util.showInfoMSG("Done!")

    def _SSTdropConvert(self, filelist: list, ext: str):
        output = self.SSTcheckOutput()
        bundling = not self.tab_sst_bundling.isChecked()

        if ext == ".sst":
            selection = "1"
        else:
            selection = "2"

            if bundling and len(filelist) > 1:
                _msg = "Following files will get bundeled into one SST\n"
                _msg += "please confirm this order:\n\n"

                for i, file in enumerate(filelist):
                    _msg += f"[{i + 1}] => {os.path.basename(file)}\n"

                if not Util.showQuestionMSG(_msg):
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
            Util.showErrorMSG(e.args[0])
            return

        if not self.tab_sst_donemessage.isChecked():
            Util.showInfoMSG("Done!")

    def SSTdropHandler(self, event):
        print(event)

        # check if view only is set
        if self.tab_sst_viewonly.isChecked():
            try:
                self.showImageViewer(event[0])  # open only the first dropped file
            except Exception as e:
                Util.showErrorMSG(e.args[0])
            finally:
                return

        # check if output is set
        if not self.tab_sst_input_checkbox.isChecked():
            if not self.tab_sst_label_out.text():
                Util.showErrorMSG("No output destination specified!")
                return

        # check if all files have the same ext otherwise show error
        ext = os.path.splitext(event[0])[1]

        if any(os.path.splitext(f)[1] != ext for f in event):
            Util.showErrorMSG("All files have to have the same file type!")
            return
        elif ext not in [".sst", ".tga"]:
            Util.showErrorMSG("only TGA and SST files are supported")
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

        # print(maxX, maxY)

        # update aspect ratio of the GridView, target is 4:3 # does not work for some reason :(
        # if maxX >= maxY:
        #    self.tab_slc_gridview.setMaximumSize(5000, round( (maxX / 4) * 3 ))
        # else:
        #    self.tab_slc_gridview.setMaximumSize(round( (maxY / 3) * 4 ))

        scene = QGraphicsScene(self)
        self.tab_slc_gridview.setScene(scene)

        rows = int(self.tab_slc_row_count.text())
        colums = int(self.tab_slc_col_count.text())

        boxH = maxY // rows
        boxB = maxX // colums

        # scene.addRect(100, -50, maxX, maxY)
        # scene.addLine(0, 0, 0, maxY)
        # scene.addLine(0, 0, 50, 50)
        # scene.addLine(50, 0, 0, 50)
        # scene.addLine(0, 0, 50, 50)

        for r in range(rows):
            scene.addLine(0, r * boxH, maxX, r * boxH)

        for c in range(colums):
            scene.addLine(c * boxB, 0, c * boxB, maxY)

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
            # self.tab_slc_label_in.setText('; '.join( [ os.path.basename(p) for p in files ] ) )
            # or maybe this is better
            pass

        # add files to the file list wiget
        self.tab_slc_list.clear()
        self.tab_slc_list.addItems(files)

        self.tab_slc_label_in.setText(f"{len(files)} file(s) imported")

        # move vertical scroll bar all the way to the right
        # self.tab_slc_list.horizontalScrollBar().maximum()
        # self.tab_slc_list.verticalScrollBar().maximum()
        # self.tab_slc_list.horizontalScrollBar().setValue(self.tab_slc_list.horizontalScrollBar())

    def SLCinSelector(self):
        dlg = QFileDialog.getOpenFileNames(
            self,
            caption="Select TGA / SST file(s)",
            filter="SST Image (*.sst);;TGA Image (*.tga)"
        )

        # print(dlg)
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
        inputfiles = [self.tab_slc_list.item(i).text() for i in range(self.tab_slc_list.count())]

        _msg = "Following files will be joined:\n"
        _msg += "Please confirm this order.\n\n"

        for i, file in enumerate(inputfiles):
            _msg += f"[{i + 1}] => {os.path.basename(file)}\n"

        if not Util.showQuestionMSG(msg_str=_msg, title_msg="Please confirm"):
            return
        else:
            self.SLCslicer()

    def SLCslicer(self):
        inputfiles = [self.tab_slc_list.item(i).text() for i in range(self.tab_slc_list.count())]

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
                yTiles=int(self.tab_slc_row_count.text()),
                reversed=self.tab_slc_switchCoords.isChecked()
            )
        except Exception as e:
            Util.showErrorMSG(e.args[0])
            return

        Util.showInfoMSG("Done!")

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

    ### other ui stuff
    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(
            self.app.primaryScreen().availableGeometry().center())
        self.move(qr.topLeft())

    ### TEST
    def test(self, event=None):
        print("nice")
        print(event)


def main():
    app = QApplication(sys.argv)

    mainWindow = MainWindow(app)
    mainWindow.center()
    mainWindow.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    # this is only needed for the CI / CD
    if "-v" in sys.argv:
        print(c.VERSION)
        sys.exit()

    main()
