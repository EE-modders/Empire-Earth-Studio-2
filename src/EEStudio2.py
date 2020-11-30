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
from PyQt5.QtWidgets import QApplication, QErrorMessage, QFileDialog, QMainWindow, QMessageBox

#import qdarkstyle

from lib import Ui_mainWindow

from lib.SSAtool.src import SSAtool

class MainWindow(QMainWindow, Ui_mainWindow.Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setupUi(self)
        self.initButtons()


    def initButtons(self):
        self.tab_ssa_select_in.clicked.connect(self.SSAinSelector)
        self.tab_ssa_select_out.clicked.connect(self.SSAoutSelector)
        self.tab_ssa_unpack.clicked.connect(self.SSAconvert)

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

    ### SSA
    def SSAinSelector(self):
        dlg = QFileDialog.getOpenFileName(
            self,
            caption="Select SSA file",
            filter="SSA Archives (*.ssa)",
        )

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

    def SSAcheckButton(self):
        if self.tab_ssa_label_in.text() and self.tab_ssa_label_out.text():
            self.tab_ssa_unpack.setEnabled(True)
        else:
            self.tab_ssa_unpack.setEnabled(False)

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
    ### SST Slicer
    ### CEM

    ### TEST
    def clickedTestButton(self):
        pass
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
