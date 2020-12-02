
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal

class CDropWidget(QtWidgets.QListWidget):
    def __init__(self, parent):
        super().__init__(parent)

    def dragEnterEvent(self, e: QtGui.QDragEnterEvent):
        if e.mimeData().hasUrls():
            print(e.mimeData().formats())

        e.accept()

    def dragMoveEvent(self, e: QtGui.QDragMoveEvent):
        e.accept()

    def dropEvent(self, e: QtGui.QDropEvent):
        files = [u.toLocalFile() for u in e.mimeData().urls()]

        for f in files:
            print(f)
            self.addItem(f)

class CDropLabel(QtWidgets.QLabel):
    onDrop = pyqtSignal(list)

    def __init__(self, parent) -> None:
        super().__init__(parent)

    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent) -> None:
        if a0.mimeData().hasUrls():
            #print(a0.mimeData().formats())
            a0.accept()

    def dragMoveEvent(self, a0: QtGui.QDragMoveEvent) -> None:
        a0.accept()

    def dropEvent(self, a0: QtGui.QDropEvent) -> None:
        files = [u.toLocalFile() for u in a0.mimeData().urls()]

        #print("dropped")
        self.onDrop.emit(files)
