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
import qrc_jotter

class HelpViewer(QDialog):

    def __init__(self, page, parent=None):
        super(HelpViewer, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_GroupLeader)

        backAction = QAction(QIcon(":/images/win/back_128x128.png"), "&Back", self)
        backAction.setShortcut(QKeySequence.Back)
        homeAction = QAction(QIcon(":/images/win/property_128x128.png"), "&Home", self)
        homeAction.setShortcut("Home")
        self.pageLabel = QLabel()

        toolBar = QToolBar()
        toolBar.addAction(backAction)
        toolBar.addAction(homeAction)
        toolBar.addWidget(self.pageLabel)
        self.textBrowser = QTextBrowser()

        layout = QVBoxLayout()
        layout.addWidget(toolBar)
        layout.addWidget(self.textBrowser, 1)
        self.setLayout(layout)

        self.connect(backAction, SIGNAL("triggered()"),
                     self.textBrowser, SLOT("backward()"))
        self.connect(homeAction, SIGNAL("triggered()"),
                     self.textBrowser, SLOT("home()"))
        self.connect(self.textBrowser, SIGNAL("sourceChanged(QUrl)"),
                     self.updatePageTitle)

        self.textBrowser.setSearchPaths(["help"])
        self.textBrowser.setSource(QUrl(page))
        self.resize(500, 700)
        self.setWindowTitle("{} Help".format(
                QApplication.applicationName()))

    """
    Something
    """
    def updatePageTitle(self):
        self.pageLabel.setText(self.textBrowser.documentTitle())


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = HelpViewer("index.html")
    form.show()
    app.exec_()