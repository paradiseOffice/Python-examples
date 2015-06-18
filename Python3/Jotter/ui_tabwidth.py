# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tabWidth.ui'
#
# Created: Thu Jul 24 16:04:15 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_dialogTabWidth(object):
    def setupUi(self, dialogTabWidth):
        dialogTabWidth.setObjectName(_fromUtf8("dialogTabWidth"))
        dialogTabWidth.resize(344, 221)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/win/logo32.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        dialogTabWidth.setWindowIcon(icon)
        self.layoutWidget = QtGui.QWidget(dialogTabWidth)
        self.layoutWidget.setGeometry(QtCore.QRect(5, 6, 335, 211))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.help = QtGui.QLabel(self.layoutWidget)
        self.help.setFrameShape(QtGui.QFrame.Box)
        self.help.setFrameShadow(QtGui.QFrame.Raised)
        self.help.setTextFormat(QtCore.Qt.RichText)
        self.help.setWordWrap(True)
        self.help.setMargin(-5)
        self.help.setObjectName(_fromUtf8("help"))
        self.verticalLayout.addWidget(self.help)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.tabSpinBox = QtGui.QSpinBox(self.layoutWidget)
        self.tabSpinBox.setMinimum(2)
        self.tabSpinBox.setMaximum(20)
        self.tabSpinBox.setObjectName(_fromUtf8("tabSpinBox"))
        self.horizontalLayout.addWidget(self.tabSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtGui.QSpacerItem(330, 25, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        self.verticalLayout.addItem(spacerItem)
        self.okCancel = QtGui.QDialogButtonBox(self.layoutWidget)
        self.okCancel.setOrientation(QtCore.Qt.Horizontal)
        self.okCancel.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.okCancel.setCenterButtons(False)
        self.okCancel.setObjectName(_fromUtf8("okCancel"))
        self.verticalLayout.addWidget(self.okCancel)

        self.retranslateUi(dialogTabWidth)
        QtCore.QObject.connect(self.okCancel, QtCore.SIGNAL(_fromUtf8("accepted()")), dialogTabWidth.accept)
        QtCore.QObject.connect(self.okCancel, QtCore.SIGNAL(_fromUtf8("rejected()")), dialogTabWidth.reject)
        QtCore.QMetaObject.connectSlotsByName(dialogTabWidth)
        dialogTabWidth.setTabOrder(self.tabSpinBox, self.okCancel)

    def retranslateUi(self, dialogTabWidth):
        dialogTabWidth.setWindowTitle(_translate("dialogTabWidth", "Tab Width", None))
        self.help.setText(_translate("dialogTabWidth", "The number entered here sets the width for when the <br /><b>tab key</b> is pressed. <br />This is set to <b>4 spaces</b> to begin with.", None))
        self.label.setText(_translate("dialogTabWidth", "<h2>Spaces</h2>", None))

