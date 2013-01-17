from PySide import QtGui, QtDeclarative
import os
# data
from buttleofx.datas import ButtleData
#connections
from buttleofx.gui.graph.connection import LineItem
# paramEditor
from buttleofx.gui.paramEditor.params import ParamInt
from buttleofx.gui.paramEditor.params import ParamString
from buttleofx.gui.paramEditor.wrappers import ParamEditorWrapper
# undo_redo
from buttleofx.core.undo_redo.manageTools import CommandManager

currentFilePath = os.path.dirname(os.path.abspath(__file__))


def main(argv):
    QtDeclarative.qmlRegisterType(LineItem, "ConnectionLineItem", 1, 0, "ConnectionLine")

    # data
    buttleData = ButtleData()

    # create undo-redo context
    cmdManager = CommandManager()
    cmdManager.setActive()
    cmdManager.clean()

    # create application
    QApplication = QtGui.QApplication(argv)
    view = QtDeclarative.QDeclarativeView()
    view.setWindowTitle("ButtleOFX")
    rc = view.rootContext()

    # data
    buttleData = ButtleData().init(view)
    #graph.createNode("Blur", cmdManager)
    rc.setContextProperty("_buttleData", buttleData)
    rc.setContextProperty("_cmdManager", cmdManager)

    paramList = []
    paramsW = ParamEditorWrapper(view, paramList)
    rc.setContextProperty('_paramList', paramsW)

    # launch QML
    view.setSource(os.path.join(currentFilePath, "MainWindow.qml"))
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    view.show()
    QApplication.exec_()
