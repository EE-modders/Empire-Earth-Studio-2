
from PyQt5 import QtWidgets
from PyQt5 import QtGui

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
    def __init__(self, parent) -> None:
        super().__init__(parent)

    