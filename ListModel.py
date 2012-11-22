from PySide import QtCore
from Node import Node
from NodeWrapper import NodeWrapper


class ListModel(QtCore.QAbstractListModel):

    """
        Class ListModel defined by:
        - elements : list of objects
        - setRoleNames

        Creates a ListModel object containing a given object list
    """

    #One column with one object per row
    ROWS = ['element']

    def __init__(self, elements):
        QtCore.QAbstractListModel.__init__(self)
        # Stores the passed objects list as a class member
        self.elements = elements
        self.setRoleNames(dict(enumerate(ListModel.ROWS)))

    # Returns data for the specified role, from the item with the given index
    @QtCore.Slot()
    def data(self, index, role):
        if index.isValid() and role == ListModel.ROWS.index('element'):
            return self.elements[index.row()]
        return None

    # Returns the number of rows in the model
    # Corresponds to the number of items in the model's internal object list
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.elements)

    # Appends a new element to the listModel
    @QtCore.Slot()
    def addElement(self):
        self.beginInsertRows(QtCore.QModelIndex(), len(self.elements), len(self.elements))
        self.elements.append(NodeWrapper(Node('Node' + str(len(self.elements) + 1), 10, 40, 187, 187, 187, 1)))
        self.endInsertRows()

    # Removes an element of the listModel
    @QtCore.Slot(int)
    def removeElement(self, index):
        if len(self.elements) > 0:
            self.beginRemoveRows(QtCore.QModelIndex(), index, index)
            self.elements.pop(index)
            self.endRemoveRows()
