__author__ = 'alefur'
from functools import partial

from PyQt5.QtWidgets import QGridLayout, QGroupBox, QLabel, QPushButton


class ValueGB(QGroupBox):
    def __init__(self, title, model, key, ind, fmt):
        self.title = title

        QGroupBox.__init__(self)
        self.setTitle('%s' % self.title)

        self.grid = QGridLayout()
        self.value = QLabel()

        self.grid.addWidget(self.value, 0, 0)
        self.setLayout(self.grid)

        keyvar = model.keyVarDict[key]

        self.setColor('green')
        keyvar.addCallback(partial(self.updateVals, self, ind, fmt))

    def updateVals(self, label, ind, fmt, keyvar):
        values = keyvar.getValue(doRaise=False)
        values = (values,) if not isinstance(values, tuple) else values

        value = values[ind]

        strValue = 'nan' if value is None else fmt.format(value)
        label.setText(strValue)
        label.pimpMe()

    def setColor(self, background, police='white'):
        if background == "red":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #f43131, stop: 1 #5e1414);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        elif background == "green":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #45f42e, stop: 1 #195511);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        elif background == "blue":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #3168f4, stop: 1 #14195e);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        elif background == "yellow":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #edf431, stop: 1 #5e5b14);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        elif background == "orange":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #f4a431, stop: 1 #5e4a14);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")

        self.value.setStyleSheet("QLabel{font-size: 11pt; qproperty-alignment: AlignCenter; color:%s;}" % police)

    def setText(self, txt):
        self.value.setText(txt)

    def pimpMe(self):
        pass


class LeakageBox(ValueGB):
    def updateVals(self, label, ind, fmt, keyvar):
        values = keyvar.getValue(doRaise=False)
        values = (values,) if not isinstance(values, tuple) else values

        value = values[ind]

        if value == 0:
            self.setColor('green')
            label.setText('OK')
        else:
            self.setColor('red')
            label.setText('Alarm')
        label.pimpMe()


class PowerButton(QGroupBox):
    def __init__(self, title, model, key, ind, sendCmd, onCmd, offCmd):
        self.title = title
        self.sendCmd = sendCmd
        self.onCmd = onCmd
        self.offCmd = offCmd

        QGroupBox.__init__(self)
        self.setTitle('%s' % self.title)

        self.grid = QGridLayout()
        self.value = QLabel()
        self.button = QPushButton()

        self.grid.addWidget(self.value, 0, 0)
        self.grid.addWidget(self.button, 1, 0)
        self.setLayout(self.grid)

        keyvar = model.keyVarDict[key]

        self.setColor('gray')
        keyvar.addCallback(partial(self.updateVals, ind))

    def updateVals(self, ind, keyvar):
        values = keyvar.getValue(doRaise=False)
        values = (values,) if not isinstance(values, tuple) else values

        value = values[ind]

        if value == 0:
            self.setColor('gray')
            self.setText('Off', 'Turn On')
            self.connect(self.onCmd)
        else:
            self.setColor('green')
            self.setText('On', 'Turn Off')
            self.connect(self.offCmd)

    def setColor(self, background, police='white'):
        if background == "red":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #f43131, stop: 1 #5e1414);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        elif background == "green":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #45f42e, stop: 1 #195511);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        elif background == "blue":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #3168f4, stop: 1 #14195e);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        elif background == "yellow":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #edf431, stop: 1 #5e5b14);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        elif background == "orange":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #f4a431, stop: 1 #5e4a14);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        elif background == "gray":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #a3a9ac, stop: 1 #13191c);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")

        self.value.setStyleSheet("QLabel{font-size: 11pt; qproperty-alignment: AlignCenter; color:%s;}" % police)

    def setText(self, txt, txt2):
        self.value.setText(txt)
        self.button.setText(txt2)

    def connect(self, cmdStr):
        while True:
            try:
                self.button.clicked.disconnect()
            except TypeError:
                break
        self.button.clicked.connect(partial(self.sendCmd, cmdStr))

    def pimpMe(self):
        pass


class ResetButton(QGroupBox):
    def __init__(self, title, model, key, ind, sendCmd, cmdStr):
        self.title = title
        self.sendCmd = sendCmd

        QGroupBox.__init__(self)
        self.setTitle('%s' % self.title)

        self.grid = QGridLayout()
        self.value = QLabel()
        self.button = QPushButton()
        self.connect(cmdStr)

        self.grid.addWidget(self.value, 0, 0)
        self.grid.addWidget(self.button, 1, 0)
        self.setLayout(self.grid)

        keyvar = model.keyVarDict[key]

        self.setColor('gray')
        keyvar.addCallback(partial(self.updateVals, ind))

    def updateVals(self, ind, keyvar):
        values = keyvar.getValue(doRaise=False)
        values = (values,) if not isinstance(values, tuple) else values

        value = values[ind]

        if value == 0:
            self.setColor('gray')
            self.setText('Off')
        else:
            self.setColor('green')
            self.setText('On')

    def setColor(self, background, police='white'):
        if background == "red":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #f43131, stop: 1 #5e1414);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        elif background == "green":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #45f42e, stop: 1 #195511);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        elif background == "blue":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #3168f4, stop: 1 #14195e);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        elif background == "yellow":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #edf431, stop: 1 #5e5b14);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        elif background == "orange":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #f4a431, stop: 1 #5e4a14);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        elif background == "gray":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #a3a9ac, stop: 1 #13191c);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")

        self.value.setStyleSheet("QLabel{font-size: 11pt; qproperty-alignment: AlignCenter; color:%s;}" % police)

    def setText(self, txt):
        self.value.setText(txt)

    def connect(self, cmdStr):
        while True:
            try:
                self.button.clicked.disconnect()
            except TypeError:
                break
        self.button.clicked.connect(partial(self.sendCmd, cmdStr))
        self.button.setText('Reset')

    def pimpMe(self):
        pass
