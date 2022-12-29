#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 30.08.2022 22:42 CET

@author: zocker_160
"""

import os
import traceback
import webbrowser
from pathlib import Path

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMessageBox

from io import BufferedReader, BufferedWriter

from lib import constants as c

def setPlaceholders(text: str) -> str:
    text = text.replace(c.PLACEHOLDER_VERSION, c.VERSION)
    text = text.replace(c.PLACEHOLDER_YEAR, c.YEAR)
    return text


def showHelp():
    webbrowser.open("https://github.com/EE-modders/Empire-Earth-Studio-2")

def showReportIssue():
    webbrowser.open("https://github.com/EE-modders/Empire-Earth-Studio-2/issues")


def showErrorMSG(message, title="ERROR", detail=""):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(str(message))
    if detail:
        msg.setDetailedText(detail)
    msg.setWindowTitle(title)
    msg.setDefaultButton(QMessageBox.Close)
    msg.exec()

def showExceptionMSG(e: Exception, title="ERROR"):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(f"An error ({type(e).__name__}) occured!")

    tbStr = traceback.format_exception(type(e), e, e.__traceback__)
    msg.setDetailedText(''.join(tbStr))

    msg.setWindowTitle(title)
    msg.setDefaultButton(QMessageBox.Close)
    msg.exec()

def showInfoMSG(msg_str: str, title_msg="INFO"):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(msg_str)
    msg.setWindowTitle(title_msg)
    msg.setDefaultButton(QMessageBox.Close)
    msg.exec()

def showQuestionMSG(msg_str: str, title_msg="QUESTION") -> bool:
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)
    msg.setText(msg_str)
    msg.setWindowTitle(title_msg)
    msg.addButton(QMessageBox.Yes)
    msg.addButton(QMessageBox.No)
    msg.setDefaultButton(QMessageBox.Yes)

    reply = msg.exec()

    return reply == QMessageBox.Yes


def readInt(f: BufferedReader) -> int:
    return int.from_bytes(f.read(4), byteorder="little", signed=False)

def writeInt(f: BufferedWriter, value: int) -> int:
    return f.write(value.to_bytes(4, byteorder="little", signed=False))

def checkNullTerminator(data: bytes) -> bytes:
    if not data.endswith(b"\0"):
        data += b"\0"
    return data
