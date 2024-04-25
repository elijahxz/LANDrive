# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UploadUserInterface.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        #Form.setWindowFlag(Qt.WindowCloseButtonHint, False)
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setEnabled(True)
        Form.resize(439, 372)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)

        self.verticalLayout.addWidget(self.label_3)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setPointSize(16)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.files = QLabel(Form)
        self.files.setObjectName(u"files")
        self.files.setEnabled(True)
        self.files.setTextFormat(Qt.AutoText)
        self.files.setScaledContents(False)
        self.files.setAlignment(Qt.AlignCenter)
        self.files.setWordWrap(True)

        self.verticalLayout.addWidget(self.files)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.closeBtn = QPushButton(Form)
        self.closeBtn.setObjectName(u"close")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.closeBtn.sizePolicy().hasHeightForWidth())
        self.closeBtn.setSizePolicy(sizePolicy2)
        self.closeBtn.setMinimumSize(QSize(120, 45))
        font2 = QFont()
        font2.setPointSize(11)
        self.closeBtn.setFont(font2)
        self.closeBtn.setLayoutDirection(Qt.LeftToRight)
        self.closeBtn.setAutoRepeat(False)

        self.verticalLayout.addWidget(self.closeBtn, 0, Qt.AlignHCenter)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"File Upload Results", None))
        self.label_3.setText("")
        self.label.setText(QCoreApplication.translate("Form", u"Uploaded Files Status:", None))
        self.files.setText("")
        self.closeBtn.setText(QCoreApplication.translate("Form", u"Close", None))
    # retranslateUi

