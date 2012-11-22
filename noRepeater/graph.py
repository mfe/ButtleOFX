import sys
from PySide import QtGui, QtDeclarative


def main():

    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()
    view.setWindowTitle("Graph editor")
    view.setSource('qml/graph.qml')

    # QDeclarativeItem* nodeItem = qobject_cast<QDeclarativeItem*>(nodeComponent->create());
    # nodeItem->setParentItem(qobject_cast<QDeclarativeItem*>(m_view.rootObject()));

    # Creates a QDeclarativeComponent from Node.qml giving the specified engine and parent
    # The QDeclarativeComponent class encapsulates a QML component definition
    # The QDeclarativeEngine class provides an environment for instantiating QML components
    nodeComponent = QtDeclarative.QDeclarativeComponent(view.engine(), 'qml/Node.qml')

    # The QDeclarativeItem class provides the most basic of all visual items in QML
    nodeItem = QtDeclarative.QDeclarativeItem(nodeComponent.create())

    # view.rootObject() returns a QGraphicsObject
    # Expected a QDeclarativeIttem
    nodeItem.setParentItem(view.rootObject())

    view.show()
    app.exec_()

if __name__ == '__main__':
    main()
