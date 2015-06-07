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

class InsertDate(QDialog):

    timestamp = ""

    def __init__(self, parent=None):
        super(InsertDate, self).__init__(parent)
        
        self.today = QDate.currentDate()
        self.now = QTime.currentTime()
        
        self.setMinimumSize(QSize(450,350))
        self.setWindowTitle("Insert Date or Time")
        self.todayRadioBtn = QCheckBox("&Today")
        #dateRadioBtn = QCheckBox("&Date picked below: ")
        self.datePicker = QCalendarWidget()#QDateEdit()
        self.datePicker.setSelectedDate(self.today)
        leftGrid = QGridLayout()
        leftGrid.addWidget(self.todayRadioBtn, 0, 0)
        #leftGrid.addWidget(dateRadioBtn, 1, 0)
        leftGrid.addWidget(self.datePicker, 1, 0)
        self.nowRadioBtn = QCheckBox("&Now")
        laterRadioBtn = QCheckBox("&A Different Time")
        self.timePicker = QTimeEdit()
        rightGrid = QGridLayout()
        rightGrid.addWidget(self.nowRadioBtn, 0, 0)
        rightGrid.addWidget(laterRadioBtn, 1, 0)
        rightGrid.addWidget(self.timePicker, 2, 0)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        mainLayout = QGridLayout()
        mainLayout.addLayout(leftGrid, 0, 0)
        mainLayout.addLayout(rightGrid, 0, 1)
        stretch = QLabel()
        mainLayout.addWidget(stretch, 1, 0)
        mainLayout.addWidget(buttonBox, 1, 1)
        self.setLayout(mainLayout)
        # connections       
        self.connect(self.datePicker, SIGNAL("selectionChanged()"), self.setDate)
        self.connect(self.timePicker, SIGNAL("triggered()"), self.setTime)
        self.connect(self.todayRadioBtn, SIGNAL("stateChanged()"), self.setDate)
        self.connect(self.nowRadioBtn, SIGNAL("stateChanged()"), self.setTime)
        self.connect(buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(buttonBox, SIGNAL("rejected()"), self.reject)
        

    def setDate(self):
        date = QDate()
        if self.todayRadioBtn.isChecked():
            date = self.today
        date = self.datePicker.selectedDate()
        self.datestring = ""
        if date.isValid():            
            self.datestring = date.toString("dd.MM.yyyy")
        InsertDate.timestamp += self.datestring

    def setTime(self):
        time = QTime()
        if self.nowRadioBtn.isChecked():
            time = self.now
        time = self.timePicker.selectedTime()
        self.timeString = ""
        if time.isValid():            
            self.timeString = time.toString("HH:mm")
        InsertDate.timestamp += self.timeString
            

        


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = InsertDate()
    form.show()
    app.exec_()
