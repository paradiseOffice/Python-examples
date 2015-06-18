#!/usr/bin/env python3

# -*- coding: UTF8 -*-

import os
import platform
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import mimetypes 
import editor
import qrc_jotter
import helpsystem
import insert_char
import spellchecker
import new_syntaxhighlighter

__version__ = "0.3"

class MainWindow(QMainWindow):
    
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.docList = []        
        self.tabWidget = QTabWidget()
        self.dirty = False
        self.setCentralWidget(self.tabWidget)

        fileNewAction = self.createAction("&New", self.fileNew, QKeySequence.New, "win/filenew.png", "Create a new text file")
        fileOpenAction = self.createAction("&Open", self.openManyFiles, QKeySequence.Open, "win/fileopen.png", "Open an existing text file")
        fileSaveAction = self.createAction("&Save", self.fileSave, QKeySequence.Save, "win/filesave.png", "Save this text file")
        fileSaveAsAction = self.createAction("Save &As", self.fileSaveAs, "Ctrl+Shift+S", "win/save_as_128x128.png", tip="Save the text under a different name")
        fileSaveAllAction = self.createAction("Save &All", self.fileSaveAll, "Ctrl+L", "win/save_all.png", tip="Save all opened files")
        fileBackTabAction = self.createAction("&Back A Tab", self.prevTab, "Ctrl+Shift+B", "win/back_128x128.png", tip="go back a file tab")
        fileNextTabAction = self.createAction("Next &Tab", self.nextTab, "Ctrl+Shift+N", "win/goto_128x128.png", tip="go to the next file tab")
        fileCloseTabAction = self.createAction("&Close", self.fileCloseTab, QKeySequence.Close, "win/close_file_128x128.png", "Close the active file")
        fileQuitAction = self.createAction("&Quit", self.close, "Alt+F4", "Close the application")
        # Edit actions
        undoAction = self.createAction("&Undo", self.textUndo, QKeySequence.Undo, "win/editundo.png", "Undo any changes made to the document")
        redoAction = self.createAction("&Redo", self.textRedo, QKeySequence.Redo, "win/editredo.png", "Redo any changes made to the file")
        editCutAction = self.createAction("Cu&t", self.editCut, QKeySequence.Cut, "win/editcut.png", "Remove text and place on the clipboard")
        editCopyAction = self.createAction("&Copy", self.editCopy, QKeySequence.Copy, "win/editcopy.png", "Copy text to the clipboard")
        editPasteAction = self.createAction("&Paste", self.editPaste, QKeySequence.Paste, "win/editpaste.png", "Appends text from the clipboard after the cursor")
        # Option actions
        
        tabWidthAction = QAction(self)
        tabWidthAction.setText("&Tab Width")
        self.connect(tabWidthAction, SIGNAL("triggered()"), self.tabWidth)
        #self.createAction("&Tab Width", self.tabWidth, "win/tab_width.png", "Change the tab width")
        changeFontAction = QAction(self)
        changeFontAction.setText("Change &Font")
        self.connect(changeFontAction, SIGNAL("triggered()"), self.changeFont)
        self.createAction("Change &Font", self.changeFont, "win/set_font.png", "Alter the font size and face")
        insertDateAction = QAction(self)
        insertDateAction.setText("&Insert Date")
        self.connect(insertDateAction, SIGNAL("triggered()"), self.insertDate)
        insertCharAction = QAction(self)
        insertCharAction.setText("Insert &Symbol")
        self.connect(insertCharAction, SIGNAL("triggered()"), self.insertChar)
        spellcheckerAction = QAction(self)
        spellcheckerAction.setText("S&pell Check")
        self.connect(spellcheckerAction, SIGNAL("triggered()"), self.spellcheck)
        
        # Help actions
        helpViewerAction = self.createAction("&Help", self.helpViewer, QKeySequence.HelpContents, "win/info_128x128.png", "View help documentation")
        helpAboutAction = self.createAction("&About", self.aboutJotter, "win/logo32.png", "Information about Jotter")
        # Menus
        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(fileMenu, (fileNewAction, fileOpenAction, fileSaveAction, fileSaveAsAction, fileSaveAllAction, fileBackTabAction, fileNextTabAction, fileCloseTabAction, None, fileQuitAction))
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (undoAction, redoAction, None, editCutAction, editCopyAction, editPasteAction))
        optionsMenu = self.menuBar().addMenu("&Options")
        self.addActions(optionsMenu, (changeFontAction, insertDateAction, insertCharAction))
        helpMenu = self.menuBar().addMenu("&Help")
        self.addActions(helpMenu, (helpViewerAction, helpAboutAction))
        # Toolbars
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("commonBar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction, fileSaveAllAction, None, editCutAction, editCopyAction, editPasteAction))

        # settings
        settings = QSettings()
        self.restoreGeometry(settings.value("MainWindow/Geometry", QByteArray()))
        self.restoreState(settings.value("MainWindow/State", QByteArray()))
        status = self.statusBar()
        status.setSizeGripEnabled(True) # TODO this should be false
        status.showMessage("Insert mode", 5000)
        self.setWindowTitle("Jotter")
        QTimer.singleShot(0, self.loadFiles)
        if not self.docList:
            self.fileNew()


    def isDirty(self):
        for i in range(self.tabWidget.count()):
            textarea = self.tabWidget.currentWidget(i)
            if textarea.textChanged():
                dirtyFName = QFileInfo(textarea.filename).fileName()
                dirtyFName += " [*]"
                self.dirty = True 
                self.tabWidget.setTabText(self.tabWidget.currentWidget(i), dirtyFName)
                try:
                    self.highlighter.rehighlight()
                except:
                    pass


    def createAction(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/images/{}".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    # end of help functions
    def setTheme(self):
        darkCss = """  QTextEdit { background-color: rgb(34,34,34); color: white; }   """
        lightCss = """ QTextEdit { background-color: rgb(221,221,221); color: black; } """
        textarea = self.tabWidget.currentWidget()
        if textarea is None or not isinstance(textarea, QTextEdit):
            return
        else:
            self.tabWidget.setStyleSheet(darkCss)
            return new_syntaxhighlighter.theme("lightOnDark")


    
    def closeEvent(self, event):
        failures = []
        for i in range(self.tabWidget.count()):
            textarea = self.tabWidget.widget(i)
            if textarea.isModified():
                try:
                    textarea.save()
                except IOError as e:
                    failures.append(e)
        if (failures and QMessageBox.warning(self, "Jotter - Save Error", "Failed to save {}\nQuit anyway?".format("\n\t".join(failures)), QMessageBox.Yes|QMessageBox.No) == QMessageBox.No):
            event.ignore()
            return
        settings = QSettings()
        settings.setValue("MainWindow/Geometry", self.saveGeometry())
        settings.setValue("MainWindow/State", self.saveState())
        self.docList = []
        for i in range(self.tabWidget.count()):
            textarea = self.tabWidget.widget(i)
            if not textarea.filename.startswith("New"):
                self.docList.append(textarea.filename)
        settings.setValue("CurrentFiles", self.docList)
        while self.tabWidget.count():
            textarea = self.tabWidget.widget(0)
            textarea.close()
            self.tabWidget.removeTab(0)

    # I don't know where to put the buttons/actions for these yet...
    def prevTab(self):
        last = self.tabWidget.count()
        current = self.tabWidget.currentIndex()
        if last:
            last -= 1
            current = last if current == 0 else current - 1
            self.tabWidget.setCurrentIndex(current)

    def nextTab(self):
        last = self.tabWidget.count()
        current = self.tabWidget.currentIndex()
        if last:
            last -= 1
            current = 0 if current == last else current + 1
            self.tabWidget.setCurrentIndex(current)


    # Basic file IO for MainWindow
    def loadFiles(self):
        if len(sys.argv) > 1:
            count = 0
            for filename in sys.argv[1:]:
                if QFileInfo(filename).isFile():
                    self.loadFile(filename)
                    QApplication.processEvents()
                    count += 1
                    if count >= 30: # 30 files should be enough for anyone
                        break
        else:
            settings = QSettings()
            self.docList = settings.value("currentFiles") or []
            for filename in self.docList:
                if QFile.exists(filename):
                    self.loadFile(filename)
                    QApplication.processEvents()


    def fileNew(self):
        filename = ""
        textarea = editor.Editor(filename)
        self.tabWidget.addTab(textarea, textarea.windowTitle())
        self.tabWidget.setCurrentWidget(textarea)
        self.setTheme()


    def openManyFiles(self):
        fileList = QFileDialog.getOpenFileNames(self, "Jotter - Open Files")
        for filename in fileList:
            self.fileOpen(filename)


    def fileOpen(self, filename):
        #filename = QFileDialog.getOpenFileName(self, "Jotter - Open File")
        if filename:
            for i in range(self.tabWidget.count()):
                textarea = self.tabWidget.widget(i)
                if textarea.filename == filename:
                    self.tabWidget.setCurrentWidget(textarea)
                    break
            else:
                self.loadFile(filename)


    def loadFile(self, filename):
        textarea = editor.Editor(filename)
        
        try:
            #self.setTheme()
            textarea.load()
            self.setTheme()
            textarea.setFocus()
            mimetypes.init()
            fileMimetype = mimetypes.guess_type(filename, strict=True)
            print(fileMimetype)
            basename, fileEnd = os.path.splitext(filename)
            print(basename, fileEnd)
            # basename should be used in the tab...
            if fileMimetype in ("text/x-c", "text/x-c++src") or fileEnd in (".cpp", ".c", ".hpp", ".h"):
                self.highlighter = new_syntaxhighlighter.CppHighlighter(textarea.document())
            elif fileMimetype == "text/x-script.python" or fileEnd in (".pyc", ".py", ".pyw"):
                self.highlighter = new_syntaxhighlighter.PythonHighlighter(textarea.document())
            elif fileMimetype == "text/x-script.perl" or fileEnd == ".pl":
                self.highlighter = new_syntaxhighlighter.PerlHighlighter(textarea.document())
            elif fileMimetype == ("text/x-sh") or fileEnd == ".sh":
                self.highlighter = new_syntaxhighlighter.BashHighlighter(textarea.document())
            elif fileMimetype in ("text/html", "application/xml", "text/xml") or fileEnd in (".html", ".htm", ".xml"):
                self.highlighter = new_syntaxhighlighter.HtmlHighlighter(textarea.document())
            elif fileMimetype == "text/markdown" or fileEnd == ".md":
                self.highlighter = new_syntaxhighlighter.MarkdownHighlighter(textarea.document())
            elif fileEnd == ".rb":
                self.highlighter = new_syntaxhighlighter.RubyHighlighter(textarea.document())
            elif fileMimetype == "text/css" or fileEnd == ".css":
                self.highlighter = new_syntaxhighlighter.CssHighlighter(textarea.document())
            elif fileMimetype == "application/javascript" or fileEnd == ".js":
                self.highlighter = new_syntaxhighlighter.JavascriptHighlighter(textarea.document())
            elif fileEnd == ".sql":
                self.highlighter = new_syntaxhighlighter.SqlHighlighter(textarea.document())
            
        except EnvironmentError as e:
            QMessageBox.warning(self, "Jotter - File Loading Error", "Failed to load {}: {}".format(filename, e))
            textarea.close()
            del textarea
        else:
            self.tabWidget.addTab(textarea, textarea.windowTitle())
            self.tabWidget.setCurrentWidget(textarea)



    def fileSave(self):
        textarea = self.tabWidget.currentWidget()
        if textarea is None or not isinstance(textarea, QTextEdit):
            return True
        try:
            textarea.save()
            self.tabWidget.setTabText(self.tabWidget.currentIndex(), QFileInfo(textarea.filename).fileName())
            return True
        except EnvironmentError as e:
            QMessageBox.warning(self, "Jotter - Save Error", "Failed to save {}: {}".format(textarea.filename, e))
            return False


    def fileSaveAs(self):
        textarea = self.tabWidget.currentWidget()
        if textarea is None or not isinstance(textarea, QTextEdit):
            return True
        filename = QFileDialog.getSaveFileName(self, "Jotter - Save As", textarea.filename, "Text files (*.txt *.*)")
        if filename:
            textarea.filename = filename
            return self.fileSave()
        return True


    def fileSaveAll(self):
        errors = []
        for i in range(self.tabWidget.count()):
            textarea = self.tabWidget.widget(i)
            if textarea.isModified():
                try:
                    textarea.save()
                except EnvironmentError as e:
                    errors.append("{}: {}".format(textarea.filename, e))
        if errors:
            QMessageBox.warning(self, "Jotter - Save All Error", 
                       "Failed to save\n{}".format("\n".join(errors)))


    def fileCloseTab(self):
        textarea = self.tabWidget.currentWidget()
        if textarea is None or not isinstance(textarea, QTextEdit):
            return
        textarea.close()

    # ------------------ edit functions-----------------------------
    def textUndo(self):
        textarea = self.tabWidget.currentWidget()
        if textarea is None or not isinstance(textarea, QTextEdit):
            return
        if (textarea.isUndoRedoEnabled()):
            textarea.undo()
        
    def textRedo(self):
        textarea = self.tabWidget.currentWidget()
        if textarea is None or not isinstance(textarea, QTextEdit):
            return
        if (textarea.isUndoRedoEnabled()):
            textarea.redo()
            

    def editCut(self):
        textarea = self.tabWidget.currentWidget()
        if textarea is None or not isinstance(textarea, QTextEdit):
            return
        cursor = textarea.textCursor()
        text = cursor.selectedText()
        if text:
            cursor.removeSelectedText()
            clipboard = QApplication.clipboard()
            clipboard.setText(text)


    def editCopy(self):
        textarea = self.tabWidget.currentWidget()
        if textarea is None or not isinstance(textarea, QTextEdit):
            return
        cursor = textarea.textCursor()
        text = cursor.selectedText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
                

    def editPaste(self):
        textarea = self.tabWidget.currentWidget()
        if textarea is None or not isinstance(textarea, QTextEdit):
            return
        clipboard = QApplication.clipboard()
        textarea.insertPlainText(clipboard.text())


    def tabWidth(self):
        textarea = self.tabWidget.currentWidget()
        if textarea is None or not isinstance(textarea, QTextEdit):
            return
        textarea.setTabs()  


    def changeFont(self):
        textarea = self.tabWidget.currentWidget()
        if textarea is None or not isinstance(textarea, QTextEdit):
            return
        newfont = QFont()
        # Try wrapping the below in try and except.
        newfont = QFontDialog.getFont(QFont("Liberation Mono [Courier]", 10), self)
        settings = QSettings()
        settings.setValue("Font", newfont)
        edit = editor.Editor()
        editor.Editor.alterFont(edit, newfont)
        
        
    def insertDate(self):
        textarea = self.tabWidget.currentWidget()
        if textarea is None or not isinstance(textarea, QTextEdit):
            return
        today = QDate.currentDate()
        dateToInsert = today.toString("dd/MM/yyyy")
        if dateToInsert:
            cursor = textarea.textCursor()
            cursor.insertText(dateToInsert)
        
    
    def insertChar(self):
        textarea = self.tabWidget.currentWidget()
        if textarea is None or not isinstance(textarea, QTextEdit):
            return
        dialog = insert_char.InsertChar()
        if dialog.exec_() == QDialog.Accepted:
            charToInsert = dialog.getChar()
            cursor = textarea.textCursor()
            cursor.insertText(charToInsert)
        textarea.setFocus()
    
    
    def spellcheck(self):
        textarea = self.tabWidget.currentWidget()
        if textarea is None or not isinstance(textarea, QTextEdit):
            return
        docker = spellchecker.Spellcheck(textarea)
        addDockWidget(Qt.RightDockWidgetArea, docker)
        
        
    def helpViewer(self):
        form = helpsystem.HelpViewer("index.html", self)
        form.show()
    
        
    def aboutJotter(self):    
        QMessageBox.about(self, "About Jotter", 
        """<h2>Jotter</h2> version {} <p>Copyright &copy; 2014 Hazel Windle <br />
        Copyright &copy; 2008-10 Qtrac Ltd. Digia Plc, All rights reserved. </p>
        <p>A text editor for creating content in any language including programming languages. Licensed under the 
        GNU GPL version 2, please see the LICENSE file included with this program for the license text, or visit 
        <a href='http://www.fsf.org/'>the Free Software Foundation</a> for more information. </p>  
        <br /><p>Python {} - Qt {} - PyQt {} on {}</p>"""\
        .format(__version__, platform.python_version(), QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))
        
        
def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/images/win/logo32.png"))
    app.setOrganizationName("Paradise Office")
    app.setOrganizationDomain("linux-paradise.co.uk")
    app.setApplicationName("Jotter")
    win = MainWindow()
    # load one new file at start
    win.resize(900,800)
    win.show()
    app.exec_()

main()
