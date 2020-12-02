
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal

class CDropWidget(QtWidgets.QListWidget):
    onDrop = pyqtSignal(list)

    def __init__(self, parent):
        super().__init__(parent)

    def dragEnterEvent(self, e: QtGui.QDragEnterEvent):
        if e.mimeData().hasUrls():
            #print(e.mimeData().formats())
            e.accept()

    def dragMoveEvent(self, e: QtGui.QDragMoveEvent):
        e.accept()

    def dropEvent(self, e: QtGui.QDropEvent):
        # only take the first file
        file = [ e.mimeData().urls()[0].toLocalFile() ]
        #files = [u.toLocalFile() for u in e.mimeData().urls()]
        self.onDrop.emit(file)

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


class CGraphicsView(QtWidgets.QGraphicsView):
    onResize = pyqtSignal()

    def __init__(self, parent) -> None:
        super().__init__(parent)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        #print("resize event")
        self.onResize.emit()
