#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#! /usr/bin/env python3

"""
Created on 10.11.2020 22:17 CET

@author: zocker_160
"""

import os
import sys
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QApplication, QErrorMessage, QFileDialog, QGraphicsScene, QMainWindow, QMessageBox

#import qdarkstyle

from lib import Ui_mainWindow

from lib.SSAtool.src import SSAtool
from lib.SSTtool.src import SSTtool

class MainWindow(QMainWindow, Ui_mainWindow.Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.gridMax = 10
        self.gridMin = 2

        self.setupUi(self)
        self.initGUIControlls()
        self.SLCupdateGridview()

    def initGUIControlls(self):
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

        #self.testbutton.clicked.connect(self.clickedTestButton)


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
                filter="SSA Archives (*.ssa)",
            )
        else:
            dlg = event

        print(dlg)

        filepath = dlg[0]

        # add file list to listWidget
        try:
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
        SSAtool.main(
            inputfile=self.tab_ssa_label_in.text(),
            outputfolder=self.tab_ssa_label_out.text(),
            decompress=self.tab_ssa_decompress.isChecked(),
            log=False
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

        # check of output is set
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

        # update aspect ratio of the GridView, target is 4:3 # does not work, but this does fix some other shit for some reason, so do not remove!
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



    ### CEM

    ### TEST
    def test(self, event=None):
        print("nice")
        print(event)
        #self.testlabel.setText("Leck mir die Eier!!!")



def main():
    app = QApplication(sys.argv)
    #app.setStyleSheet(qdarkstyle.load_stylesheet())

    Window = MainWindow()
    Window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    # this is only needed for the CI / CD
    try:
        testmode = sys.argv[1] == "-v"
    except:
        testmode = False

    if testmode:
        print("THIS SHOULD WORK!")
        sys.exit()
    else:
        main()
