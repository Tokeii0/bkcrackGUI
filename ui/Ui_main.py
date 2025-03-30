# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QWidget)

from qfluentwidgets import (PlainTextEdit, PushButton, TextBrowser)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1218, 481)
        Form.setAutoFillBackground(False)
        Form.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.SelectCompressedFile = PushButton(Form)
        self.SelectCompressedFile.setObjectName(u"SelectCompressedFile")
        self.SelectCompressedFile.setGeometry(QRect(10, 30, 91, 31))
        font = QFont()
        font.setFamilies([u"\u534e\u6587\u4e2d\u5b8b"])
        font.setPointSize(10)
        font.setBold(True)
        self.SelectCompressedFile.setFont(font)
        self.SelectCompressedFile.setStyleSheet(u"background-color: rgb(197, 0, 99);")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 81, 16))
        self.label.setFont(font)
        self.OutPutArea = TextBrowser(Form)
        self.OutPutArea.setObjectName(u"OutPutArea")
        self.OutPutArea.setGeometry(QRect(430, 20, 761, 441))
        font1 = QFont()
        font1.setFamilies([u"Cascadia Code"])
        font1.setPointSize(10)
        self.OutPutArea.setFont(font1)
        self.OutPutArea.setAutoFillBackground(False)
        self.OutPutArea.setStyleSheet(u"color: rgb(255, 255, 127);\n"
"border-color: rgb(255, 170, 255);")
        self.CompressedZipInfo = PushButton(Form)
        self.CompressedZipInfo.setObjectName(u"CompressedZipInfo")
        self.CompressedZipInfo.setGeometry(QRect(10, 100, 401, 31))
        self.CompressedZipInfo.setFont(font)
        self.CompressedZipInfo.setStyleSheet(u"background-color: rgb(197, 0, 99);")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 140, 151, 16))
        self.label_2.setFont(font)
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 190, 281, 16))
        self.label_3.setFont(font)
        self.SelectPlainFile = PushButton(Form)
        self.SelectPlainFile.setObjectName(u"SelectPlainFile")
        self.SelectPlainFile.setGeometry(QRect(10, 210, 91, 31))
        self.SelectPlainFile.setFont(font)
        self.SelectPlainFile.setStyleSheet(u"background-color: rgb(197, 0, 99);")
        self.StartAttack = PushButton(Form)
        self.StartAttack.setObjectName(u"StartAttack")
        self.StartAttack.setGeometry(QRect(10, 280, 401, 31))
        self.StartAttack.setFont(font)
        self.StartAttack.setStyleSheet(u"background-color: rgb(197, 0, 99);")
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 320, 281, 16))
        self.label_4.setFont(font)
        self.InputKey = PlainTextEdit(Form)
        self.InputKey.setObjectName(u"InputKey")
        self.InputKey.setGeometry(QRect(10, 340, 401, 25))
        font2 = QFont()
        font2.setFamilies([u"Cascadia Code"])
        font2.setPointSize(9)
        self.InputKey.setFont(font2)
        self.InputKey.setAutoFillBackground(False)
        self.InputKey.setStyleSheet(u"color: rgb(255, 255, 127);\n"
"background-color: rgb(35, 35, 35);")
        self.InputKey.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.InputKey.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.InputKey.setBackgroundVisible(False)
        self.ExportZip = PushButton(Form)
        self.ExportZip.setObjectName(u"ExportZip")
        self.ExportZip.setGeometry(QRect(10, 370, 401, 31))
        self.ExportZip.setFont(font)
        self.ExportZip.setStyleSheet(u"background-color: rgb(197, 0, 99);")
        self.ViewCompressedZip = TextBrowser(Form)
        self.ViewCompressedZip.setObjectName(u"ViewCompressedZip")
        self.ViewCompressedZip.setGeometry(QRect(10, 70, 401, 25))
        font3 = QFont()
        font3.setFamilies([u"Cascadia Code"])
        self.ViewCompressedZip.setFont(font3)
        self.ViewCompressedZip.setAutoFillBackground(False)
        self.ViewCompressedZip.setStyleSheet(u"color: rgb(255, 255, 127);\n"
"border-color: rgb(255, 170, 255);")
        self.ViewCompressedZip.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.PlainName = PlainTextEdit(Form)
        self.PlainName.setObjectName(u"PlainName")
        self.PlainName.setGeometry(QRect(10, 160, 401, 25))
        font4 = QFont()
        font4.setFamilies([u"Cascadia Code"])
        font4.setPointSize(9)
        font4.setBold(False)
        self.PlainName.setFont(font4)
        self.PlainName.setAutoFillBackground(False)
        self.PlainName.setStyleSheet(u"color: rgb(255, 255, 127);\n"
"background-color: rgb(35, 35, 35);")
        self.PlainName.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.PlainName.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.PlainName.setBackgroundVisible(False)
        self.ViewPlainFile = TextBrowser(Form)
        self.ViewPlainFile.setObjectName(u"ViewPlainFile")
        self.ViewPlainFile.setGeometry(QRect(10, 250, 401, 25))
        self.ViewPlainFile.setFont(font3)
        self.ViewPlainFile.setAutoFillBackground(False)
        self.ViewPlainFile.setStyleSheet(u"color: rgb(255, 255, 127);\n"
"border-color: rgb(255, 170, 255);")
        self.ViewPlainFile.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"bkcrack-gui", None))
        self.SelectCompressedFile.setText(QCoreApplication.translate("Form", u"\u9009\u62e9\u6587\u4ef6", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u52a0\u5bc6\u7684\u538b\u7f29\u5305", None))
        self.CompressedZipInfo.setText(QCoreApplication.translate("Form", u"\u67e5\u770b\u538b\u7f29\u5305\u4fe1\u606f", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u660e\u6587\u6587\u4ef6\u540d\u79f0", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u660e\u6587\u8def\u5f84 (\u9884\u5236\u660e\u6587\u5728 plains \u6587\u4ef6\u5939\u4e2d)", None))
        self.SelectPlainFile.setText(QCoreApplication.translate("Form", u"\u9009\u62e9\u6587\u4ef6", None))
        self.StartAttack.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb\u653b\u51fb", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u5bc6\u94a5", None))
        self.ExportZip.setText(QCoreApplication.translate("Form", u"\u5bfc\u51fa\u65e0\u5bc6\u7801\u538b\u7f29\u5305", None))
    # retranslateUi

