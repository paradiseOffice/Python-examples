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
import sys

def theme(themeName="lightOnDark"):
    # import theme - print theme.xvar
    theme = themeName
    return theme

# Colours - lightOnDark
DARKGREY = QColor(34,34,34) # background
LIGHTESTGREY = QColor(204,204,204) # comments
BRIGHTBLUE = QColor(2,162,255) # scripts
LIGHTCYAN = QColor(0,255,255) # beginningLines
OFFRED = QColor(229,71,13) # strings
LEAFGREEN = QColor(130,207,7) # Attributes
BEIGE = QColor(255,220,168) # character entities
ORANGE = QColor(247,159,6) # keywords
LIGHTPINK = QColor(255,192,255) # special chars 2
LIGHTERCYAN = QColor(192,255,255) # inner script keywords
LIGHTPURPLE = QColor(211,76,255) # special chars 3
# Colours - darkOnLight
OFFWHITE = QColor(221,221,221) # background
GREY = QColor(148,145,145) # comment
VERMILLION = QColor(253,93,0) # scripts
DARKMAROON = QColor(94,0,0) # inner script keywords
RED = QColor(255,0,0) # beginningLines
SKYBLUE = QColor(72,194,238) # strings
VIOLET = QColor(107,35,227) # attributes
DARKBLUE = QColor(2,53,130) # entities
MEDBLUE = QColor(8,96,249) # keywords
DARKESTGREEN = QColor(0,63,0) # special chars 2
BRIGHTGREEN = QColor(50,164,15) # special chars 3


class CppHighlighter(QSyntaxHighlighter):
    
    Rules = []
    Formats = {}
    
    def __init__(self, parent=None):
        super(CppHighlighter, self).__init__(parent)
        
        self.initializeFormats()
        
        CPPKEYWORDS = ("alignas", "alignof", "and", "and_eq", "asm", "auto", "bitand", "bitor", "bool", "break", "case", "catch", "char", "char16_t", "char32_t", "class", "compl", "const", "constexpr", "const_cast", "continue", "decltype", "default", "delete", "do", "double", "dynamic_cast", "else", "else", "enum", "explicit", "export", "extern", "false", "float", "for", "friend", "goto", "if", "inline", "int", "long", "mutable", "namespace", "new", "noexcept", "not", "not_eq", "nullptr", "operator", "or", "or_eq", "private", "protected", "public", "register", "reinterpret_cast", "return", "short", "signed", "sizeof", "static", "static_assert", "static_cast", "struct", "switch", "template", "this", "thread_local", "throw", "true", "try", "typedef", "typeid", "typename", "union", "unsigned", "using", "virtual", "void", "volatile", "wchar_t", "while", "xor", "xor_eq" )
        
        self.commentRegex = QRegExp(r"""(?://+)""")
        CppHighlighter.Rules.append((self.commentRegex, "comment"))
        self.commentStartRegex = QRegExp(r"""(:?\/\*)""")
        self.commentEndRegex = QRegExp(r"""(:?\*\/)""")
        CppHighlighter.Rules.append((QRegExp(
           "|".join([r"\b%s\b" % keyword for keyword in CPPKEYWORDS])), "keyword"))       
        self.stringRegex = QRegExp(r"""(?:'[^']*'|"[^"]*")""")
        CppHighlighter.Rules.append((self.stringRegex, "strings"))
        CppHighlighter.Rules.append((QRegExp(
               r"\b[+-]?[0-9]+[fFuUlL]?\b" 
               # matches -90, +4, 4000l 
               r"|\b[-+]?0[xX][0-9A-Fa-f]+[fFuUlL]?\b"
               # matches -0x33232F and other hexadecimal nums
               r"|\b[-+]?[0-9]+(?:\.[0-9]+)?(?:[eE][-+]?[0-9]+)?\b"),
               # matches decimals and numbers with exponents
               "number"))
        
        self.includeRegex = QRegExp(r"""(:?^[#include].|^#[a-zA-Z]+)""")
        CppHighlighter.Rules.append((self.includeRegex, "includeLines"))
        self.backslashRegex = QRegExp(r"""(:?\\.)""")
        CppHighlighter.Rules.append((self.backslashRegex, "backslashChars"))
        self.curliesRegex = QRegExp(r"""(:?\{+|\}+)""")
        CppHighlighter.Rules.append((self.curliesRegex, "curlyBraces"))
        self.parenthesesRegex = QRegExp(r"""(:?\(+|\)+|==.)""")
        CppHighlighter.Rules.append((self.parenthesesRegex, "parentheses"))
        
    @staticmethod
    def initializeFormats():
        baseFormat = QTextCharFormat()
        # if for theme changer
        for name, colour in (("normal", QColor(Qt.white)),
             ("keyword", ORANGE), 
             ("comment", GREY), ("strings", OFFRED),
             ("number", LIGHTCYAN), 
             ("includeLines", BEIGE), ("backslashChars", LIGHTESTGREY),
             ("curlyBraces", LIGHTPURPLE), ("parentheses", LEAFGREEN)):
            format = QTextCharFormat(baseFormat)
            format.setForeground(colour)
            if name in ("keyword", "decorator", "curlyBraces", "parentheses"):
                format.setFontWeight(QFont.Bold)
            if name == "comment":
                format.setFontItalic(True)
            CppHighlighter.Formats[name] = format   
            
    def highlightBlock(self, text):
        NORMAL, COMMENT = range(2)
        textLength = len(text)
        prevState = self.previousBlockState()
 
        self.setFormat(0, textLength, CppHighlighter.Formats["normal"])
        # running through the reg. expressions
        for regex, format in CppHighlighter.Rules:
            i = regex.indexIn(text)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(i, length, CppHighlighter.Formats[format])
                i = regex.indexIn(text, i + length)
        self.setCurrentBlockState(NORMAL)
        if self.stringRegex.indexIn(text) != -1:
            return
        
        startIndex = 0
        endIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartRegex.indexIn(text)
        while startIndex >= 0:
            endIndex = self.commentEndRegex.indexIn(text, startIndex)
            commentLength = 0
            if endIndex == -1:
                self.setCurrentBlockState(COMMENT)
                commentLength = len(text) - startIndex;
            else:
                commentLength = endIndex - startIndex + self.commentEndRegex.matchedLength()
            self.setFormat(startIndex, commentLength, CppHighlighter.Formats["comment"])
            startIndex = self.commentStartRegex.indexIn(text, startIndex + commentLength)

    def rehighlight(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        QSyntaxHighlighter.rehighlight(self)
        QApplication.restoreOverrideCursor()
        
           
            
class PythonHighlighter(QSyntaxHighlighter):
    Rules = []
    Formats = {}

    def __init__(self, parent=None):
        """
        Put any tests in here, preceded by '>>>'
        """
        super(PythonHighlighter, self).__init__(parent)

        self.initializeFormats()

        KEYWORDS = ["and", "as", "assert", "break", "class", "continue", 
              "def", "del", "elif", "else", "except", "exec", "finally", "for",
              "from", "global", "if", "import", "in", "is", "lambda", "not", "or",
              "pass", "print", "raise", "return", "try", "while", "with", "yield" ]
        BUILTINS = ["abs", "all", "any", "basestring", "bool", "callable", "chr", 
                  "classmethod", "cmp", "compile", "complex", "delattr", "dict", "dir",
                  "divmod", "enumerate", "eval", "execfile", "exit", "file", "filter", 
                  "float", "frozenset", "getattr", "globals", "hasattr", "hex", "id", "int",
                  "isinstance", "issubclass", "iter", "len", "list", "locals", "map", "max",
                  "min", "object", "oct", "open", "ord", "pow", "property", "range", "reduce",
                  "repr", "reversed", "round", "set", "setattr", "slice", "sorted",
                  "staticmethod", "str", "sum", "super", "tuple", "type", "vars", "zip"]
        CONSTANTS = ["False", "True", "None", "NotImplemented", "Ellipsis"]

        PythonHighlighter.Rules.append((QRegExp(
           "|".join([r"\b%s\b" % keyword for keyword in KEYWORDS])), "keyword"))
        PythonHighlighter.Rules.append((QRegExp(
           "|".join([r"\b%s\b" % builtin for builtin in BUILTINS])), "builtin"))
        PythonHighlighter.Rules.append((QRegExp(
           "|".join([r"\b%s\b" % constant for constant in CONSTANTS])), "constants"))
        PythonHighlighter.Rules.append((QRegExp(
               r"\b[+-]?[0-9]+[lL]?\b" 
               # matches -90, +4, 4000l 
               r"|\b[-+]?0[xX][0-9A-Fa-f]+[lL]?\b"
               # matches -0x33232F and other hexadecimal nums
               r"|\b[-+]?[0-9]+(?:\.[0-9]+)?(?:[eE][-+]?[0-9]+)?\b"),
               # matches decimals and numbers with exponents
               "number"))
        PythonHighlighter.Rules.append((QRegExp(
               r"\bPyQt4\b|\bQt?[A-Z][a-z]\w+\b"), "pyqt"))
        PythonHighlighter.Rules.append((QRegExp(r"\b@\w+\b"), "decorator"))
        PythonHighlighter.Rules.append((QRegExp(r"#.*"), "comment"))
        stringRe = QRegExp(r"""(?:'[^']*'|"[^"]*")""")
        # starts with ' no quote in that string, ends with ' or (|) the same with " quotes
        stringRe.setMinimal(True)
        PythonHighlighter.Rules.append((stringRe, "string"))
        self.stringRe = QRegExp(r"""(:?"["]".*"["]"|'''.*''')""")
        self.stringRe.setMinimal(True)
        PythonHighlighter.Rules.append((self.stringRe, "string"))
        PythonHighlighter.Rules.append((QRegExp(r"""(?:^[import|from]+)"""), "includeLines"))
        PythonHighlighter.Rules.append((QRegExp(r"""(:?\\.)"""), "backslashChars"))
        PythonHighlighter.Rules.append((QRegExp(r"""(:?\[\]+)"""), "curlyBraces"))
        PythonHighlighter.Rules.append((QRegExp(r"""(:?\(+|\)+)"""), "parentheses"))
        
        self.tripleSingleRe = QRegExp(r"""'''(?!")""")
        self.tripleDoubleRe = QRegExp(r'''"""(?!')''')

    @staticmethod
    def initializeFormats():
        baseFormat = QTextCharFormat()
        # if for theme changer
        for name, colour in (("normal", QColor(Qt.white)),
             ("keyword", ORANGE), ("builtin", LIGHTERCYAN),
             ("constants", LEAFGREEN), ("decorator", BRIGHTBLUE),
             ("comment", GREY), ("string", OFFRED),
             ("number", LIGHTCYAN), ("error", OFFRED), ("pyqt", LIGHTPURPLE),
             ("includeLines", LIGHTCYAN), ("backslashChars", LIGHTESTGREY),
             ("curlyBraces", BEIGE), ("parentheses", LEAFGREEN)):
            format = QTextCharFormat(baseFormat)
            format.setForeground(colour)
            if name in ("keyword", "decorator", "curlyBraces", "parentheses"):
                format.setFontWeight(QFont.Bold)
            if name == "comment":
                format.setFontItalic(True)
            PythonHighlighter.Formats[name] = format


    def highlightBlock(self, text):
        NORMAL, TRIPLESINGLE, TRIPLEDOUBLE, ERROR = range(4)

        textLength = len(text)
        prevState = self.previousBlockState()
 
        self.setFormat(0, textLength, PythonHighlighter.Formats["normal"])
        if text.startswith("Traceback") or text.startswith("Error: "):
            self.setCurrentBlockState(ERROR)
            self.setFormat(0, textLength, PythonHighlighter.Formats["error"])
            return
        if (prevState == ERROR and not (text.startswith(sys.ps1) or text.startswith("#"))):
            self.setCurrentBlockState(ERROR)
            self.setFormat(0, textLength, PythonHighlighter.Formats["error"])
            return
        # running through the reg. expressions
        for regex, format in PythonHighlighter.Rules:
            i = regex.indexIn(text)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(i, length, PythonHighlighter.Formats[format])
                i = regex.indexIn(text, i + length)
        self.setCurrentBlockState(NORMAL)
        if self.stringRe.indexIn(text) != -1:
            return
        
        for i, state in ((self.tripleSingleRe.indexIn(text), TRIPLESINGLE),
                        (self.tripleDoubleRe.indexIn(text), TRIPLEDOUBLE)):
            if self.previousBlockState() == state:
                if i == -1:
                    i = len(text)
                    self.setCurrentBlockState(state)
                self.setFormat(0, i + 3, PythonHighlighter.Formats["comment"])
            elif i > -1:
                self.setCurrentBlockState(state)
                self.setFormat(i, len(text), PythonHighlighter.Formats["comment"])


    def rehighlight(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        QSyntaxHighlighter.rehighlight(self)
        QApplication.restoreOverrideCursor()
        
        """
        elif theme == "darkOnLight":
            self.comment.setForeground(GREY)
            self.includeLines.setForeground(RED)
            self.strings.setForeground(SKYBLUE)
            self.backslashChars.setForeground(DARKMAROON)
            self.keywords.setForeground(MEDBLUE)
            self.curlyBraces.setForeground(DARKBLUE)
            self.parentheses.setForeground(BRIGHTGREEN)
            self.parentheses.setFontWeight(QFont.Bold)
            self.specChars3.setForeground(VERMILLION)
        """ 
                       
class PerlHighlighter(QSyntaxHighlighter):
    
    Rules = []
    Formats = {}
    def __init__(self, parent=None):
        super(PerlHighlighter, self).__init__(parent)
        
        self.initializeFormats()
        PERLKEYWORDS = ("abs", "accept", "alarm", "atan2", "AUTOLOAD", "BEGIN", "bind", "binmode", "bless", "break", "caller", "chdir", "CHECK", "chmod", "chomp", "chop", "chown", "chr", "END", "endgrent", "endhostent", "endnetent", "endprotoent", "endpwent", "endservent", "eof", "eval", "exec", "exists", "exit", "fcntl", "fileno", "flock", "format", "formline", "getc", "getgrent", "getgrgid", "getgrnam", "gethostbyaddr", "gethostbyname", "gethostent", "getlogin", "getnetbyaddr", "getnetbyname", "getnetent", "getpeername", "getpgrp", "getppid", "getpriority", "getprotobyname", "getprotobynumber", "getprotoent", "getpwent", "getpwnam", "getpwuid", "getservbyname", "getservbyport", "getservent", "getsockname", "getsockopt", "glob", "length", "link", "listen", "local", "localtime", "log", "lstat", "map", "mkdir", "msgctl", "msgget", "msgrcv", "msgsnd", "my", "next", "not", "oct", "open", "opendir", "ord", "our", "pack", "pipe", "pop", "pos", "print", "printf", "prototype", "push", "quotemeta", "rand", "read", "readdir", "readline",  "shutdown", "sin", "sleep", "socket", "socketpair", "sort", "splice", "split", "sprintf", "sqrt", "srand", "stat", "state", "study", "substr", "symlink", "syscall", "sysopen", "sysread", "sysseek", "system", "syswrite", "tell", "telldir", "tie", "tied", "time", "times", "truncate", "uc", "ucfirst", "umask", "undef", "UNITCHECK", "delete", "DESTROY", "die", "dump", "each", "keys", "kill", "last", "lc", "lcfirst", "semop", "send", "setgrent", "sethostent", "setnetent", "waitpid", "wantarray", "warn", "write", "cmp", "continue", "do", "else", "elsif", "exp", "for", "foreach",  "if", "lock", "package", "sub", "tr", "unless", "until", "while", "xor" )
        PerlHighlighter.Rules.append((QRegExp(
           "|".join([r"\b%s\b" % keyword for keyword in PERLKEYWORDS])), "keyword"))
        self.stringRegex = QRegExp(r"""(?:'[^']*'|"[^"]*")""")
        PerlHighlighter.Rules.append((self.stringRegex, "strings"))
        self.commentRegex = QRegExp(r"""(?:#.*)""")
        self.commentStartRegex = QRegExp(r"""(?:=begin comment)""")
        self.commentEndRegex = QRegExp(r"""(?:=end)""")
        PerlHighlighter.Rules.append((self.commentRegex, "comment"))
        PerlHighlighter.Rules.append((QRegExp(
               r"\b[+-]?[0-9]+[lL]?\b" 
               # matches -90, +4, 4000l 
               r"|\b[-+]?0[xX][0-9A-Fa-f]+[lL]?\b"
               # matches -0x33232F and other hexadecimal nums
               r"|\b[-+]?[0-9]+(?:\.[0-9]+)?(?:[eE][-+]?[0-9]+)?\b"),
               # matches decimals and numbers with exponents
               "number"))
        
        self.variableRegex = QRegExp(r"""(?:\$\w+\b)""")
        PerlHighlighter.Rules.append((self.variableRegex, "variables"))
        self.backslashRegex = QRegExp(r"""(:?\\.)""")
        PerlHighlighter.Rules.append((self.backslashRegex, "backslashChars"))
        self.curliesRegex = QRegExp(r"""(?:\{+|\}+)""")
        PerlHighlighter.Rules.append((self.curliesRegex, "curlyBraces"))
        self.parenthesesRegex = QRegExp(r"""(?:\(+|\)+)""")
        PerlHighlighter.Rules.append((self.parenthesesRegex, "parentheses"))
        self.colonsRegex = QRegExp(r"""(:?;+)""")
        PerlHighlighter.Rules.append((self.colonsRegex, "colons"))
        
    @staticmethod
    def initializeFormats():
        baseFormat = QTextCharFormat()
        # if for theme changer
        for name, colour in (("normal", QColor(Qt.white)), ("variables", LEAFGREEN),
             ("keyword", ORANGE), ("comment", GREY), ("strings", OFFRED),
             ("number", LIGHTCYAN), ("backslashChars", LIGHTESTGREY),
             ("curlyBraces", BEIGE), ("parentheses", LEAFGREEN), ("colons", LIGHTPURPLE)):
            format = QTextCharFormat(baseFormat)
            format.setForeground(colour)
            if name in ("keyword", "curlyBraces", "parentheses"):
                format.setFontWeight(QFont.Bold)
            if name == "comment":
                format.setFontItalic(True)
            PerlHighlighter.Formats[name] = format
    
    def highlightBlock(self, text):
        NORMAL, COMMENT = range(2)

        textLength = len(text)
        prevState = self.previousBlockState()
 
        self.setFormat(0, textLength, PerlHighlighter.Formats["normal"])
        # running through the reg. expressions
        for regex, format in PerlHighlighter.Rules:
            i = regex.indexIn(text)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(i, length, PerlHighlighter.Formats[format])
                i = regex.indexIn(text, i + length)
        self.setCurrentBlockState(NORMAL)
        if self.stringRegex.indexIn(text) != -1:
            return
        
        startIndex = 0
        endIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartRegex.indexIn(text)
        while startIndex >= 0:
            endIndex = self.commentEndRegex.indexIn(text, startIndex)
            commentLength = 0
            if endIndex == -1:
                self.setCurrentBlockState(COMMENT)
                commentLength = len(text) - startIndex;
            else:
                commentLength = endIndex - startIndex + self.commentEndRegex.matchedLength()
            self.setFormat(startIndex, commentLength, PerlHighlighter.Formats["comment"])
            startIndex = self.commentStartRegex.indexIn(text, startIndex + commentLength)

    def rehighlight(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        QSyntaxHighlighter.rehighlight(self)
        QApplication.restoreOverrideCursor()
               
            
            
class BashHighlighter(QSyntaxHighlighter):
    
    Rules = []
    Formats = {}
    
    def __init__(self, parent=None):
        super(BashHighlighter, self).__init__(parent)
        
        self.initializeFormats()
        BASHKEYWORDS = ("if", "else", "elif", "case", "if", "then", "fi", "esac", "while", "do", "done", "until", "for", "chmod", "chown", "alias", "break", "cat", "EXPORT", "ls", "mkdir", "cd", "less", "more", "rm", "rmdir", "touch", "test", "file", "grep")
        BASHOPERATORS = ("-gt", "-lt", "-ge", "-le", "-eq", "-ne", "-z", "-a", "-o", "-f", "-s", "-r", "-w", "-x", "-d" )
        BashHighlighter.Rules.append((QRegExp(
           "|".join([r"\b%s\b" % keyword for keyword in BASHKEYWORDS])), "keyword"))
        BashHighlighter.Rules.append((QRegExp("|".join([r"\b%s\b" % operator for operator in BASHOPERATORS])), "operators"))
        self.stringRegex = QRegExp(r"""(?:=[a-zA-Z]*|'[^']*'|`[^`]*`|"[^"]*")""")
        BashHighlighter.Rules.append((self.stringRegex, "strings"))
        BashHighlighter.Rules.append((QRegExp(
               r"\b[+-]?[0-9]+[lL]?\b" 
               # matches -90, +4, 4000l 
               r"|\b[-+]?0[xX][0-9A-Fa-f]+[lL]?\b"
               # matches -0x33232F and other hexadecimal nums
               r"|\b[-+]?[0-9]+(?:\.[0-9]+)?(?:[eE][-+]?[0-9]+)?\b"),
               # matches decimals and numbers with exponents
               "number"))
        self.commentRegex = QRegExp(r"""(?:#.*)""")
        BashHighlighter.Rules.append((self.commentRegex, "comment"))
        self.exprRegex = QRegExp(r"""(?:[$\(\(*\)\))""")
        BashHighlighter.Rules.append((self.exprRegex, "expr"))
        self.backslashRegex = QRegExp(r"""(?:\\.)""")
        BashHighlighter.Rules.append((self.backslashRegex, "backslashChars"))
        self.parenthesesRegex = QRegExp(r"""(:?\(+|\)+)""")
        BashHighlighter.Rules.append((self.parenthesesRegex, "parentheses"))
        
    @staticmethod
    def initializeFormats():
        baseFormat = QTextCharFormat()
        # if for theme changer
        for name, colour in (("normal", QColor(Qt.white)),
             ("keyword", ORANGE), ("comment", GREY), 
             ("strings", OFFRED), ("operators", LIGHTPINK),
             ("number", BEIGE), ("backslashChars", LIGHTESTGREY),
             ("parentheses", LEAFGREEN), ("expr", LIGHTPURPLE)):
            format = QTextCharFormat(baseFormat)
            format.setForeground(colour)
            if name in ("keyword", "operators", "parentheses"):
                format.setFontWeight(QFont.Bold)
            if name == "comment":
                format.setFontItalic(True)
            BashHighlighter.Formats[name] = format
    
    def highlightBlock(self, text):
        NORMAL, COMMENT = range(2)

        textLength = len(text)
        prevState = self.previousBlockState()
 
        self.setFormat(0, textLength, BashHighlighter.Formats["normal"])
        # running through the reg. expressions
        for regex, format in BashHighlighter.Rules:
            i = regex.indexIn(text)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(i, length, BashHighlighter.Formats[format])
                i = regex.indexIn(text, i + length)
        self.setCurrentBlockState(NORMAL)
        if self.stringRegex.indexIn(text) != -1:
            return

    def rehighlight(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        QSyntaxHighlighter.rehighlight(self)
        QApplication.restoreOverrideCursor()

            
class HtmlHighlighter(QSyntaxHighlighter):
    
    Rules = []
    Formats = {}

    def __init__(self, parent=None):
        super(HtmlHighlighter, self).__init__(parent)
        
        self.initializeFormats()
        # the keywords below are HTML elements that are deprecated.
        DEPRECATEDKEYWORDS = ("<applet>", "<basefont />", "<blackface>", "<blockquote>", "<center>", "<dir>", "<embed>", "<font>", "<i>", "<isindex />", "<layer>", "<menu>", "<noembed>", "<s>", "<shadow>", "<strike>", "<u>", "alink=", "align=", "background=", "border=", "color=", "compact=", "face=", "height=", "language=", "link=", "noshade=", "nowrap=", "size=", "start=", "text=", "type=", "vlink=", "width=", "height=" )
        HtmlHighlighter.Rules.append((QRegExp(
           "|".join([r"\b%s\b" % keyword for keyword in DEPRECATEDKEYWORDS])), "keyword"))         
        self.stringRegex = QRegExp(r"""(?:='[^']*'|="[^"]*")""")
        HtmlHighlighter.Rules.append((self.stringRegex, "strings"))
        self.commentStartRegex = QRegExp(r"""(?:<!--)""")
        self.commentEndRegex = QRegExp(r"""(?:-->)""")
        self.doctypeRegex = QRegExp(r"""(:?^[<!DOCTYPE]+|^[<?xml]+|^[<!doctype]+)""")
        HtmlHighlighter.Rules.append((self.doctypeRegex, "doctype"))
        self.scriptRegex = QRegExp(r"""(:?<script|</script>)""")
        HtmlHighlighter.Rules.append((self.scriptRegex, "script"))
        self.attributeRegex = QRegExp(r"""(:?\w+=)""")
        HtmlHighlighter.Rules.append((self.attributeRegex, "attributes"))
        self.entitiesRegex = QRegExp(r"""(:?&\w+;)""")
        HtmlHighlighter.Rules.append((self.entitiesRegex, "entities"))
        self.jsCharsRegex = QRegExp(r"""(:?\(\{+|\}\)\;+|\(\);+|(CDATA).)""")
        HtmlHighlighter.Rules.append((self.jsCharsRegex, "jsChars"))
        self.styles = QRegExp(r"""(?:<style*>*</style>)""")
        HtmlHighlighter.Rules.append((self.styles, "stylesFormat"))
        self.elementRegex = QRegExp(r"""(?:<\w+|</[a-zA-Z]+>|[/>].|>)""")
        HtmlHighlighter.Rules.append((self.elementRegex, "elements"))
        
    @staticmethod
    def initializeFormats():
        baseFormat = QTextCharFormat()
        # if for theme changer
        for name, colour in (("normal", QColor(Qt.white)),
             ("keyword", OFFRED), ("doctype", GREY), 
             ("comment", GREY), ("script", BRIGHTBLUE), ("stylesFormat", LIGHTERCYAN),
             ("strings", OFFRED), ("attributes", LEAFGREEN),
             ("number", BEIGE), ("entities", LIGHTCYAN),
             ("elements", ORANGE), ("jsChars", LIGHTPURPLE)):
            format = QTextCharFormat(baseFormat)
            format.setForeground(colour)
            if name in ("keyword", "jsChars", "elements"):
                format.setFontWeight(QFont.Bold)
            if name == "comment":
                format.setFontItalic(True)
            HtmlHighlighter.Formats[name] = format
    
    def highlightBlock(self, text):
        NORMAL, COMMENT, SCRIPT = range(3)

        textLength = len(text)
        prevState = self.previousBlockState()
 
        self.setFormat(0, textLength, HtmlHighlighter.Formats["normal"])
        # running through the reg. expressions
        for regex, format in HtmlHighlighter.Rules:
            i = regex.indexIn(text)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(i, length, HtmlHighlighter.Formats[format])
                i = regex.indexIn(text, i + length)
        self.setCurrentBlockState(NORMAL)
        if self.stringRegex.indexIn(text) != -1:
            return
        
        startIndex = 0
        endIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartRegex.indexIn(text)
        while startIndex >= 0:
            endIndex = self.commentEndRegex.indexIn(text, startIndex)
            commentLength = 0
            if endIndex == -1:
                self.setCurrentBlockState(COMMENT)
                commentLength = len(text) - startIndex;
            else:
                commentLength = endIndex - startIndex + self.commentEndRegex.matchedLength()
            self.setFormat(startIndex, commentLength, HtmlHighlighter.Formats["comment"])
            startIndex = self.commentStartRegex.indexIn(text, startIndex + commentLength)

    def rehighlight(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        QSyntaxHighlighter.rehighlight(self)
        QApplication.restoreOverrideCursor()
            
            
            
class MarkdownHighlighter(QSyntaxHighlighter):
    
    Rules = []
    Formats = {}
    def __init__(self, parent=None):
        super(MarkdownHighlighter, self).__init__(parent)
        
        self.initializeFormats()
        self.elementRegex = QRegExp(r"""(?:<\w+|</[a-zA-Z]+>|[/>].|>)""")        
        MarkdownHighlighter.Rules.append((self.elementRegex, "elements"))
        self.commentStartRegex = QRegExp(r"""(?:<!--)""")
        self.commentEndRegex = QRegExp(r"""(?:-->)""")
        self.headingRegex = QRegExp(r"""(?:^[#]..+|^=..+|^-..+)""")
        MarkdownHighlighter.Rules.append((self.headingRegex, "headings"))
        self.blockquoteRegex = QRegExp(r"""(?:^>)""")
        MarkdownHighlighter.Rules.append((self.blockquoteRegex, "quote"))
        self.emphasisRegex = QRegExp(r"""(?:\*|\*\*|_|__)""")
        MarkdownHighlighter.Rules.append((self.emphasisRegex, "emphasis"))
        self.listsRegex = QRegExp(r"""(?:^\*[a-zA-Z -_]+$|^\+|^-|^[0-9]+\.)""")
        MarkdownHighlighter.Rules.append((self.listsRegex, "lists"))
        self.linkRegex = QRegExp(r"""(?:!?\[*\]\(*\))""")
        # linkRegex does pics .
        MarkdownHighlighter.Rules.append((self.linkRegex, "links"))
        self.backticksRegex = QRegExp(r"""(?:`)""")
        MarkdownHighlighter.Rules.append((self.backticksRegex, "codeFormat"))
        
    @staticmethod
    def initializeFormats():
        baseFormat = QTextCharFormat()
        # if for theme changer
        for name, colour in (("normal", QColor(Qt.white)),
             ("elements", ORANGE), ("comment", GREY), 
             ("headings", OFFRED), ("quote", LIGHTPINK),
             ("emphasis", LIGHTCYAN), ("lists", LIGHTESTGREY),
             ("codeFormat", LEAFGREEN), ("links", LIGHTPURPLE)):
            format = QTextCharFormat(baseFormat)
            format.setForeground(colour)
            if name in ("emphasis", "headings", "elements"):
                format.setFontWeight(QFont.Bold)
            if name == "comment":
                format.setFontItalic(True)
            MarkdownHighlighter.Formats[name] = format
    
    def highlightBlock(self, text):
        NORMAL, COMMENT = range(2)

        textLength = len(text)
        prevState = self.previousBlockState()
 
        self.setFormat(0, textLength, MarkdownHighlighter.Formats["normal"])
        # running through the reg. expressions
        for regex, format in MarkdownHighlighter.Rules:
            i = regex.indexIn(text)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(i, length, MarkdownHighlighter.Formats[format])
                i = regex.indexIn(text, i + length)
        self.setCurrentBlockState(NORMAL)
        if self.elementRegex.indexIn(text) != -1:
            return
        
        startIndex = 0
        endIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartRegex.indexIn(text)
        while startIndex >= 0:
            endIndex = self.commentEndRegex.indexIn(text, startIndex)
            commentLength = 0
            if endIndex == -1:
                self.setCurrentBlockState(COMMENT)
                commentLength = len(text) - startIndex;
            else:
                commentLength = endIndex - startIndex + self.commentEndRegex.matchedLength()
            self.setFormat(startIndex, commentLength, MarkdownHighlighter.Formats["comment"])
            startIndex = self.commentStartRegex.indexIn(text, startIndex + commentLength)

    def rehighlight(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        QSyntaxHighlighter.rehighlight(self)
        QApplication.restoreOverrideCursor()
        
            
            
class RubyHighlighter(QSyntaxHighlighter):
    
    Rules = []
    Formats = {}
    def __init__(self, parent=None):
        super(RubyHighlighter, self).__init__(parent)
        
        self.initializeFormats()
        RUBYKEYWORDS = ("BEGIN", "END", "__ENCODING__", "__END__", "__FILE__", "__LINE__", "alias", "and", "begin", "break", "case", "class", "def", "defined?", "do", "else", "elsif", "end", "ensure", "false", "for", "if", "in", "module", "next", "nil", "not", "or", "redo", "rescue", "retry", "return", "self", "super", "then", "true", "undef", "unless", "until", "when", "while", "yield")
        RubyHighlighter.Rules.append((QRegExp(
           "|".join([r"\b%s\b" % keyword for keyword in RUBYKEYWORDS])), "keyword"))        
        self.stringRegex = QRegExp(r"""(?:'[^']*'|"[^"]*")""")
        RubyHighlighter.Rules.append((self.stringRegex, "strings"))
        self.commentRegex = QRegExp(r"""(?:#.\w+)""")
        RubyHighlighter.Rules.append((self.commentRegex, "comment"))
        self.commentStartRegex = QRegExp(r"""(:?=begin)""")
        self.commentEndRegex = QRegExp(r"""(:?=end)""")
        self.varRegex = QRegExp(r"""(:?\$\w+|@\w*|^_\w+|@@\w+)""")
        RubyHighlighter.Rules.append((QRegExp(
               r"\b[+-]?[0-9]+[lL]?\b" 
               # matches -90, +4, 4000l 
               r"|\b[-+]?0[xX][0-9A-Fa-f]+[lL]?\b"
               # matches -0x33232F and other hexadecimal nums
               r"|\b[-+]?[0-9]+(?:\.[0-9]+)?(?:[eE][-+]?[0-9]+)?\b"),
               # matches decimals and numbers with exponents
               "number"))
        RubyHighlighter.Rules.append((self.varRegex, "variables"))
        self.backslashRegex = QRegExp(r"""(:?\\.)""")
        RubyHighlighter.Rules.append((self.backslashRegex, "backslashChars"))
        self.curliesRegex = QRegExp(r"""(:?\[|\]|\{|\})""")
        RubyHighlighter.Rules.append((self.curliesRegex, "curlyBraces"))
        self.parenthesesRegex = QRegExp(r"""(:?\(+|\)+)""")
        RubyHighlighter.Rules.append((self.parenthesesRegex, "parentheses"))
        
        
    @staticmethod
    def initializeFormats():
        baseFormat = QTextCharFormat()
        # if for theme changer
        for name, colour in (("normal", QColor(Qt.white)),
             ("keyword", ORANGE), ("comment", GREY), 
             ("strings", OFFRED), ("variables", BEIGE),
             ("number", LIGHTCYAN), ("backslashChars", LIGHTESTGREY),
             ("parentheses", LEAFGREEN), ("curlyBraces", LIGHTPURPLE)):
            format = QTextCharFormat(baseFormat)
            format.setForeground(colour)
            if name in ("keyword", "curlyBraces", "parentheses"):
                format.setFontWeight(QFont.Bold)
            if name == "comment":
                format.setFontItalic(True)
            RubyHighlighter.Formats[name] = format
    
    def highlightBlock(self, text):
        NORMAL, COMMENT = range(2)

        textLength = len(text)
        prevState = self.previousBlockState()
 
        self.setFormat(0, textLength, RubyHighlighter.Formats["normal"])
        # running through the reg. expressions
        for regex, format in RubyHighlighter.Rules:
            i = regex.indexIn(text)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(i, length, RubyHighlighter.Formats[format])
                i = regex.indexIn(text, i + length)
        self.setCurrentBlockState(NORMAL)
        if self.stringRegex.indexIn(text) != -1:
            return
        
        startIndex = 0
        endIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartRegex.indexIn(text)
        while startIndex >= 0:
            endIndex = self.commentEndRegex.indexIn(text, startIndex)
            commentLength = 0
            if endIndex == -1:
                self.setCurrentBlockState(COMMENT)
                commentLength = len(text) - startIndex;
            else:
                commentLength = endIndex - startIndex + self.commentEndRegex.matchedLength()
            self.setFormat(startIndex, commentLength, RubyHighlighter.Formats["comment"])
            startIndex = self.commentStartRegex.indexIn(text, startIndex + commentLength)

    def rehighlight(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        QSyntaxHighlighter.rehighlight(self)
        QApplication.restoreOverrideCursor()
            
            
class CssHighlighter(QSyntaxHighlighter):
    
    Rules = []
    Formats = {}
    def __init__(self, parent=None):
        super(CssHighlighter, self).__init__(parent)
        
        self.initializeFormats()            
        self.cssKeywordRegex = QRegExp(r"""(:?[a-zA-Z0-9-]+:)""")
        CssHighlighter.Rules.append((self.cssKeywordRegex, "keyword"))         
        self.stringRegex = QRegExp(r"""(?:'[^']*'|"[^"]*")""")
        CssHighlighter.Rules.append((self.stringRegex, "strings"))
        CssHighlighter.Rules.append((QRegExp(
               r"[0-9]." 
               # matches 90, 4, 4000 
               r"|[0-9].+\."
               # matches -0x33232F and other hexadecimal nums
               r"|#[0-9A-Fa-f]+"),
               # matches decimals and numbers in pixels
               "number"))
        self.commentStartRegex = QRegExp(r"""(?:\/\*)""")
        self.commentEndRegex = QRegExp(r"""(?:\*\/)""")
        self.importRegex = QRegExp(r"""(:?^@[a-zA-Z0-9-]+)""")
        CssHighlighter.Rules.append((self.importRegex, "importFormat"))
        self.selectorRegex = QRegExp(r"""(:?^[.#].[a-zA-Z0-9-_.#]+|\w+\[\w+=['"].\w+['"].\]|^[a-zA-Z-_,~+>:]+)""")
        CssHighlighter.Rules.append((self.selectorRegex, "selectorChars"))
        self.curliesRegex = QRegExp(r"""(:?\{+|\}+)""")
        CssHighlighter.Rules.append((self.curliesRegex, "curlyBraces"))
        self.parenthesesRegex = QRegExp(r"""(:?\(+|\)+|;+)""")
        CssHighlighter.Rules.append((self.parenthesesRegex, "parentheses"))
        
        
    @staticmethod
    def initializeFormats():
        baseFormat = QTextCharFormat()
        # if for theme changer
        for name, colour in (("normal", QColor(Qt.white)),
             ("keyword", ORANGE), ("comment", GREY), 
             ("strings", OFFRED), ("importFormat", LIGHTPINK),
             ("number", LIGHTCYAN), ("selectorChars", BRIGHTBLUE),
             ("parentheses", LEAFGREEN), ("curlyBraces", LIGHTPURPLE)):
            format = QTextCharFormat(baseFormat)
            format.setForeground(colour)
            if name in ("keyword", "selectorChars", "curlyBraces"):
                format.setFontWeight(QFont.Bold)
            if name == "comment":
                format.setFontItalic(True)
            CssHighlighter.Formats[name] = format
    
    def highlightBlock(self, text):
        NORMAL, COMMENT = range(2)

        textLength = len(text)
        prevState = self.previousBlockState()
 
        self.setFormat(0, textLength, CssHighlighter.Formats["normal"])
        # running through the reg. expressions
        for regex, format in CssHighlighter.Rules:
            i = regex.indexIn(text)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(i, length, CssHighlighter.Formats[format])
                i = regex.indexIn(text, i + length)
        self.setCurrentBlockState(NORMAL)
        if self.stringRegex.indexIn(text) != -1:
            return
        
        startIndex = 0
        endIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartRegex.indexIn(text)
        while startIndex >= 0:
            endIndex = self.commentEndRegex.indexIn(text, startIndex)
            commentLength = 0
            if endIndex == -1:
                self.setCurrentBlockState(COMMENT)
                commentLength = len(text) - startIndex;
            else:
                commentLength = endIndex - startIndex + self.commentEndRegex.matchedLength()
            self.setFormat(startIndex, commentLength, CssHighlighter.Formats["comment"])
            startIndex = self.commentStartRegex.indexIn(text, startIndex + commentLength)
        
    def rehighlight(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        QSyntaxHighlighter.rehighlight(self)
        QApplication.restoreOverrideCursor()
            
            
class JavascriptHighlighter(QSyntaxHighlighter):
    
    Rules = []
    Formats = {}
    def __init__(self, parent=None):
        super(JavascriptHighlighter, self).__init__(parent)
        
        self.initializeFormats()
        JSKEYWORDS = ("break", "export", "return", "case", "for", "switch", "comment", "function", "this", "continue", "if", "typeof", "default", "import", "var", "delete", "in", "void", "do", "label", "while", "else", "new", "with", "abstract", "implements", "protected", "boolean", "instanceOf", "public", "byte", "int", "short", "char", "interface", "static", "double", "long", "synchronized", "false", "native", "throws", "final", "null", "transient", "float", "package", "true", "goto", "private", "catch", "enum", "throw", "class", "extends", "try", "const", "finally", "debugger", "super", "alert", "isFinite", "personalbar", "Anchor", "isNan", "Plugin", "Area", "java", "print", "arguments", "JavaArray", "prompt", "Array", "JavaClass", "prototype", "assign", "JavaObject", "Radio", "blur", "JavaPackage", "ref", "Boolean", "length", "RegExp", "Button", "Link", "releaseEvents", "callee", "location", "Reset", "caller", "Location", "resizeBy", "captureEvents", "locationbar", "resizeTo", "Checkbox", "Math", "routeEvent", "clearInterval", "menubar", "scroll", "clearTimeout", "MimeType", "scrollbars", "close", "moveBy", "scrollBy", "closed", "moveTo", "scrollTo", "confirm", "name", "Select", "constructor", "NaN", "self", "Date", "navigate", "setInterval", "defaultStatus", "navigator", "setTimeout", "document", "Navigator", "status", "Document", "netscape", "statusbar", "Element", "Number", "stop", "escape", "Object", "String", "onBlur", "Submit", "FileUpload", "onError", "sun", "find", "onFocus", "taint", "focus", "onLoad", "Text", "Form", "onUnload", "Textarea", "Frame", "open", "toolbar", "Frames", "opener", "top", "Function", "Option", "toString", "getClass", "outerHeight", "unescape", "Hidden", "OuterWidth", "untaint", "history", "Packages", "unwatch", "History", "pageXoffset", "valueOf", "home", "pageYoffset", "watch", "Image", "parent", "window", "Infinity", "parseFloat", "Window", "InnerHeight", "parseInt", "InnerWidth", "Password" )
        JavascriptHighlighter.Rules.append((QRegExp(
           "|".join([r"\b%s\b" % keyword for keyword in JSKEYWORDS])), "keyword"))        
        self.stringRegex = QRegExp(r"""(?:'[^']*'|"[^"]*")""")
        JavascriptHighlighter.Rules.append((self.stringRegex, "strings"))
        JavascriptHighlighter.Rules.append((QRegExp(
               r"\b[0-9].\b" 
               # matches 90, 4 
               r"|#[0-9a-fA-F]...+"
               r"|0x[0-9a-fA-F]...+"
               # matches #33232F and other hex 0x34ff style nums
               r"|\b[0-9].\.?[0-9].\b"),
               # matches decimals 
               "number"))
        self.commentRegex = QRegExp(r"""(?://.*)""")
        self.commentStartRegex = QRegExp(r"""(?:\/\*)""")
        self.commentEndRegex = QRegExp(r"""(?:\*\/)""")
        JavascriptHighlighter.Rules.append((self.commentRegex, "comment"))
        self.methodRegex = QRegExp(r"""(:?\.[a-z0-9A-Z]+\()""")
        JavascriptHighlighter.Rules.append((self.methodRegex, "methodFormat"))
        self.backslashRegex = QRegExp(r"""(:?\\.)""")
        JavascriptHighlighter.Rules.append((self.backslashRegex, "backslashChars"))
        self.curliesRegex = QRegExp(r"""(:?\{+|\}+)""")
        JavascriptHighlighter.Rules.append((self.curliesRegex, "curlyBraces"))
        self.specChars3Regex = QRegExp(r"""(?:\(+\{+|\}\)+;+|\(\);+)""")
        JavascriptHighlighter.Rules.append((self.specChars3Regex, "specChars3"))
        
        
    @staticmethod
    def initializeFormats():
        baseFormat = QTextCharFormat()
        # if for theme changer
        for name, colour in (("normal", QColor(Qt.white)),
             ("keyword", ORANGE), ("comment", GREY), 
             ("strings", OFFRED), ("methodFormat", LIGHTPINK),
             ("number", LIGHTCYAN), ("backslashChars", LIGHTESTGREY),
             ("curlyBraces", LIGHTPURPLE), ("specChars3", LEAFGREEN)):
            format = QTextCharFormat(baseFormat)
            format.setForeground(colour)
            if name in ("keyword", "specChars3", "curlyBraces"):
                format.setFontWeight(QFont.Bold)
            if name == "comment":
                format.setFontItalic(True)
            JavascriptHighlighter.Formats[name] = format
    
    def highlightBlock(self, text):
        NORMAL, COMMENT = range(2)

        textLength = len(text)
        prevState = self.previousBlockState()
 
        self.setFormat(0, textLength, JavascriptHighlighter.Formats["normal"])
        # running through the reg. expressions
        for regex, format in JavascriptHighlighter.Rules:
            i = regex.indexIn(text)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(i, length, JavascriptHighlighter.Formats[format])
                i = regex.indexIn(text, i + length)
        self.setCurrentBlockState(NORMAL)
        if self.stringRegex.indexIn(text) != -1:
            return
        
        startIndex = 0
        endIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartRegex.indexIn(text)
        while startIndex >= 0:
            endIndex = self.commentEndRegex.indexIn(text, startIndex)
            commentLength = 0
            if endIndex == -1:
                self.setCurrentBlockState(COMMENT)
                commentLength = len(text) - startIndex;
            else:
                commentLength = endIndex - startIndex + self.commentEndRegex.matchedLength()
            self.setFormat(startIndex, commentLength, JavascriptHighlighter.Formats["comment"])
            startIndex = self.commentStartRegex.indexIn(text, startIndex + commentLength)

    def rehighlight(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        QSyntaxHighlighter.rehighlight(self)
        QApplication.restoreOverrideCursor()

            
class SqlHighlighter(QSyntaxHighlighter):
    
    Rules = []
    Formats = {}

    def __init__(self, parent=None):
        super(SqlHighlighter, self).__init__(parent)
        
        self.initializeFormats()
        SQLKEYWORDS = ("ABORT", "ACTION", "ADD", "AFTER", "ALL", "ALTER", "ANALYZE", "AND", "AS", "ASC", "ATTACH", "AUTOINCREMENT", "BEFORE", "BEGIN", "BETWEEN", "BY", "CASCADE", "CASE", "CAST", "CHECK", "COLLATE", "COLUMN", "COMMIT", "CONFLICT", "CONSTRAINT", "CREATE", "CROSS", "CURRENT_DATE", "CURRENT_TIME", "CURRENT_TIMESTAMP", "DATABASE", "DEFAULT", "DEFERRABLE", "DEFERRED", "DELETE", "DESC", "DETACH", "DISTINCT", "DROP", "EACH", "ELSE", "END", "ESCAPE", "EXCEPT", "EXCLUSIVE", "EXISTS", "EXPLAIN", "FAIL", "FOR", "FOREIGN", "FROM", "FULL", "GLOB", "GROUP", "HAVING", "IF", "IGNORE", "IMMEDIATE", "IN", "INDEX", "INDEXED", "INITIALLY", "INNER", "INSERT", "INSTEAD", "INTERSECT", "INTO", "IS", "ISNULL", "JOIN", "KEY", "LEFT", "LIKE", "LIMIT", "MATCH", "NATURAL", "NO", "NOT", "NOTNULL", "NULL", "OF", "OFFSET", "ON", "OR", "ORDER", "OUTER", "PLAN", "PRAGMA", "PRIMARY", "QUERY", "RAISE", "RECURSIVE", "REFERENCES", "REGEXP", "REINDEX", "RELEASE", "RENAME", "REPLACE", "RESTRICT", "RIGHT", "ROLLBACK", "ROW", "SAVEPOINT", "SELECT", "SET", "TABLE", "TEMP", "TEMPORARY", "THEN", "TO", "TRANSACTION", "TRIGGER", "UNION", "UNIQUE", "UPDATE", "USING", "VACUUM", "VALUES", "VIEW", "VIRTUAL", "WHEN", "WHERE", "WITH", "WITHOUT" )
        SqlHighlighter.Rules.append((QRegExp(
           "|".join([r"\b%s\b" % keyword for keyword in SQLKEYWORDS])), "keyword"))         
        self.stringRegex = QRegExp(r"""(?:'[^']*'|"[^"]*")""")
        SqlHighlighter.Rules.append((self.stringRegex, "strings"))
        SqlHighlighter.Rules.append((QRegExp(
               r"\b[0-9]+\b" 
               # matches -90, +4, 4000l 
               r"|\b0[xX].[0-9A-Fa-f]+\b"
               # matches 0x33232F and other hexadecimal nums
               r"|\b[0-9]+(?:\.[0-9]+)?(?:[eE][-+]?[0-9]+)?\b"),
               # matches decimals and numbers with exponents
               "number"))
        self.commentRegex = QRegExp(r"""(?:[//]+)""")
        self.commentStartRegex = QRegExp(r"""(?:\/\*)""")
        self.commentEndRegex = QRegExp(r"""(?:\*\/)""")
        SqlHighlighter.Rules.append((self.commentRegex, "comment"))
        self.parenthesesRegex = QRegExp(r"""(:?\(+|\)+)""")
        SqlHighlighter.Rules.append((self.parenthesesRegex, "parentheses"))
        self.colonRegex = QRegExp(r"""(?:[:;].)""")
        SqlHighlighter.Rules.append((self.colonRegex, "colons"))
        
    @staticmethod
    def initializeFormats():
        baseFormat = QTextCharFormat()
        # if for theme changer
        for name, colour in (("normal", QColor(Qt.white)),
             ("keyword", ORANGE), ("comment", GREY), 
             ("strings", OFFRED), ("number", LIGHTCYAN), 
             ("parentheses", LEAFGREEN), ("colons", LIGHTPURPLE)):
            format = QTextCharFormat(baseFormat)
            format.setForeground(colour)
            if name in ("keyword", "parentheses"):
                format.setFontWeight(QFont.Bold)
            if name == "comment":
                format.setFontItalic(True)
            SqlHighlighter.Formats[name] = format
    
    def highlightBlock(self, text):
        NORMAL, COMMENT = range(2)

        textLength = len(text)
        prevState = self.previousBlockState()
 
        self.setFormat(0, textLength, SqlHighlighter.Formats["normal"])
        # running through the reg. expressions
        for regex, format in SqlHighlighter.Rules:
            i = regex.indexIn(text)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(i, length, SqlHighlighter.Formats[format])
                i = regex.indexIn(text, i + length)
        self.setCurrentBlockState(NORMAL)
        if self.stringRegex.indexIn(text) != -1:
            return
        
        startIndex = 0
        endIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartRegex.indexIn(text)
        while startIndex >= 0:
            endIndex = self.commentEndRegex.indexIn(text, startIndex)
            commentLength = 0
            if endIndex == -1:
                self.setCurrentBlockState(COMMENT)
                commentLength = len(text) - startIndex;
            else:
                commentLength = endIndex - startIndex + self.commentEndRegex.matchedLength()
            self.setFormat(startIndex, commentLength, SqlHighlighter.Formats["comment"])
            startIndex = self.commentStartRegex.indexIn(text, startIndex + commentLength)

    def rehighlight(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        QSyntaxHighlighter.rehighlight(self)
        QApplication.restoreOverrideCursor()
           
           

           
if __name__ == "__main__":
    import doctest
    doctest.testmod()
