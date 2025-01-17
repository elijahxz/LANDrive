# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LANDriveUserInterface.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1046, 786)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout_12 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setEnabled(True)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMaximumSize(QSize(16777215, 16777215))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(100)
        sizePolicy1.setVerticalStretch(100)
        sizePolicy1.setHeightForWidth(self.page.sizePolicy().hasHeightForWidth())
        self.page.setSizePolicy(sizePolicy1)
        self.page.setMinimumSize(QSize(1024, 768))
        self.verticalLayout_13 = QVBoxLayout(self.page)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.header = QLabel(self.page)
        self.header.setObjectName(u"header")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(100)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setPointSize(36)
        self.header.setFont(font)
        self.header.setLayoutDirection(Qt.LeftToRight)
        self.header.setFrameShape(QFrame.NoFrame)
        self.header.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.header.setMargin(0)

        self.verticalLayout.addWidget(self.header)

        self.verticalSpacer = QSpacerItem(2, 2, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.server_label = QLabel(self.page)
        self.server_label.setObjectName(u"server_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.server_label.sizePolicy().hasHeightForWidth())
        self.server_label.setSizePolicy(sizePolicy3)
        self.server_label.setMinimumSize(QSize(300, 20))
        self.server_label.setMaximumSize(QSize(300, 20))
        font1 = QFont()
        font1.setPointSize(16)
        self.server_label.setFont(font1)

        self.verticalLayout.addWidget(self.server_label, 0, Qt.AlignHCenter)

        self.server_name = QLineEdit(self.page)
        self.server_name.setObjectName(u"server_name")
        sizePolicy3.setHeightForWidth(self.server_name.sizePolicy().hasHeightForWidth())
        self.server_name.setSizePolicy(sizePolicy3)
        self.server_name.setMinimumSize(QSize(300, 30))
        font2 = QFont()
        font2.setPointSize(12)
        self.server_name.setFont(font2)
        self.server_name.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.server_name, 0, Qt.AlignHCenter)

        self.port_label = QLabel(self.page)
        self.port_label.setObjectName(u"port_label")
        self.port_label.setMinimumSize(QSize(300, 20))
        self.port_label.setFont(font1)

        self.verticalLayout.addWidget(self.port_label, 0, Qt.AlignHCenter)

        self.port_number = QLineEdit(self.page)
        self.port_number.setObjectName(u"port_number")
        sizePolicy3.setHeightForWidth(self.port_number.sizePolicy().hasHeightForWidth())
        self.port_number.setSizePolicy(sizePolicy3)
        self.port_number.setMinimumSize(QSize(300, 30))
        self.port_number.setFont(font2)

        self.verticalLayout.addWidget(self.port_number, 0, Qt.AlignHCenter)

        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy4)
        self.label.setMinimumSize(QSize(300, 20))
        self.label.setFont(font1)

        self.verticalLayout.addWidget(self.label, 0, Qt.AlignHCenter)

        self.password = QLineEdit(self.page)
        self.password.setObjectName(u"password")
        sizePolicy3.setHeightForWidth(self.password.sizePolicy().hasHeightForWidth())
        self.password.setSizePolicy(sizePolicy3)
        self.password.setMinimumSize(QSize(300, 30))
        self.password.setFont(font2)
        self.password.setEchoMode(QLineEdit.Password)

        self.verticalLayout.addWidget(self.password, 0, Qt.AlignHCenter)

        self.connect_button = QPushButton(self.page)
        self.connect_button.setObjectName(u"connect_button")
        self.connect_button.setEnabled(True)
        sizePolicy3.setHeightForWidth(self.connect_button.sizePolicy().hasHeightForWidth())
        self.connect_button.setSizePolicy(sizePolicy3)
        self.connect_button.setMinimumSize(QSize(300, 150))
        font3 = QFont()
        font3.setPointSize(26)
        self.connect_button.setFont(font3)

        self.verticalLayout.addWidget(self.connect_button, 0, Qt.AlignHCenter)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.connect_label = QLabel(self.page)
        self.connect_label.setObjectName(u"connect_label")
        sizePolicy3.setHeightForWidth(self.connect_label.sizePolicy().hasHeightForWidth())
        self.connect_label.setSizePolicy(sizePolicy3)
        self.connect_label.setMinimumSize(QSize(400, 100))
        self.connect_label.setMaximumSize(QSize(400, 300))
        self.connect_label.setBaseSize(QSize(0, 0))
        font4 = QFont()
        font4.setPointSize(14)
        self.connect_label.setFont(font4)
        self.connect_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.connect_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.connect_label, 0, Qt.AlignHCenter)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.verticalLayout_13.addLayout(self.horizontalLayout)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        sizePolicy1.setHeightForWidth(self.page_2.sizePolicy().hasHeightForWidth())
        self.page_2.setSizePolicy(sizePolicy1)
        self.page_2.setMinimumSize(QSize(1024, 768))
        self.verticalLayout_14 = QVBoxLayout(self.page_2)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetMaximumSize)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout_6.setContentsMargins(0, 0, -1, -1)
        self.disconnect_button = QPushButton(self.page_2)
        self.disconnect_button.setObjectName(u"disconnect_button")
        sizePolicy3.setHeightForWidth(self.disconnect_button.sizePolicy().hasHeightForWidth())
        self.disconnect_button.setSizePolicy(sizePolicy3)
        self.disconnect_button.setMinimumSize(QSize(100, 60))
        self.disconnect_button.setFont(font2)

        self.horizontalLayout_6.addWidget(self.disconnect_button)

        self.header_2 = QLabel(self.page_2)
        self.header_2.setObjectName(u"header_2")
        sizePolicy2.setHeightForWidth(self.header_2.sizePolicy().hasHeightForWidth())
        self.header_2.setSizePolicy(sizePolicy2)
        self.header_2.setFont(font)
        self.header_2.setLayoutDirection(Qt.LeftToRight)
        self.header_2.setFrameShape(QFrame.NoFrame)
        self.header_2.setAlignment(Qt.AlignCenter)
        self.header_2.setMargin(0)

        self.horizontalLayout_6.addWidget(self.header_2)

        self.users = QLabel(self.page_2)
        self.users.setObjectName(u"users")
        sizePolicy3.setHeightForWidth(self.users.sizePolicy().hasHeightForWidth())
        self.users.setSizePolicy(sizePolicy3)
        self.users.setMinimumSize(QSize(100, 0))
        self.users.setFont(font2)
        self.users.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_6.addWidget(self.users)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SetMaximumSize)
        self.back = QPushButton(self.page_2)
        self.back.setObjectName(u"back")
        sizePolicy3.setHeightForWidth(self.back.sizePolicy().hasHeightForWidth())
        self.back.setSizePolicy(sizePolicy3)
        self.back.setMinimumSize(QSize(100, 60))
        self.back.setFont(font2)

        self.horizontalLayout_4.addWidget(self.back)

        self.dir_name = QLabel(self.page_2)
        self.dir_name.setObjectName(u"dir_name")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.dir_name.sizePolicy().hasHeightForWidth())
        self.dir_name.setSizePolicy(sizePolicy5)
        self.dir_name.setFont(font1)
        self.dir_name.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.dir_name)

        self.updated = QLabel(self.page_2)
        self.updated.setObjectName(u"updated")
        sizePolicy3.setHeightForWidth(self.updated.sizePolicy().hasHeightForWidth())
        self.updated.setSizePolicy(sizePolicy3)
        self.updated.setMinimumSize(QSize(100, 60))

        self.horizontalLayout_4.addWidget(self.updated)

        self.horizontalLayout_4.setStretch(2, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.tableWidget = QTableWidget(self.page_2)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem.setFont(font2);
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem1.setFont(font2);
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem2.setFont(font2);
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        if (self.tableWidget.rowCount() < 21):
            self.tableWidget.setRowCount(21)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setItem(0, 0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setItem(1, 0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setItem(1, 1, __qtablewidgetitem5)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy6.setHorizontalStretch(100)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy6)
        self.tableWidget.setMinimumSize(QSize(0, 0))
        self.tableWidget.setMaximumSize(QSize(16777215, 16777215))
        self.tableWidget.setFont(font2)
        self.tableWidget.setLayoutDirection(Qt.LeftToRight)
        self.tableWidget.setAutoFillBackground(False)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setTextElideMode(Qt.ElideRight)
        self.tableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setGridStyle(Qt.SolidLine)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setRowCount(21)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(40)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(300)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(50)
        self.tableWidget.verticalHeader().setProperty("showSortIndicator", False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_4.addWidget(self.tableWidget)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.refresh = QPushButton(self.page_2)
        self.refresh.setObjectName(u"refresh")
        sizePolicy3.setHeightForWidth(self.refresh.sizePolicy().hasHeightForWidth())
        self.refresh.setSizePolicy(sizePolicy3)
        self.refresh.setMinimumSize(QSize(100, 60))
        self.refresh.setFont(font2)

        self.horizontalLayout_5.addWidget(self.refresh)

        self.upload = QPushButton(self.page_2)
        self.upload.setObjectName(u"upload")
        sizePolicy3.setHeightForWidth(self.upload.sizePolicy().hasHeightForWidth())
        self.upload.setSizePolicy(sizePolicy3)
        self.upload.setMinimumSize(QSize(100, 60))
        self.upload.setFont(font2)

        self.horizontalLayout_5.addWidget(self.upload)

        self.create_dir = QPushButton(self.page_2)
        self.create_dir.setObjectName(u"create_dir")
        sizePolicy3.setHeightForWidth(self.create_dir.sizePolicy().hasHeightForWidth())
        self.create_dir.setSizePolicy(sizePolicy3)
        self.create_dir.setMinimumSize(QSize(100, 60))
        self.create_dir.setFont(font2)

        self.horizontalLayout_5.addWidget(self.create_dir)

        self.label_9 = QLabel(self.page_2)
        self.label_9.setObjectName(u"label_9")
        sizePolicy5.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy5)

        self.horizontalLayout_5.addWidget(self.label_9)

        self.delete_2 = QPushButton(self.page_2)
        self.delete_2.setObjectName(u"delete_2")
        sizePolicy3.setHeightForWidth(self.delete_2.sizePolicy().hasHeightForWidth())
        self.delete_2.setSizePolicy(sizePolicy3)
        self.delete_2.setMinimumSize(QSize(100, 60))
        self.delete_2.setFont(font2)

        self.horizontalLayout_5.addWidget(self.delete_2)

        self.download = QPushButton(self.page_2)
        self.download.setObjectName(u"download")
        sizePolicy3.setHeightForWidth(self.download.sizePolicy().hasHeightForWidth())
        self.download.setSizePolicy(sizePolicy3)
        self.download.setMinimumSize(QSize(100, 60))
        self.download.setFont(font2)

        self.horizontalLayout_5.addWidget(self.download)

        self.edit = QPushButton(self.page_2)
        self.edit.setObjectName(u"edit")
        sizePolicy3.setHeightForWidth(self.edit.sizePolicy().hasHeightForWidth())
        self.edit.setSizePolicy(sizePolicy3)
        self.edit.setMinimumSize(QSize(100, 60))
        self.edit.setFont(font2)

        self.horizontalLayout_5.addWidget(self.edit)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)


        self.horizontalLayout_3.addLayout(self.verticalLayout_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.verticalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout_2.setStretch(1, 1)

        self.horizontalLayout_2.addLayout(self.verticalLayout_2)


        self.verticalLayout_14.addLayout(self.horizontalLayout_2)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        sizePolicy1.setHeightForWidth(self.page_3.sizePolicy().hasHeightForWidth())
        self.page_3.setSizePolicy(sizePolicy1)
        self.page_3.setMinimumSize(QSize(1024, 768))
        self.verticalLayout_15 = QVBoxLayout(self.page_3)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout_8.setContentsMargins(0, 0, -1, -1)
        self.disconnect_2 = QPushButton(self.page_3)
        self.disconnect_2.setObjectName(u"disconnect_2")
        sizePolicy3.setHeightForWidth(self.disconnect_2.sizePolicy().hasHeightForWidth())
        self.disconnect_2.setSizePolicy(sizePolicy3)
        self.disconnect_2.setMinimumSize(QSize(100, 60))
        self.disconnect_2.setFont(font2)

        self.horizontalLayout_8.addWidget(self.disconnect_2)

        self.header_3 = QLabel(self.page_3)
        self.header_3.setObjectName(u"header_3")
        sizePolicy2.setHeightForWidth(self.header_3.sizePolicy().hasHeightForWidth())
        self.header_3.setSizePolicy(sizePolicy2)
        self.header_3.setFont(font)
        self.header_3.setLayoutDirection(Qt.LeftToRight)
        self.header_3.setFrameShape(QFrame.NoFrame)
        self.header_3.setAlignment(Qt.AlignCenter)
        self.header_3.setMargin(0)

        self.horizontalLayout_8.addWidget(self.header_3)

        self.users_2 = QLabel(self.page_3)
        self.users_2.setObjectName(u"users_2")
        sizePolicy3.setHeightForWidth(self.users_2.sizePolicy().hasHeightForWidth())
        self.users_2.setSizePolicy(sizePolicy3)
        self.users_2.setMinimumSize(QSize(100, 0))
        self.users_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.users_2)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.edit_file_name = QLabel(self.page_3)
        self.edit_file_name.setObjectName(u"edit_file_name")
        font5 = QFont()
        font5.setPointSize(18)
        self.edit_file_name.setFont(font5)
        self.edit_file_name.setWordWrap(True)

        self.verticalLayout_5.addWidget(self.edit_file_name)

        self.file_contents_area = QTextEdit(self.page_3)
        self.file_contents_area.setObjectName(u"file_contents_area")
        self.file_contents_area.setFont(font2)
        self.file_contents_area.setTabStopDistance(20.000000000000000)

        self.verticalLayout_5.addWidget(self.file_contents_area)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(-1, -1, -1, 0)
        self.cancel = QPushButton(self.page_3)
        self.cancel.setObjectName(u"cancel")
        sizePolicy3.setHeightForWidth(self.cancel.sizePolicy().hasHeightForWidth())
        self.cancel.setSizePolicy(sizePolicy3)
        self.cancel.setMinimumSize(QSize(100, 60))
        self.cancel.setFont(font2)

        self.horizontalLayout_9.addWidget(self.cancel)

        self.label_14 = QLabel(self.page_3)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_9.addWidget(self.label_14)

        self.save = QPushButton(self.page_3)
        self.save.setObjectName(u"save")
        sizePolicy3.setHeightForWidth(self.save.sizePolicy().hasHeightForWidth())
        self.save.setSizePolicy(sizePolicy3)
        self.save.setMinimumSize(QSize(100, 60))
        self.save.setFont(font2)

        self.horizontalLayout_9.addWidget(self.save, 0, Qt.AlignRight)

        self.horizontalLayout_9.setStretch(0, 1)
        self.horizontalLayout_9.setStretch(2, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_9)


        self.verticalLayout_15.addLayout(self.verticalLayout_5)

        self.stackedWidget.addWidget(self.page_3)

        self.verticalLayout_12.addWidget(self.stackedWidget, 0, Qt.AlignHCenter)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"LANDrive", None))
        self.header.setText(QCoreApplication.translate("MainWindow", u"Welcome to LANDrive!!!", None))
        self.server_label.setText(QCoreApplication.translate("MainWindow", u"Server Name", None))
        self.server_name.setText("")
        self.port_label.setText(QCoreApplication.translate("MainWindow", u"Port", None))
        self.port_number.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.connect_button.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.connect_label.setText("")
        self.disconnect_button.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
        self.header_2.setText(QCoreApplication.translate("MainWindow", u"LANDrive", None))
        self.users.setText(QCoreApplication.translate("MainWindow", u"Users: ", None))
        self.back.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.dir_name.setText(QCoreApplication.translate("MainWindow", u"Directory:", None))
        self.updated.setText(QCoreApplication.translate("MainWindow", u"Last Updated:", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Name", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Date modified", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Size", None));

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)

        self.refresh.setText(QCoreApplication.translate("MainWindow", u"Refresh Files", None))
        self.upload.setText(QCoreApplication.translate("MainWindow", u"Upload a File", None))
        self.create_dir.setText(QCoreApplication.translate("MainWindow", u"Create Dir", None))
        self.label_9.setText("")
        self.delete_2.setText(QCoreApplication.translate("MainWindow", u"Delete File", None))
        self.download.setText(QCoreApplication.translate("MainWindow", u"Download File", None))
        self.edit.setText(QCoreApplication.translate("MainWindow", u"Edit File", None))
        self.disconnect_2.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
        self.header_3.setText(QCoreApplication.translate("MainWindow", u"LANDrive", None))
        self.users_2.setText(QCoreApplication.translate("MainWindow", u"Users: ", None))
        self.edit_file_name.setText(QCoreApplication.translate("MainWindow", u"TextFile Name and other information here", None))
        self.file_contents_area.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI';\">This is a test</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI';\">	tab</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI';\">		doubletab</span></p></body></html>", None))
        self.cancel.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.label_14.setText("")
        self.save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
    # retranslateUi

