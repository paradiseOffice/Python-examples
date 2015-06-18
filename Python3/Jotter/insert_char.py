#!/usr/bin/env python3
"""
/********************************************************
*
* Jotter, part of the Paradise Office suite.
* Copyright (C) Hazel Windle, with some parts from QTrac & Digia Plc
*
* This program is free software; you can redistribute it and/or
* modify it under the terms of the GNU General Public License
* as published by the Free Software Foundation; either version 2
* of the License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program; if not, write to the Free Software
* Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
* Also add information on how to contact you by electronic and paper mail.
*
**********************************************************/
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class InsertChar(QDialog):

    def __init__(self, parent=None):
        super(InsertChar, self).__init__(parent)
        
        self.character = ""
        self.setMinimumSize(QSize(650,450))
        self.setWindowTitle("Insert Character")
        helptext = QLabel("Select a character to include in your document: ")
        middleLayout = QVBoxLayout()
        charFont = QFont("Courier", 14)
        #initialFont.setFamily("Courier")
        #initialFont.setStyleHint(QFont.Monospace)
        #initialFont.setFixedPitch(True)
        #initialFont.setPointSize(14)
        #initialFont.setStyle(QFont.Regular)
        firstGroupBox = QGroupBox("C&urrency")
        currencyGroup = QVBoxLayout()
        self.euroBtn = QRadioButton("\u20ac")
        currencyGroup.addWidget(self.euroBtn)
        self.dollarBtn = QRadioButton("$")
        currencyGroup.addWidget(self.dollarBtn)
        self.yenBtn = QRadioButton("\u00A5")
        currencyGroup.addWidget(self.yenBtn)
        self.gbpBtn = QRadioButton("£")
        currencyGroup.addWidget(self.gbpBtn)
        self.centBtn = QRadioButton("\u00A2")
        currencyGroup.addWidget(self.centBtn)
        firstGroupBox.setLayout(currencyGroup)

        secondGroupBox = QGroupBox("&Symbols")
        symbolsGroup = QVBoxLayout()
        self.leftquoteBtn = QRadioButton("\u201C")
        symbolsGroup.addWidget(self.leftquoteBtn)
        self.rightquoteBtn = QRadioButton("\u201D")
        symbolsGroup.addWidget(self.rightquoteBtn)
        self.ltBtn = QRadioButton("<")
        symbolsGroup.addWidget(self.ltBtn)
        self.gtBtn = QRadioButton(">")
        symbolsGroup.addWidget(self.gtBtn)
        self.ampBtn = QRadioButton("&")
        symbolsGroup.addWidget(self.ampBtn)
        self.copyrBtn = QRadioButton("\u00A9")
        symbolsGroup.addWidget(self.copyrBtn)
        self.tmBtn = QRadioButton("\u00AE")
        symbolsGroup.addWidget(self.tmBtn)
        secondGroupBox.setLayout(symbolsGroup)

        thirdGroupBox = QGroupBox("&Other")
        otherGroup = QVBoxLayout()
        self.eacuteBtn = QRadioButton("\u00E9")
        otherGroup.addWidget(self.eacuteBtn)
        self.aumlautsBtn = QRadioButton("\u00E4")
        otherGroup.addWidget(self.aumlautsBtn)
        self.eumlautsBtn = QRadioButton("\u00EB")
        otherGroup.addWidget(self.eumlautsBtn)
        self.uumlautsBtn = QRadioButton("\u00FC")
        otherGroup.addWidget(self.uumlautsBtn)
        thirdGroupBox.setLayout(otherGroup)
        radioButtons = ("self.euroBtn", "self.dollarBtn", "self.yenBtn", "self.gbpBtn", "self.centBtn", "self.leftquoteBtn", "self.rightquoteBtn", "self.ltBtn", "self.gtBtn", "self.ampBtn", "self.copyrBtn", "self.tmBtn", "self.eacuteBtn", "self.aumlautsBtn", "self.eumlautsBtn", "self.uumlautsBtn")
        for radioBtn in radioButtons:
            pass
            #radioBtn.font(charFont)
        self.htmlCheckBox = QCheckBox("Web friendly character (&#xxx;)")
        self.connect(firstGroupBox, SIGNAL("isChecked()"), self.getChar)
        self.connect(secondGroupBox, SIGNAL("isChecked()"), self.getChar)
        self.connect(thirdGroupBox, SIGNAL("isChecked()"), self.getChar)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        mainLayout = QGridLayout()
        mainLayout.addWidget(helptext, 0, 0)
        mainLayout.addWidget(firstGroupBox, 1, 0)
        mainLayout.addWidget(secondGroupBox, 1, 1)
        mainLayout.addWidget(thirdGroupBox, 1, 2)
        mainLayout.addWidget(self.htmlCheckBox, 2, 0)
        mainLayout.addWidget(buttonBox, 3, 0)
        self.setLayout(mainLayout)
        # connections
        self.connect(buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(buttonBox, SIGNAL("rejected()"), self.reject)
        
    def getChar(self):
        if self.euroBtn.isChecked():
            if self.htmlCheckBox.isChecked():
                self.character = "&euro;"
            else:
                self.character = "\u20AC"
        elif self.dollarBtn.isChecked():
            self.character = "$"
        elif self.yenBtn.isChecked():
            if self.htmlCheckBox.isChecked():
                self.character = "&yen;"
            else:
                self.character = self.yenBtn.text()
        elif self.gbpBtn.isChecked():
            self.character = self.gbpBtn.text()
        elif self.centBtn.isChecked():
            if self.htmlCheckBox.isChecked():
                self.character = "&cent;"
            else:
                self.character = self.centBtn.text()
        elif self.leftquoteBtn.isChecked():
            if self.htmlCheckBox.isChecked():
                self.character = "&#8220;"
            else:
                self.character = self.leftquoteBtn.text()
        elif self.rightquoteBtn.isChecked():
            if self.htmlCheckBox.isChecked():
                self.character = "&#8221;"
            else:
                self.character = self.rightquoteBtn.text()
        elif self.ltBtn.isChecked():
            if self.htmlCheckBox.isChecked():
                self.character = "&lt;"
            else:
                self.character = self.ltBtn.text()
        elif self.gtBtn.isChecked():
            if self.htmlCheckBox.isChecked():
                self.character = "&gt;"
            else:
                self.character = self.gtBtn.text()
        elif self.ampBtn.isChecked():
            if self.htmlCheckBox.isChecked():
                self.character = "&amp;"
            else:
                self.character = self.ampBtn.text()
        elif self.copyrBtn.isChecked():
            if self.htmlCheckBox.isChecked():
                self.character = "&copy;"
            else:
                self.character = self.copyrBtn.text()
        elif self.tmBtn.isChecked():
            if self.htmlCheckBox.isChecked():
                self.character = "&reg;"
            else:
                self.character = self.tmBtn.text()
        elif self.eacuteBtn.isChecked():
            if self.htmlCheckBox.isChecked():
                self.character = "&#233;"
            else:
                self.character = self.eacuteBtn.text()
        elif self.aumlautsBtn.isChecked():
            if self.htmlCheckBox.isChecked():
                self.character = "&#228;"
            else:            
                self.character = self.aumlautsBtn.text()
        elif self.eumlautsBtn.isChecked():
            if self.htmlCheckBox.isChecked():
                self.character = "&#235;"
            else:
                self.character = self.eumlautsBtn.text()
        elif self.uumlautsBtn.isChecked():
            if self.htmlCheckBox.isChecked():
                self.character = "&#252;"
            else:
                self.character = self.uumlautsBtn.text()
        return self.character

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = InsertChar()
    form.show()
    app.exec_()
