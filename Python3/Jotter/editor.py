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
import tabwidth

class Editor(QTextEdit):
    
    """
    Line Numbers:
    When combining with the editor it needs these (modified) bits in too:
     hbox = QHBoxLayout(self)
        hbox.setSpacing(0)
        hbox.setMargin(0)
        hbox.addWidget(self.number_bar)
        hbox.addWidget(self.edit)
 
        self.edit.blockCountChanged.connect(self.number_bar.adjustWidth)
        self.edit.updateRequest.connect(self.number_bar.updateContents)
    """


    tWidth = 4
    NextId = 1 # for file numbers in new filenames

    def __init__(self, filename="", parent=None):
        super(Editor, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.filename = filename
        if not self.filename:
            self.filename = "New - {}".format(Editor.NextId)
            Editor.NextId += 1
        self.document().setModified(False)
        self.setWindowTitle(QFileInfo(self.filename).fileName())
        # set up an initial font
        initialFont = QFont()
        initialFont.setFamily("Courier")
        initialFont.setStyleHint(QFont.Monospace)
        initialFont.setFixedPitch(True)
        initialFont.setPointSize(12)
        self.alterFont(initialFont)
        self.setFont(initialFont)
        # set the tab width, spaces
        metrics = QFontMetrics(initialFont)
        self.setTabStopWidth(Editor.tWidth * metrics.width('H'))
        # Line numbers...

        #self.lineNumberBox = QWidget()
        #self.lineNumberBox.sizeHint(QSize(self.lineNumAreaWidth(), 0))
        #self.connect(self, SIGNAL("blockCountChanged(int)"), self.updateLineNumAreaWidth)
        #self.connect(self, SIGNAL("updateRequest()"), self.updateLineNumArea)
        #self.connect(self, SIGNAL("cursorPositionChanged()"), self.highlightCurrentLine)
        #self.updateLineNumAreaWidth(0)
        #self.highlightCurrentLine()

    def alterFont(self, font):
        self.setFont(font)
        metrics = QFontMetrics(font)
        self.setTabStopWidth(Editor.tWidth * metrics.width('H'))


    def keyPressEvent(self, event):
        # replacing tabs with spaces
        # tab key is the event to modify the most
        """        
        if event.key() == Qt.Key_Home:
            pass
        elif event.key() == Qt.Key_End:
            pass
        elif event.key() == Qt.Key_PageUp:
            pass
        elif event.key() == Qt.Key_PageDown:
            pass
        """
        if event.key() == Qt.Key_Tab:
            spaces = " " * Editor.tWidth
            # prevent the tab from adding - discard keypress
            cursor = self.textCursor()
            cursor.insertText(spaces)
        else:
            QTextEdit.keyPressEvent(self, event)


    def setTabs(self):
        dialog = tabwidth.TabWidth()
        if dialog.exec_():
            initTabWidth = dialog.tabSpinBox.text().toInt()
            Editor.tWidth = initTabWidth    

    def alterFont(self, font):   
        pass




    def closeEvent(self, event):
        if (self.document().isModified() and QMessageBox.question(self, "Jotter - Unsaved Changes", "Save the modified text in {}?".format(self.filename), QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes):
            try:
                self.save()
            except EnvironmentError as e:
                QMessageBox.warning(self, "Jotter - Save Error", "Failed to save {}: {}".format(self.filename, e))


    def isModified(self):
        return self.document().isModified()


    def save(self):
        if self.filename.startswith("New"):
            filename = QFileDialog.getSaveFileName(self, "Jotter - Save", self.filename, "Text files (*.txt *.*)")
            if not filename:
                return
            self.filename = filename
        self.setWindowTitle(QFileInfo(self.filename).fileName())
        exception = None
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError(fh.errorString())
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            stream << self.toPlainText()
            self.document().setModified(False)
        except EnvironmentError as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception


    def load(self):
        exception = None
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError(fh.errorString())
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            self.setPlainText(stream.readAll())
            self.document().setModified(False)
        except EnvironmentError as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception

    """
    In the editor class
    Bracket matching code
    """

    def bracket_text(self):
        self.cursor = self.textCursor()
        self.document = cursor.document() 
        bracketLabel = QLabel() # stuck at bottom of Editor layout
        # the above should be a QTextDocument instance
        if self.document is not isinstance(QTextDocument, self.document):
            return
        while document.characterAt(self.cursor.position()) in "(":
            leftCount =  self.countChar("(")
            rightCount = self.countChar(")")
            bracketMsg = leftCount + "( and " + rightCount + " ) characters. "
            print(bracketMsg)
            bracketLabel.setText(bracketMsg)

    def countChar(self, char):
        if char not in "(){}[]":
            return False
        if char in ")]}":
            if char is ")":
                self.searchBack(")")
            elif char is "]":
                self.searchBack("]")
            elif char is "}":
                self.searchBack("}")
        elif char in "([{":
            if char is "(":
                self.searchForward(")")
            elif char is "[":
                self.searchForward("]")
            elif char is "{":
                self.searchForward("}")
        else:
            return False


    def searchBack(self, substr):
        if substr is ")":
            matchChar = "("
        elif substr is "]":
            matchChar = "["
        else:
            matchChar = "{"
        block = self.cursor.block()
        startpos = self.cursor.position()
        i = 0
        count = 0
        while i < startpos:
            charUnderCursor = self.document.characterAt(startpos)
            if charUnderCursor is matchChar:
                count += 1
                startpos -= 1
            return count 


    def searchForward(self, substr):
        if substr is "(":
            matchChar = ")"
        elif substr is "[":
            matchChar = "]"
        else: 
            matchChar = "}"
        blockStart = self.cursor.block()
        startpos = self.cursor.position()
        # if self.cursor.atEnd(): (end of file)
        i = 0
        count = 0
        while not self.cursor.atEnd():
            charUnderCursor = self.document.characterAt(startpos)
            if charUnderCursor is matchChar:
                count += 1
                startpos += 1
            return count 

            
    """
    Line Numbers:
    When combining with the editor it needs these (modified) bits in too:
     hbox = QHBoxLayout(self)
        hbox.setSpacing(0)
        hbox.setMargin(0)
        hbox.addWidget(self.number_bar)
        hbox.addWidget(self.edit)
 
        self.edit.blockCountChanged.connect(self.number_bar.adjustWidth)
        self.edit.updateRequest.connect(self.number_bar.updateContents)
    """

    NextId = 1 # for file numbers in new filenames


    """
    Start of line numbering part
    """

    def lineNumAreaWidth(self):
        digits = 1 
        maxnum = max(1, self.document.blockCount())     
        while maxnum >= 10:
            maxnum /= 10
            digits += digits
        space = 0
        space = 3 + self.fontMetrics().width(QLatin1Char('9')) * digits
        return space


    def updateLineNumAreaWidth(self, num=None):
        setViewportMargins(self.lineNumAreaWidth, 0, 0, 0)


    def updateLineNumArea(self):
        dy = 0
        if (dy):
            self.lineNumberBox.scroll(0, dy)
        else:
            self.lineNumberBox.update(0, rect.y(), self.lineNumberBox.width(), rect.height())
        if (rect.contains(viewport().rect())):
            updateLineNumAreaWidth(0)    


    def highlightCurrentLine(self):
        highlight = QTextEdit.ExtraSelection()
        highlight.format.setBackground(QColor(55,55,55))
        highlight.format.setProperty(QTextFormat.FullWidthSelection)
        highlight.cursor = self.textCursor()
        highlight.cursor.clearSelection()
        self.setExtraSelections([highlight])

    """
    am not sure what to do with this bit: 
    def resizeEvent(event):
     QPlainTextEdit::resizeEvent(e);
     QRect cr = contentsRect();
     lineNumberArea->setGeometry(QRect(cr.left(), cr.top(), lineNumberAreaWidth(), cr.height()));
    """
    """
    def paintEvent(self, event):
        font_metrics = self.fontMetrics()
        current_line = self.document().findBlock(self.textCursor().position()).blockNumber() + 1
        block = self.firstVisibleBlock()
        line_count = block.blockNumber()
        painter = QPainter()
        painter.fillRect(event.rect(), self.palette().base())
        while block.isValid():
            line_count += 1
            # checking the boxes offset, at the top, bottom
            block_top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
            if not block.isVisible() or block_top >= event.rect().bottom():
                break
                if line_count == current_line:
                    brush = painter.brush(QColor(0,0,200))
                    painter.setBackground(brush)
                    #font = painter.font()
                    #font.setColor(Qt.White)
                    #painter.setFont(font)
                else:
                    brush2 = painter.brush(QColor(34,34,34))
                    painter.setBrush(brush2)
                    #font = painter.font()
                    #font.setColor(Qt.White)
                    #font.setBold(False)
                    #painter.setFont(font)

                paint_rect = QRect(0, block_top, self.lineNumberBox.width(), font_metrics.height())
                painter.drawText(paint_rect, Qt.AlignRight, unicode(line_count))
                block = block.next()
            painter.end()

    """
