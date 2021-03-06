# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/bene/Windows_Daten/Programmierung_Modding/Empire Earth/GitHub/Empire-Earth-Studio-2/src/lib/mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(793, 633)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/assets/icon128.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.MainTabs = QtWidgets.QTabWidget(self.centralwidget)
        self.MainTabs.setSizeIncrement(QtCore.QSize(0, 0))
        self.MainTabs.setTabPosition(QtWidgets.QTabWidget.North)
        self.MainTabs.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.MainTabs.setElideMode(QtCore.Qt.ElideNone)
        self.MainTabs.setUsesScrollButtons(True)
        self.MainTabs.setTabsClosable(False)
        self.MainTabs.setMovable(True)
        self.MainTabs.setObjectName("MainTabs")
        self.tab_main = QtWidgets.QWidget()
        self.tab_main.setObjectName("tab_main")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_main)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.main_description = QtWidgets.QLabel(self.tab_main)
        self.main_description.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.main_description.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.main_description.setObjectName("main_description")
        self.verticalLayout_3.addWidget(self.main_description)
        self.MainTabs.addTab(self.tab_main, "")
        self.tab_ssa = QtWidgets.QWidget()
        self.tab_ssa.setObjectName("tab_ssa")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_ssa)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tab_ssa_label = QtWidgets.QLabel(self.tab_ssa)
        self.tab_ssa_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_ssa_label.setObjectName("tab_ssa_label")
        self.verticalLayout.addWidget(self.tab_ssa_label)
        self.tab_ssa_list = CDropWidget(self.tab_ssa)
        self.tab_ssa_list.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tab_ssa_list.setAcceptDrops(True)
        self.tab_ssa_list.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.tab_ssa_list.setAlternatingRowColors(True)
        self.tab_ssa_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tab_ssa_list.setObjectName("tab_ssa_list")
        self.verticalLayout.addWidget(self.tab_ssa_list)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setContentsMargins(6, -1, -1, -1)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.tab_ssa_label_clear = QtWidgets.QPushButton(self.tab_ssa)
        self.tab_ssa_label_clear.setMaximumSize(QtCore.QSize(75, 20))
        self.tab_ssa_label_clear.setStyleSheet("color: rgb(255, 0, 0);")
        self.tab_ssa_label_clear.setObjectName("tab_ssa_label_clear")
        self.horizontalLayout_9.addWidget(self.tab_ssa_label_clear)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem)
        self.tab_ssa_list_export = QtWidgets.QPushButton(self.tab_ssa)
        self.tab_ssa_list_export.setEnabled(False)
        self.tab_ssa_list_export.setMaximumSize(QtCore.QSize(16777215, 20))
        self.tab_ssa_list_export.setObjectName("tab_ssa_list_export")
        self.horizontalLayout_9.addWidget(self.tab_ssa_list_export)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.widget = QtWidgets.QWidget(self.tab_ssa)
        self.widget.setMinimumSize(QtCore.QSize(0, 43))
        self.widget.setObjectName("widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tab_ssa_label_in = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_ssa_label_in.sizePolicy().hasHeightForWidth())
        self.tab_ssa_label_in.setSizePolicy(sizePolicy)
        self.tab_ssa_label_in.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tab_ssa_label_in.setText("")
        self.tab_ssa_label_in.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tab_ssa_label_in.setWordWrap(True)
        self.tab_ssa_label_in.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.tab_ssa_label_in.setObjectName("tab_ssa_label_in")
        self.gridLayout_2.addWidget(self.tab_ssa_label_in, 0, 1, 1, 1)
        self.tab_ssa_select_in = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_ssa_select_in.sizePolicy().hasHeightForWidth())
        self.tab_ssa_select_in.setSizePolicy(sizePolicy)
        self.tab_ssa_select_in.setMinimumSize(QtCore.QSize(0, 0))
        self.tab_ssa_select_in.setMaximumSize(QtCore.QSize(150, 30))
        self.tab_ssa_select_in.setObjectName("tab_ssa_select_in")
        self.gridLayout_2.addWidget(self.tab_ssa_select_in, 0, 0, 1, 1)
        self.tab_ssa_select_out = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_ssa_select_out.sizePolicy().hasHeightForWidth())
        self.tab_ssa_select_out.setSizePolicy(sizePolicy)
        self.tab_ssa_select_out.setMinimumSize(QtCore.QSize(0, 0))
        self.tab_ssa_select_out.setMaximumSize(QtCore.QSize(150, 30))
        self.tab_ssa_select_out.setObjectName("tab_ssa_select_out")
        self.gridLayout_2.addWidget(self.tab_ssa_select_out, 1, 0, 1, 1)
        self.tab_ssa_label_out = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_ssa_label_out.sizePolicy().hasHeightForWidth())
        self.tab_ssa_label_out.setSizePolicy(sizePolicy)
        self.tab_ssa_label_out.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tab_ssa_label_out.setText("")
        self.tab_ssa_label_out.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tab_ssa_label_out.setWordWrap(True)
        self.tab_ssa_label_out.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.tab_ssa_label_out.setObjectName("tab_ssa_label_out")
        self.gridLayout_2.addWidget(self.tab_ssa_label_out, 1, 1, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tab_ssa_decompress = QtWidgets.QCheckBox(self.widget)
        self.tab_ssa_decompress.setChecked(True)
        self.tab_ssa_decompress.setTristate(False)
        self.tab_ssa_decompress.setObjectName("tab_ssa_decompress")
        self.horizontalLayout.addWidget(self.tab_ssa_decompress)
        self.tab_ssa_kyrillicencode = QtWidgets.QCheckBox(self.widget)
        self.tab_ssa_kyrillicencode.setObjectName("tab_ssa_kyrillicencode")
        self.horizontalLayout.addWidget(self.tab_ssa_kyrillicencode)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.tab_ssa_unpack = QtWidgets.QPushButton(self.widget)
        self.tab_ssa_unpack.setEnabled(False)
        self.tab_ssa_unpack.setCheckable(False)
        self.tab_ssa_unpack.setChecked(False)
        self.tab_ssa_unpack.setDefault(False)
        self.tab_ssa_unpack.setFlat(False)
        self.tab_ssa_unpack.setObjectName("tab_ssa_unpack")
        self.verticalLayout_4.addWidget(self.tab_ssa_unpack)
        self.verticalLayout.addWidget(self.widget)
        self.MainTabs.addTab(self.tab_ssa, "")
        self.tab_sst = QtWidgets.QWidget()
        self.tab_sst.setAcceptDrops(True)
        self.tab_sst.setObjectName("tab_sst")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_sst)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.tab_sst_droplabel = CDropLabel(self.tab_sst)
        self.tab_sst_droplabel.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_sst_droplabel.sizePolicy().hasHeightForWidth())
        self.tab_sst_droplabel.setSizePolicy(sizePolicy)
        self.tab_sst_droplabel.setAcceptDrops(True)
        self.tab_sst_droplabel.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 4px dashed rgb(97, 97, 97);\n"
"border-radius: 10;\n"
"")
        self.tab_sst_droplabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tab_sst_droplabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_sst_droplabel.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.tab_sst_droplabel.setObjectName("tab_sst_droplabel")
        self.verticalLayout_5.addWidget(self.tab_sst_droplabel)
        self.label_5 = QtWidgets.QLabel(self.tab_sst)
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 24))
        self.label_5.setObjectName("label_5")
        self.verticalLayout_5.addWidget(self.label_5)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tab_sst_viewonly = QtWidgets.QCheckBox(self.tab_sst)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tab_sst_viewonly.setFont(font)
        self.tab_sst_viewonly.setChecked(False)
        self.tab_sst_viewonly.setTristate(False)
        self.tab_sst_viewonly.setObjectName("tab_sst_viewonly")
        self.gridLayout_4.addWidget(self.tab_sst_viewonly, 0, 0, 1, 1)
        self.tab_sst_firstonly = QtWidgets.QCheckBox(self.tab_sst)
        self.tab_sst_firstonly.setObjectName("tab_sst_firstonly")
        self.gridLayout_4.addWidget(self.tab_sst_firstonly, 1, 1, 1, 1)
        self.tab_sst_donemessage = QtWidgets.QCheckBox(self.tab_sst)
        self.tab_sst_donemessage.setObjectName("tab_sst_donemessage")
        self.gridLayout_4.addWidget(self.tab_sst_donemessage, 1, 2, 1, 1)
        self.tab_sst_overwrite = QtWidgets.QCheckBox(self.tab_sst)
        self.tab_sst_overwrite.setObjectName("tab_sst_overwrite")
        self.gridLayout_4.addWidget(self.tab_sst_overwrite, 0, 2, 1, 1)
        self.tab_sst_bundling = QtWidgets.QCheckBox(self.tab_sst)
        self.tab_sst_bundling.setObjectName("tab_sst_bundling")
        self.gridLayout_4.addWidget(self.tab_sst_bundling, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tab_sst)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 1, 0, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout_4)
        self.line_3 = QtWidgets.QFrame(self.tab_sst)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_5.addWidget(self.line_3)
        self.line_4 = QtWidgets.QFrame(self.tab_sst)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_5.addWidget(self.line_4)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tab_sst_radio_1 = QtWidgets.QRadioButton(self.tab_sst)
        self.tab_sst_radio_1.setChecked(True)
        self.tab_sst_radio_1.setObjectName("tab_sst_radio_1")
        self.horizontalLayout_4.addWidget(self.tab_sst_radio_1)
        self.tab_sst_radio_2 = QtWidgets.QRadioButton(self.tab_sst)
        self.tab_sst_radio_2.setChecked(False)
        self.tab_sst_radio_2.setObjectName("tab_sst_radio_2")
        self.horizontalLayout_4.addWidget(self.tab_sst_radio_2)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.tab_sst_select_in = QtWidgets.QPushButton(self.tab_sst)
        self.tab_sst_select_in.setMaximumSize(QtCore.QSize(220, 30))
        self.tab_sst_select_in.setObjectName("tab_sst_select_in")
        self.gridLayout.addWidget(self.tab_sst_select_in, 1, 0, 1, 1)
        self.tab_sst_label_in = QtWidgets.QLabel(self.tab_sst)
        self.tab_sst_label_in.setText("")
        self.tab_sst_label_in.setWordWrap(True)
        self.tab_sst_label_in.setObjectName("tab_sst_label_in")
        self.gridLayout.addWidget(self.tab_sst_label_in, 1, 1, 1, 1)
        self.tab_sst_label_out = QtWidgets.QLabel(self.tab_sst)
        self.tab_sst_label_out.setText("")
        self.tab_sst_label_out.setWordWrap(True)
        self.tab_sst_label_out.setObjectName("tab_sst_label_out")
        self.gridLayout.addWidget(self.tab_sst_label_out, 4, 1, 1, 1)
        self.tab_sst_select_out = QtWidgets.QPushButton(self.tab_sst)
        self.tab_sst_select_out.setEnabled(False)
        self.tab_sst_select_out.setMaximumSize(QtCore.QSize(220, 30))
        self.tab_sst_select_out.setObjectName("tab_sst_select_out")
        self.gridLayout.addWidget(self.tab_sst_select_out, 4, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.tab_sst)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 2, 1, 1, 1)
        self.tab_sst_input_checkbox = QtWidgets.QCheckBox(self.tab_sst)
        self.tab_sst_input_checkbox.setChecked(True)
        self.tab_sst_input_checkbox.setObjectName("tab_sst_input_checkbox")
        self.gridLayout.addWidget(self.tab_sst_input_checkbox, 3, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.tab_sst)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 0, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout)
        self.tab_sst_convert = QtWidgets.QPushButton(self.tab_sst)
        self.tab_sst_convert.setEnabled(False)
        self.tab_sst_convert.setObjectName("tab_sst_convert")
        self.verticalLayout_5.addWidget(self.tab_sst_convert)
        self.MainTabs.addTab(self.tab_sst, "")
        self.tab_slicer = QtWidgets.QWidget()
        self.tab_slicer.setObjectName("tab_slicer")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_slicer)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label = QtWidgets.QLabel(self.tab_slicer)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_8.addWidget(self.label)
        self.tab_slc_list = CDropWidget(self.tab_slicer)
        self.tab_slc_list.setObjectName("tab_slc_list")
        self.verticalLayout_8.addWidget(self.tab_slc_list)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.clear = QtWidgets.QPushButton(self.tab_slicer)
        self.clear.setMaximumSize(QtCore.QSize(75, 25))
        self.clear.setStyleSheet("color: rgb(255, 0, 0);\n"
"")
        self.clear.setObjectName("clear")
        self.horizontalLayout_7.addWidget(self.clear)
        self.tab_slc_moveup = QtWidgets.QPushButton(self.tab_slicer)
        self.tab_slc_moveup.setMaximumSize(QtCore.QSize(30, 25))
        self.tab_slc_moveup.setObjectName("tab_slc_moveup")
        self.horizontalLayout_7.addWidget(self.tab_slc_moveup)
        self.tab_slc_movedown = QtWidgets.QPushButton(self.tab_slicer)
        self.tab_slc_movedown.setMaximumSize(QtCore.QSize(45, 25))
        self.tab_slc_movedown.setObjectName("tab_slc_movedown")
        self.horizontalLayout_7.addWidget(self.tab_slc_movedown)
        self.verticalLayout_8.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6.addLayout(self.verticalLayout_8)
        self.line_5 = QtWidgets.QFrame(self.tab_slicer)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.horizontalLayout_6.addWidget(self.line_5)
        self.widget_2 = QtWidgets.QWidget(self.tab_slicer)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tab_slc_gridview = CGraphicsView(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_slc_gridview.sizePolicy().hasHeightForWidth())
        self.tab_slc_gridview.setSizePolicy(sizePolicy)
        self.tab_slc_gridview.setMinimumSize(QtCore.QSize(400, 0))
        self.tab_slc_gridview.setMaximumSize(QtCore.QSize(16777215, 300))
        self.tab_slc_gridview.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tab_slc_gridview.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tab_slc_gridview.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.HighQualityAntialiasing|QtGui.QPainter.TextAntialiasing)
        self.tab_slc_gridview.setResizeAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        self.tab_slc_gridview.setObjectName("tab_slc_gridview")
        self.horizontalLayout_3.addWidget(self.tab_slc_gridview)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem1)
        self.tab_slc_row_plus = QtWidgets.QPushButton(self.widget_2)
        self.tab_slc_row_plus.setMinimumSize(QtCore.QSize(30, 30))
        self.tab_slc_row_plus.setMaximumSize(QtCore.QSize(30, 30))
        self.tab_slc_row_plus.setObjectName("tab_slc_row_plus")
        self.verticalLayout_7.addWidget(self.tab_slc_row_plus)
        self.tab_slc_row_count = QtWidgets.QLabel(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_slc_row_count.sizePolicy().hasHeightForWidth())
        self.tab_slc_row_count.setSizePolicy(sizePolicy)
        self.tab_slc_row_count.setMinimumSize(QtCore.QSize(0, 30))
        self.tab_slc_row_count.setTextFormat(QtCore.Qt.PlainText)
        self.tab_slc_row_count.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_slc_row_count.setObjectName("tab_slc_row_count")
        self.verticalLayout_7.addWidget(self.tab_slc_row_count)
        self.tab_slc_row_minus = QtWidgets.QPushButton(self.widget_2)
        self.tab_slc_row_minus.setMinimumSize(QtCore.QSize(30, 30))
        self.tab_slc_row_minus.setMaximumSize(QtCore.QSize(30, 30))
        self.tab_slc_row_minus.setObjectName("tab_slc_row_minus")
        self.verticalLayout_7.addWidget(self.tab_slc_row_minus)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_7)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout_9.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.tab_slc_col_minus = QtWidgets.QPushButton(self.widget_2)
        self.tab_slc_col_minus.setMinimumSize(QtCore.QSize(30, 30))
        self.tab_slc_col_minus.setMaximumSize(QtCore.QSize(30, 30))
        self.tab_slc_col_minus.setObjectName("tab_slc_col_minus")
        self.horizontalLayout_5.addWidget(self.tab_slc_col_minus)
        self.tab_slc_col_count = QtWidgets.QLabel(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_slc_col_count.sizePolicy().hasHeightForWidth())
        self.tab_slc_col_count.setSizePolicy(sizePolicy)
        self.tab_slc_col_count.setMinimumSize(QtCore.QSize(30, 0))
        self.tab_slc_col_count.setTextFormat(QtCore.Qt.PlainText)
        self.tab_slc_col_count.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_slc_col_count.setObjectName("tab_slc_col_count")
        self.horizontalLayout_5.addWidget(self.tab_slc_col_count)
        self.tab_slc_col_plus = QtWidgets.QPushButton(self.widget_2)
        self.tab_slc_col_plus.setMinimumSize(QtCore.QSize(30, 30))
        self.tab_slc_col_plus.setMaximumSize(QtCore.QSize(30, 30))
        self.tab_slc_col_plus.setObjectName("tab_slc_col_plus")
        self.horizontalLayout_5.addWidget(self.tab_slc_col_plus)
        spacerItem5 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem6)
        self.verticalLayout_9.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6.addWidget(self.widget_2)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tab_slc_select_out = QtWidgets.QPushButton(self.tab_slicer)
        self.tab_slc_select_out.setMaximumSize(QtCore.QSize(150, 30))
        self.tab_slc_select_out.setObjectName("tab_slc_select_out")
        self.gridLayout_3.addWidget(self.tab_slc_select_out, 3, 0, 1, 1)
        self.tab_slc_label_in = CDropLabel(self.tab_slicer)
        self.tab_slc_label_in.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 2px dashed rgb(200, 200, 200);\n"
"border-radius: 10;\n"
"")
        self.tab_slc_label_in.setText("")
        self.tab_slc_label_in.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_slc_label_in.setWordWrap(True)
        self.tab_slc_label_in.setObjectName("tab_slc_label_in")
        self.gridLayout_3.addWidget(self.tab_slc_label_in, 2, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.tab_slicer)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 0, 0, 1, 1)
        self.tab_slc_label_out = QtWidgets.QLabel(self.tab_slicer)
        self.tab_slc_label_out.setText("")
        self.tab_slc_label_out.setWordWrap(True)
        self.tab_slc_label_out.setObjectName("tab_slc_label_out")
        self.gridLayout_3.addWidget(self.tab_slc_label_out, 3, 1, 1, 1)
        self.tab_slc_select_in = QtWidgets.QPushButton(self.tab_slicer)
        self.tab_slc_select_in.setMaximumSize(QtCore.QSize(150, 30))
        self.tab_slc_select_in.setObjectName("tab_slc_select_in")
        self.gridLayout_3.addWidget(self.tab_slc_select_in, 2, 0, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.tab_slc_switchCoords = QtWidgets.QCheckBox(self.tab_slicer)
        self.tab_slc_switchCoords.setObjectName("tab_slc_switchCoords")
        self.horizontalLayout_8.addWidget(self.tab_slc_switchCoords)
        self.gridLayout_3.addLayout(self.horizontalLayout_8, 0, 1, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tab_slc_slice = QtWidgets.QPushButton(self.tab_slicer)
        self.tab_slc_slice.setEnabled(False)
        self.tab_slc_slice.setMinimumSize(QtCore.QSize(0, 50))
        self.tab_slc_slice.setObjectName("tab_slc_slice")
        self.horizontalLayout_2.addWidget(self.tab_slc_slice)
        self.tab_slc_join = QtWidgets.QPushButton(self.tab_slicer)
        self.tab_slc_join.setEnabled(False)
        self.tab_slc_join.setMinimumSize(QtCore.QSize(0, 50))
        self.tab_slc_join.setObjectName("tab_slc_join")
        self.horizontalLayout_2.addWidget(self.tab_slc_join)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.MainTabs.addTab(self.tab_slicer, "")
        self.verticalLayout_2.addWidget(self.MainTabs)
        self.main_infotext = QtWidgets.QLabel(self.centralwidget)
        self.main_infotext.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.main_infotext.setObjectName("main_infotext")
        self.verticalLayout_2.addWidget(self.main_infotext)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 793, 34))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menubar.sizePolicy().hasHeightForWidth())
        self.menubar.setSizePolicy(sizePolicy)
        self.menubar.setObjectName("menubar")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout_Studio_II = QtWidgets.QAction(MainWindow)
        self.actionAbout_Studio_II.setObjectName("actionAbout_Studio_II")
        self.actionHelp_from_GitHUb = QtWidgets.QAction(MainWindow)
        self.actionHelp_from_GitHUb.setObjectName("actionHelp_from_GitHUb")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionReport_Issue = QtWidgets.QAction(MainWindow)
        self.actionReport_Issue.setObjectName("actionReport_Issue")
        self.actionOpen_Image_Viewer = QtWidgets.QAction(MainWindow)
        self.actionOpen_Image_Viewer.setObjectName("actionOpen_Image_Viewer")
        self.actionabout_QT = QtWidgets.QAction(MainWindow)
        self.actionabout_QT.setObjectName("actionabout_QT")
        self.menuAbout.addAction(self.actionHelp_from_GitHUb)
        self.menuAbout.addAction(self.actionReport_Issue)
        self.menuAbout.addSeparator()
        self.menuAbout.addAction(self.actionabout_QT)
        self.menuAbout.addAction(self.actionAbout_Studio_II)
        self.menuFile.addAction(self.actionOpen_Image_Viewer)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.MainTabs.setCurrentIndex(0)
        self.actionExit.triggered.connect(MainWindow.close)
        self.tab_ssa_label_clear.clicked.connect(self.tab_ssa_label_in.clear)
        self.clear.clicked.connect(self.tab_slc_list.clear)
        self.clear.clicked.connect(self.tab_slc_label_in.clear)
        self.tab_ssa_label_clear.clicked['bool'].connect(self.tab_ssa_unpack.setEnabled)
        self.clear.clicked['bool'].connect(self.tab_slc_join.setEnabled)
        self.tab_sst_input_checkbox.clicked['bool'].connect(self.tab_sst_select_out.setDisabled)
        self.tab_ssa_label_clear.clicked.connect(self.tab_ssa_list.clear)
        self.clear.clicked['bool'].connect(self.tab_slc_slice.setEnabled)
        self.tab_sst_input_checkbox.clicked['bool'].connect(self.tab_sst_label_out.setDisabled)
        self.tab_ssa_label_clear.clicked['bool'].connect(self.tab_ssa_list_export.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Empire Earth Studio II"))
        self.MainTabs.setAccessibleName(_translate("MainWindow", "some random name"))
        self.MainTabs.setAccessibleDescription(_translate("MainWindow", "some random description"))
        self.main_description.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; text-decoration: underline;\">Empire Earth Studio II</span></p><p>Empire Earth Studio II is an unofficial successor and replacement for the old EEStudio.</p><p>Here a quick overview of what you can do:</p><p>- <span style=\" font-weight:600;\">Archives (SSA):</span> extracting ssa game files</p><p>- <span style=\" font-weight:600;\">Textures (SST):</span> view, convert sst texture files</p><p>- <span style=\" font-weight:600;\">Slicer (SST):</span> join/split sst/tga textures (mainly used for backgrounds)</p><p>-------------------------</p><p><span style=\" font-weight:600;\">CREDITS:</span></p><p>programming by zocker_160 and thanks to Philla007 for additional help<br/>-------------------------</p><p><span style=\" font-weight:600;\">LINKS:</span></p><p>- join our Discord server: <a href=\"https://discord.gg/BjUXbFB\"><span style=\" text-decoration: underline; color:#2980b9;\">https://discord.gg/BjUXbFB</span></a></p><p>- our GitHub page: <a href=\"https://github.com/EE-modders\"><span style=\" text-decoration: underline; color:#2980b9;\">https://github.com/EE-modders</span></a></p><p>- report an issue: <a href=\"https://github.com/EE-modders/Empire-Earth-Studio-2/issues\"><span style=\" text-decoration: underline; color:#2980b9;\">https://github.com/EE-modders/Empire-Earth-Studio-2/issues</span></a><br/></p></body></html>"))
        self.MainTabs.setTabText(self.MainTabs.indexOf(self.tab_main), _translate("MainWindow", "Main"))
        self.tab_ssa_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">file list: </span></p></body></html>"))
        self.tab_ssa_label_clear.setText(_translate("MainWindow", "clear"))
        self.tab_ssa_list_export.setText(_translate("MainWindow", "export list to CSV"))
        self.tab_ssa_select_in.setText(_translate("MainWindow", "Select SSA"))
        self.tab_ssa_select_out.setText(_translate("MainWindow", "Output folder"))
        self.tab_ssa_decompress.setText(_translate("MainWindow", "decompress"))
        self.tab_ssa_kyrillicencode.setToolTip(_translate("MainWindow", "check this for Russian files"))
        self.tab_ssa_kyrillicencode.setText(_translate("MainWindow", "use CP1251 encoding"))
        self.tab_ssa_unpack.setText(_translate("MainWindow", "UNPACK"))
        self.MainTabs.setTabText(self.MainTabs.indexOf(self.tab_ssa), _translate("MainWindow", "Archives (SSA)"))
        self.tab_sst_droplabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">DRAG &amp; DROP HERE!!</span></p><p align=\"center\"><br/>You can drop TGA and SST files!</p><p align=\"center\">(autoconvert on drop)</p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">options:</span></p></body></html>"))
        self.tab_sst_viewonly.setText(_translate("MainWindow", "view only (first dropped)"))
        self.tab_sst_firstonly.setText(_translate("MainWindow", "highest resolution only (SST)"))
        self.tab_sst_donemessage.setText(_translate("MainWindow", "disable success message"))
        self.tab_sst_overwrite.setText(_translate("MainWindow", "force overwrite output"))
        self.tab_sst_bundling.setText(_translate("MainWindow", "disable bundling (TGA)"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt;\">you can also view images with:</span></p><p><span style=\" font-size:8pt;\">File &gt; Open Image Viewer</span></p></body></html>"))
        self.tab_sst_radio_1.setText(_translate("MainWindow", "SST -> TGA"))
        self.tab_sst_radio_2.setText(_translate("MainWindow", "TGA -> SST"))
        self.tab_sst_select_in.setText(_translate("MainWindow", "Bulk convert Folder"))
        self.tab_sst_select_out.setText(_translate("MainWindow", "Output Folder"))
        self.tab_sst_input_checkbox.setText(_translate("MainWindow", "use input location for output"))
        self.tab_sst_convert.setText(_translate("MainWindow", "CONVERT"))
        self.MainTabs.setTabText(self.MainTabs.indexOf(self.tab_sst), _translate("MainWindow", "Textures (SST)"))
        self.label.setText(_translate("MainWindow", "imported files:"))
        self.clear.setText(_translate("MainWindow", "clear"))
        self.tab_slc_moveup.setText(_translate("MainWindow", "up"))
        self.tab_slc_movedown.setText(_translate("MainWindow", "down"))
        self.tab_slc_row_plus.setText(_translate("MainWindow", "+"))
        self.tab_slc_row_count.setText(_translate("MainWindow", "3"))
        self.tab_slc_row_minus.setText(_translate("MainWindow", "-"))
        self.tab_slc_col_minus.setText(_translate("MainWindow", "-"))
        self.tab_slc_col_count.setText(_translate("MainWindow", "4"))
        self.tab_slc_col_plus.setText(_translate("MainWindow", "+"))
        self.tab_slc_select_out.setText(_translate("MainWindow", "Ouput Folder"))
        self.label_9.setText(_translate("MainWindow", "options:"))
        self.tab_slc_select_in.setText(_translate("MainWindow", "Select SST / TGA"))
        self.tab_slc_switchCoords.setText(_translate("MainWindow", "switch X and Y coords in filename"))
        self.tab_slc_slice.setText(_translate("MainWindow", "SLICE"))
        self.tab_slc_join.setText(_translate("MainWindow", "JOIN"))
        self.MainTabs.setTabText(self.MainTabs.indexOf(self.tab_slicer), _translate("MainWindow", "Slicer (SST)"))
        self.main_infotext.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Empire Earth Studio II</span> by zocker_160 from <span style=\" font-weight:600;\">Empire Earth: Reborn</span> - $$$ | GPLv3 | 2020 - 2021</p></body></html>"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionAbout_Studio_II.setText(_translate("MainWindow", "About EEStudio II"))
        self.actionHelp_from_GitHUb.setText(_translate("MainWindow", "Help"))
        self.actionHelp_from_GitHUb.setShortcut(_translate("MainWindow", "F1"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.actionReport_Issue.setText(_translate("MainWindow", "Report Issue"))
        self.actionOpen_Image_Viewer.setText(_translate("MainWindow", "Open Image Viewer"))
        self.actionOpen_Image_Viewer.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionabout_QT.setText(_translate("MainWindow", "About QT"))
from .customwidgets import CDropLabel, CDropWidget, CGraphicsView
from . import mainWindowAssets_rc
