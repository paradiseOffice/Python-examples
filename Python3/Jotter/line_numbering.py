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

