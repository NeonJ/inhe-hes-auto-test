# -*- coding: UTF-8 -*-

import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QKeyEvent
from PyQt5.QtWidgets import QApplication, QInputDialog, QMessageBox
# 弹窗停留时长, 单位:秒
from libs.Singleton import Singleton

QT_TIMEOUT = Singleton().QT_TIMEOUT

# ICON图标存储目录
ICON_BASE_DIR = os.path.join('icons', Singleton().Project)


class InputDialog(QInputDialog):

    def __init__(self, parent=None):
        QInputDialog.__init__(self, parent)
        self.timeout = 0
        self.autoclose = False
        self.currentTime = 0

    def showEvent(self, QShowEvent):
        self.currentTime = 0
        if self.autoclose:
            self.startTimer(1000)

    def timerEvent(self, *args, **kwargs):
        self.currentTime += 1
        if self.currentTime >= self.timeout:
            self.done(0)

    def eventFilter(self, watched, event):
        if event.type() == QKeyEvent.KeyPress:
            return True
        else:
            return QInputDialog.eventFilter(self, watched, event)

    @staticmethod
    def GetInteger(defaultValue=0, minValue=0, maxValue=100, step=1, message='Enter an integer number:', title='KATS',
                   timeout=QT_TIMEOUT):
        value = defaultValue

        def getValue(val):
            nonlocal value
            value = val

        app = QApplication(sys.argv)
        m = InputDialog()
        # 确保弹窗一直以前置方式显示
        m.setWindowFlags(Qt.WindowStaysOnTopHint)
        m.autoclose = True
        m.timeout = timeout
        m.setLabelText(message)
        m.setWindowTitle(title)
        m.setIntValue(defaultValue)
        m.setIntMinimum(minValue)
        m.setIntMaximum(maxValue)
        m.setIntStep(step)
        m.show()
        m.intValueChanged.connect(getValue)
        if app.exec_() == 0:
            return value

    @staticmethod
    def GetDouble(defaultValue=0.0, minValue=0.0, maxValue=100.0, step=1, message='Enter an float number:',
                  title='KATS', timeout=QT_TIMEOUT):
        value = defaultValue

        def getValue(val):
            nonlocal value
            value = val

        app = QApplication(sys.argv)
        m = InputDialog()
        # 确保弹窗一直以前置方式显示
        m.setWindowFlags(Qt.WindowStaysOnTopHint)
        m.autoclose = True
        m.timeout = timeout
        m.setLabelText(message)
        m.setWindowTitle(title)
        m.setDoubleValue(defaultValue)
        m.setDoubleMinimum(minValue)
        m.setDoubleMaximum(maxValue)
        m.setDoubleStep(step)
        m.show()
        m.doubleValueChanged.connect(getValue)

        app.installEventFilter(m)
        if app.exec_() == 0:
            return value

    @staticmethod
    def GetChoice(itemList, message='Select an item', title='KATS', timeout=QT_TIMEOUT):
        value = itemList[0]

        def getValue(val):
            nonlocal value
            value = val

        app = QApplication(sys.argv)
        m = InputDialog()
        # 确保弹窗一直以前置方式显示
        m.setWindowFlags(Qt.WindowStaysOnTopHint)
        m.autoclose = True
        m.timeout = timeout
        m.setLabelText(message)
        m.setWindowTitle(title)
        m.setComboBoxItems(itemList)
        m.show()
        m.textValueChanged.connect(getValue)

        app.installEventFilter(m)
        if app.exec_() == 0:
            return value

    @staticmethod
    def GetText(message='Select an item', title='KATS', timeout=QT_TIMEOUT):
        value = ''

        def getValue(val):
            nonlocal value
            value = val

        app = QApplication(sys.argv)
        m = InputDialog()
        # 确保弹窗一直以前置方式显示
        m.setWindowFlags(Qt.WindowStaysOnTopHint)
        m.autoclose = True
        m.timeout = timeout
        m.setLabelText(message)
        m.setWindowTitle(title)
        m.show()
        m.textValueChanged.connect(getValue)

        app.installEventFilter(m)
        if app.exec_() == 0:
            return value


class MessageBox(QMessageBox):

    def __init__(self, *__args):
        QMessageBox.__init__(self)
        self.timeout = 0
        self.autoclose = False
        self.currentTime = 0

    def showEvent(self, QShowEvent):
        self.currentTime = 0
        if self.autoclose:
            self.startTimer(1000)

    def timerEvent(self, *args, **kwargs):
        self.currentTime += 1
        if self.currentTime >= self.timeout:
            self.done(0)

    def eventFilter(self, watched, event):
        if event.type() == QKeyEvent.KeyPress:
            return True
        else:
            return QMessageBox.eventFilter(self, watched, event)

    @staticmethod
    def Question(message, icon=None, suffix='png', title='KATS', timeout=QT_TIMEOUT):
        value = 'No'

        def getValue(val):
            nonlocal value
            value = val.text().replace("&", "")

        app = QApplication(sys.argv)
        m = MessageBox()
        # 确保弹窗一直以前置方式显示
        m.setWindowFlags(Qt.WindowStaysOnTopHint)
        m.autoclose = True
        m.timeout = timeout
        m.setText(message)
        m.setWindowTitle(title)
        m.setIcon(QMessageBox.Question)
        m.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        m.setDefaultButton(QMessageBox.No)
        # 设置图标
        if icon is None:
            m.setIcon(QMessageBox.Question)
        else:
            m.setIconPixmap(QPixmap(os.path.join(ICON_BASE_DIR, f"{icon}.{suffix}")))
        m.buttonClicked.connect(getValue)

        app.installEventFilter(m)
        m.show()
        if app.exec_() == 0:
            return value

    @staticmethod
    def Information(message, title='KATS', timeout=QT_TIMEOUT):
        app = QApplication(sys.argv)
        m = MessageBox()
        # 确保弹窗一直以前置方式显示
        m.setWindowFlags(Qt.WindowStaysOnTopHint)
        m.autoclose = True
        m.timeout = timeout
        m.setText(message)
        m.setWindowTitle(title)
        m.setIcon(QMessageBox.Information)
        m.setStandardButtons(QMessageBox.Ok)
        m.setDefaultButton(QMessageBox.Ok)

        app.installEventFilter(m)
        m.show()
        app.exec_()

    @staticmethod
    def Warning(message, title='KATS', timeout=QT_TIMEOUT):
        app = QApplication(sys.argv)
        m = MessageBox()
        # 确保弹窗一直以前置方式显示
        m.setWindowFlags(Qt.WindowStaysOnTopHint)
        m.autoclose = True
        m.timeout = timeout
        m.setText(message)
        m.setWindowTitle(title)
        m.setIcon(QMessageBox.Warning)
        m.setStandardButtons(QMessageBox.Ok)
        m.setDefaultButton(QMessageBox.Ok)

        app.installEventFilter(m)
        m.show()
        app.exec_()


if __name__ == '__main__':
    # print(InputDialog.GetInteger(message='请输入一个整数'))
    # print(InputDialog.GetDouble(message='请输入一个浮点数'))
    # print(InputDialog.GetChoice(itemList=['Camel', 'Normal16', 'Cetus02'], message='请选择一款电表'))
    # print(InputDialog.GetText(message='请输入序列号'))

    # print(MessageBox.Question(message='继续执行用例？'))
    # print(MessageBox.Information(message='请切断电表电源'))
    print(MessageBox.Warning(message='电表电源没有连接上'))
