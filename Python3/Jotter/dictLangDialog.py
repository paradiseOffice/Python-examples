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


import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class DictLangDialog(QDialog):
    
    selectedLang = "British"

    def __init__(self, parent=None):
        super(DictLangDialog, self).__init__(parent)

        self.setWindowTitle("Spelling Dictionaries")
        helptext = QLabel("Set the dictionary language below to spellcheck in a different language. ")
        self.dictLangList = QListWidget()
        self.dictLangList.setMinimumSize(300, 200)
        langStrings = []
        langStrings.append("British")
        langStrings.append("United States")
        langStrings.append("Chinese")
        langStrings.append("Russian")
        langStrings.append("German")
        langStrings.append("French")
        langStrings.append("Norwegian")
        langStrings.append("Zulu")
        langStrings.append("Arabic")
        langStrings.append("Hindi")
        self.dictLangList.addItems(langStrings)
        self.dictLangList.setCurrentRow(0)
        # set up the buttons OK and Cancel
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        layout = QVBoxLayout()
        layout.addWidget(helptext)
        layout.addWidget(self.dictLangList)
        layout.addWidget(buttonBox)
        self.setLayout(layout)
        # connections
        self.connect(self.dictLangList, SIGNAL("currentRowChanged()"), self.setLang)
        self.connect(buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(buttonBox, SIGNAL("rejected()"), self.reject)

    def setLang(self):
        row = self.dictLangList.currentRow()
        item = self.dictLangList.item(row)
        DictLangDialog.selectedLang = item.text()
        print(DictLangDialog.selectedLang)
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = DictLangDialog()
    form.show()
    app.exec_()

