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
import os
import sys
import enchant
from enchant.tokenize import get_tokenizer, EmailFilter, URLFilter, HTMLChunker

"""
    Use the binary windows installer to add the enchant module for Windows.
    Ships with en_GB, en_US, de_DE, fr_FR on Win.
    Get dicts from Libreoffice, extract in c:/Python/Lib/site-pkgs/enchant/share/enchant/myspell

    On Mac dicts go in: /Library/Frameworks/Python/Version.../lib/py3/site-pkgs/enchant/.../myspell

    Linux dicts go in: /usr/lib/python3/enchant../myspell
     
"""

class Spellcheck(QDockWidget):

    index = 0

    def __init__(self, document, parent=None):
        super(Spellcheck, self).__init__(parent)

        self.createUI()
        if document is None:
            return
        else:
            self.doc = document.toPlainText()
        # copy the document text and strip out HTML, URL's and Email addresses
        tokens = get_tokenizer("en_US", chunkers=(HTMLChunker,), filters=[EmailFilter, URLFilter])
        self.editDoc = [] # tuples go into this list
        for word in tokens(self.doc):
            self.editDoc.append(word)
        self.wordsToCheck = dict((t[0], i) for i, t in enumerate(self.editDoc))
        # >>> Output self.wordsToCheck , unit Test with 10 cases
        self.wordlist = enchant.request_dict("en_GB")
        self.misspeltList = []
        for key in self.wordsToCheck.keys():
            self.checkWord(key)
        # >>> Plonk a test here
        
        self.highlightMisspelt(self.misspeltList[Spellcheck.index:])


    def setDictionary(self):        
        import dictLangDialog
        dialog = dictLangDialog.DictLangDialog()
        try:
            dialog.show()
            lang = dialog.selectedLang
            if lang == "United States" and enchant.dict_exists("en_US"):
                self.wordlist = enchant.request_dict("en_US")
            elif lang == "Chinese" and enchant.dict_exists("zh"):
                self.wordlist = enchant.request_dict("zh")
            elif lang == "Russian" and enchant.dict_exists("ru"):
                self.wordlist = enchant.request_dict("ru")
            elif lang == "German" and enchant.dict_exists("de_DE"):
                self.wordlist = enchant.request_dict("de_DE")
            elif lang == "French" and enchant.dict_exists("fr_FR"):
                self.wordlist = enchant.request_dict("fr_FR")
            elif lang == "Norwegian" and enchant.dict_exists("no"):
                self.wordlist = enchant.request_dict("no")
            elif lang == "Zulu" and enchant.dict_exists("zu"):
                self.wordlist = enchant.request_dict("zu")
            elif lang == "Arabic" and enchant.dict_exists("ar"):
                self.wordlist = enchant.request_dict("ar")
            elif lang == "Hindi" and enchant.dict_exists("hi"):
                self.wordlist = enchant.request_dict("hi")
            elif lang == "British" and enchant.dict_exists("en_GB"):
                self.wordlist = enchant.request_dict("en_GB")
        except:
            self.wordlist = enchant.request_dict("en_GB")


    def createUI(self):
        spellcheckDock = QDockWidget("Spell Check")
        spellcheckDock.setAllowedAreas(Qt.RightDockWidgetArea)
        centralBit = QWidget()
        spellcheckDock.setWidget(centralBit)       
        
        self.misspeltWordText = QLineEdit() 
        self.misspeltWordText.setReadOnly(True)
        setLangToolBtn = QToolButton()
        setLangToolBtn.setIcon(QIcon(":/images/win/dictionary_128x128.png"))
        setLangToolBtn.setToolTip("Change the language dictionary")
        addWordBtn = QPushButton("&Add")
        addWordBtn.setIcon(QIcon(":/images/win/add_sign.png"))
        addIgnoreGap = QLabel()
        ignoreWordBtn = QPushButton("&Ignore")
        ignoreWordBtn.setIcon(QIcon(":/images/win/delete_128x128.png"))
        # top layout
        topLayout = QGridLayout()
        topLayout.addWidget(self.misspeltWordText, 0, 0, 3, 1)
        topLayout.addWidget(setLangToolBtn, 0, 1)
        topLayout.addWidget(addWordBtn, 1, 0)
        topLayout.addWidget(addIgnoreGap, 1, 1, 2, 1)
        topLayout.addWidget(ignoreWordBtn, 1, 2)
        # list widget ... this has the focus
        self.suggestedWordListWidget = QListWidget()
        self.suggestedWordListWidget.setMinimumSize(100, 600)
        self.suggestedWordListWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.suggestedWordListWidget.setFocus()
        closeBtn = QPushButton("&Close")
        closeBackGap = QLabel()
        backBtn = QPushButton("&Back")
        backBtn.setIcon(QIcon(":/images/win/back_128x128.png"))
        nextBtn = QPushButton("&Next")
        nextBtn.setIcon(QIcon(":/images/win/goto_128x128.png"))
        # lining up buttons
        buttonBox = QGridLayout()
        buttonBox.addWidget(closeBtn, 0, 0)
        buttonBox.addWidget(closeBackGap, 0, 1)
        buttonBox.addWidget(backBtn, 0, 2)
        buttonBox.addWidget(nextBtn, 0, 3)
        # main layout
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.suggestedWordListWidget)
        mainLayout.addLayout(buttonBox)
        # the connections 
        self.connect(setLangToolBtn, SIGNAL("triggered()"), self.setDictionary)
        self.connect(addWordBtn, SIGNAL("triggered()"), self.addWord)
        self.connect(ignoreWordBtn, SIGNAL("triggered()"), self.skipWord)
        #self.connect(closeBtn, SIGNAL("triggered()"), SLOT(close()))
        self.connect(backBtn, SIGNAL("triggered()"), self.backAWord)
        self.connect(nextBtn, SIGNAL("triggered()"), self.nextAWord)


    def checkWord(self, word):
        """
        check whether the word is in the enchant dictionary
        """
        if self.wordlist.check(word):
            return 
        else:
            self.misspeltList = []
            self.misspeltList.append(word)


    def highlightMisspelt(self, word):
        """
        Selects the misspelt word, after changing the selection bg colour.
        Clears the selection first, and lastly changes the selection bg to the
        default colour.
        """
        doc = str()
        doc = self.doc
        startpos = self.doc.find(word)
        endpos = len(word) + startpos
        self.cursor = QTextCursor()
        self.cursor.clearSelection()
        self.cursor.selection.setStyle("{ font-weight: bold; background-color: #F0A1AA; }")
        self.cursor.setPosition(startpos)
        self.cursor.setPosition(endpos, KeepAnchor)
        self.misspeltWordText.setText(word)
        similarWords(word)
        
   
    def similarWords(self, word):
        if word is None:
            return
        suggestions = self.wordlist.suggest(word)
        del suggestions[10:]
        self.suggestedWordListWidget.addItems(suggestions)


    def updateWord(self):
        newWord = self.suggestedWordListWidget.currentItem()
        self.cursor.removeSelectedText()
        self.cursor.insertText(newWord)
        
    def skipWord(self):
        Spellcheck.index += 1
        nextAWord()
        
        
    def backAWord(self):
        Spellcheck.index = Spellcheck.index - 1
        highlightMisspelt(self.misspeltList[Spellcheck.index:])
        
        
    def nextAWord(self):
        Spellcheck.index = Spellcheck.index + 1
        highlightMisspelt(self.misspeltList[Spellcheck.index:])
        
        
    def addWord(self):
        pass
        

# Tests: >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5))
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    app = QApplication(sys.argv)
    form = Spellcheck("<strong>Was hat sich durch die Entlassung für ihn geändert?</strong><br /> <br />So seltsam das klingen mag, im Gefängnis war er mehr gemittet, mehr bei sich. Jetzt ist er unruhig, reist viel, will seine Freiheit nutzen. Politisch betätigen möchte er sich nicht, aber er will seine Stiftung „OPEN RUSSIA“ wieder aufbauen, die sich um Bildung in Russland kümmerte. Außerdem ko-finanziert er die Gründung einer neuen Nachrichtenagentur in Riga, um der Propaganda in Russland etwas entgegen zu halten.</p><p><strong>Es heißt, sie planen einen neuen Film über ihn. </strong><br /> <br />Ja, er trägt den Arbeitstitel „Chodorkowskis Freiheit“. Es soll darum gehen, wie er mit seiner neuen Freiheit umgeht. Er sagt selbst, dass er sich im Gefängnis freier gefühlt hat als draußen. Jetzt verspürt er wieder den Druck, den er von allen Seiten bekommt. Die einen sähen ihn gern in einer aktiven Rolle, die anderen wünschen sich, dass er sich nicht politisch betätigt. Außerdem kann Chodorkowski gar nicht so radikal agieren, wie das Einige vielleicht wollen, weil sonst andere Menschen Probleme bekommen.<br /> <br />")
    form.show()
    app.exec_()
    