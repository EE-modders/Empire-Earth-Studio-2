
from PIL import Image, ImageQt
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
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

        #self.setStyleSheet("background-color: rgb(255, 255, 255);border: 4px dashed rgb(97, 97, 97);border-radius: 10;")

    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent) -> None:
        if a0.mimeData().hasUrls():
            #print(a0.mimeData().formats())
            a0.accept()
            #self.setStyleSheet("background-color: rgb(255, 255, 255);border: 4px dashed rgb(97, 255, 97);border-radius: 10;")
        else:
            pass
            #self.setStyleSheet("background-color: rgb(255, 255, 255);border: 4px dashed rgb(255, 97, 97);border-radius: 10;")
        
    def dragMoveEvent(self, a0: QtGui.QDragMoveEvent) -> None:
        a0.accept()

    def dragLeaveEvent(self, a0: QtGui.QDragLeaveEvent) -> None:
        a0.accept()
        #self.setStyleSheet("background-color: rgb(255, 255, 255);border: 4px dashed rgb(97, 97, 97);border-radius: 10;")

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


class CImageLabel(QtWidgets.QLabel):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.LabelImage = list()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        #super().resizeEvent(a0)

        x, y = self.width(), self.height()

        if x < y:
            for LImage in self.LabelImage:
                self.setPixmap( LImage.scaled(x, x, QtCore.Qt.KeepAspectRatio) )
        else:
            for LImage in self.LabelImage:
                self.setPixmap( LImage.scaled(y, y, QtCore.Qt.KeepAspectRatio) )

    def setImage(self, image: Image):
        LabelImage = QtGui.QPixmap.fromImage( ImageQt.ImageQt(image) )
        self.LabelImage.append(LabelImage)
        self.setPixmap(LabelImage)
        self.resizeEvent(None)
