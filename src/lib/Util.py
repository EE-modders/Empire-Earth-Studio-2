#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 30.08.2022 22:42 CET

@author: zocker_160
"""

import webbrowser

from PyQt5.QtWidgets import QMessageBox


def showHelp():
    webbrowser.open("https://github.com/EE-modders/Empire-Earth-Studio-2")


def showReportIssue():
    webbrowser.open("https://github.com/EE-modders/Empire-Earth-Studio-2/issues")


def showErrorMSG(msg_str, title_msg="ERROR"):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(str(msg_str))
    msg.setWindowTitle(title_msg)
    msg.setDefaultButton(QMessageBox.Close)
    msg.exec()


def showInfoMSG(msg_str: str, title_msg="INFO"):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(msg_str)
    msg.setWindowTitle(title_msg)
    msg.setDefaultButton(QMessageBox.Close)
    msg.exec()


def showQuestionMSG(msg_str: str, title_msg="QUESTION"):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)
    msg.setText(msg_str)
    msg.setWindowTitle(title_msg)
    msg.addButton(QMessageBox.Yes)
    msg.addButton(QMessageBox.No)
    msg.setDefaultButton(QMessageBox.Yes)

    reply = msg.exec()

    if reply == QMessageBox.Yes:
        return True
    else:
        return False
