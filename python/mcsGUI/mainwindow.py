__author__ = 'alefur'

from datetime import datetime as dt
from functools import partial

from PyQt5.QtWidgets import QGridLayout, QWidget, QGroupBox, QLineEdit, QPushButton, QPlainTextEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QTextCursor

from widgets import ValueGB, LeakageBox, PowerButton, ResetButton
from graph import Graph, Curve


class LogArea(QPlainTextEdit):
    def __init__(self):
        QPlainTextEdit.__init__(self)
        self.logArea = QPlainTextEdit()
        self.setMaximumBlockCount(10000)
        self.setReadOnly(True)

        self.setStyleSheet("background-color: black;color:white;")
        self.setFont(QFont("Monospace", 8))

    def newLine(self, line):
        self.insertPlainText("\n%s  %s" % (dt.now().strftime("%H:%M:%S.%f"), line))
        self.moveCursor(QTextCursor.End)
        self.ensureCursorVisible()

    def trick(self, qlineedit):
        self.newLine(qlineedit.text())


class McsGUI(QWidget):
    def __init__(self, mainTree):
        QWidget.__init__(self)
        self.mainTree = mainTree
        self.mainLayout = QGridLayout()
        self.windowLayout = QHBoxLayout()
        self.labelLayout = QGridLayout()

        self.labelLayout.addWidget(ValueGB('Temp-1(C) ', self.actor.models['meb'], 'temps', 0, '{:g}'), 0, 0)
        self.labelLayout.addWidget(ValueGB('Temp-2(C) ', self.actor.models['meb'], 'temps', 1, '{:g}'), 0, 1)
        self.labelLayout.addWidget(ValueGB('Temp-3(C) ', self.actor.models['meb'], 'temps', 2, '{:g}'), 0, 2)
        self.labelLayout.addWidget(ValueGB('Temp-4(C) ', self.actor.models['meb'], 'temps', 3, '{:g}'), 0, 3)
        self.labelLayout.addWidget(ValueGB('Temp-5(C) ', self.actor.models['meb'], 'temps', 4, '{:g}'), 1, 0)
        self.labelLayout.addWidget(ValueGB('Temp-6(C) ', self.actor.models['meb'], 'temps', 5, '{:g}'), 1, 1)
        self.labelLayout.addWidget(ValueGB('Temp-7(C) ', self.actor.models['meb'], 'temps', 6, '{:g}'), 1, 2)
        self.labelLayout.addWidget(ValueGB('Flow meter ', self.actor.models['meb'], 'flow', 0, '{:g}'), 1, 3)
        self.labelLayout.addWidget(PowerButton('Camera ', self.actor.models['meb'], 'power', 0, self.sendCommand, 'meb power on mc', 'meb power off mc'), 2, 0, 2, 1)
        self.labelLayout.addWidget(PowerButton('Shutter/Temp/Flow ', self.actor.models['meb'], 'power', 1, self.sendCommand, 'meb power on stf', 'meb power off stf'), 2, 1, 2, 1)
        self.labelLayout.addWidget(ResetButton('Cisco ', self.actor.models['meb'], 'power', 2, self.sendCommand, 'meb power bounce cisco'), 2, 2, 2, 1)
        self.labelLayout.addWidget(PowerButton('PC/Cooling ', self.actor.models['meb'], 'power', 3, self.sendCommand, 'meb power on pc', 'meb power off pc'), 2, 3, 2, 1)

        self.commandLine = QLineEdit()
        self.commandButton = QPushButton('Send Command')
        self.commandButton.clicked.connect(self.sendCmdLine)

        self.logArea = LogArea()

        self.mainLayout.addLayout(self.labelLayout, 0, 0, 1, 4)

        self.mainLayout.addWidget(self.commandLine, 1, 0, 1, 3)
        self.mainLayout.addWidget(self.commandButton, 1, 3, 1, 1)

        self.mainLayout.addWidget(self.logArea, 2, 0, 1, 4)
        self.setLayout(self.mainLayout)

    @property
    def actor(self):
        return self.mainTree.actor

    def createButton(self, title, cmdStr):
        button = QPushButton(title)
        button.clicked.connect(partial(self.sendCommand, cmdStr))
        return button

    def sendCmdLine(self):
         self.sendCommand(self.commandLine.text())

    def sendCommand(self, fullCmd):
        import opscore.actor.keyvar as keyvar
        [actor, cmdStr] =fullCmd.split(' ', 1)
        self.logArea.newLine('cmdIn=%s %s' % (actor, cmdStr))
        self.actor.cmdr.bgCall(**dict(actor=actor,
                                      cmdStr=cmdStr,
                                      timeLim=600,
                                      callFunc=self.returnFunc,
                                      callCodes=keyvar.AllCodes))

    def returnFunc(self, cmdVar):
        self.logArea.newLine('cmdOut=%s' % cmdVar.replyList[0].canonical())
        for i in range(len(cmdVar.replyList)-1):
            self.logArea.newLine(cmdVar.replyList[i+1].canonical())
