# Tuttle
from buttleofx.data import tuttleTools

from quickmamba.models import QObjectListModel

from PySide import QtCore
# core : graph
from buttleofx.core.graph import Graph
from buttleofx.core.graph.connection import IdClip
# gui : graphWrapper
from buttleofx.gui.graph import GraphWrapper
# undo redo
from buttleofx.core.undo_redo.manageTools import CommandManager
from buttleofx.core.undo_redo.commands import CmdSetCoord
#quickmamba
from quickmamba.patterns import Singleton


class ButtleData(QtCore.QObject, Singleton):
    """
        Class ButtleData defined by:
        - _graphWrapper
        - _graph
        - _currentNodeViewer
        - _currentNodeParam
        - _currentNodeGraph

        This class :
            - containts all data we need to manage the application.
            - receives the undo and redo from QML, and call the cmdManager to do this.
    """
    def init(self, view):
        self._graph = Graph()
        self._graphWrapper = GraphWrapper(self._graph, view)

        self._currentParamNodeName = None
        self._currentParamNodeWrapper = None

        self._currentSelectedNodeNameList = []
        #self._currentSelectedNodeWrapperList = QObjectListModel()

        self._currentViewerNodeName = None
        self._currentViewerNodeWrapper = None

        return self

    ################################################## GETTERS ET SETTERS ##################################################

    #################### getters ####################

    def getGraph(self):
        return self._graph

    def getGraphWrapper(self):
        return self._graphWrapper

    def getCurrentParamNodeName(self):
        """
            Returns the name of the current param node.
        """
        return self._currentParamNodeName

    # def getCurrentSelectedNodeName(self):
    #     """
    #         Returns the name of the current selected node.
    #     """
    #     return self._currentSelectedNodeName

    def getCurrentSelectedNodeNameList(self):
        # tmp = self._currentSelectedNodeNameList
        # self._currentSelectedNodeNameList = QObjectListModel()
        # for value in tmp:
        #     self._currentSelectedNodeNameList.append(value)
        return self._currentSelectedNodeNameList

    @QtCore.Slot(int, result="QVariant")
    def getCurrentSelectedNodeNameIndex(self, index):
        return self.getCurrentSelectedNodeNameList()[index]

    def getCurrentViewerNodeName(self):
        """
            Returns the name of the current viewer node.
        """
        return self._currentViewerNodeName

    def getCurrentParamNodeWrapper(self):
        """
            Returns the current param nodeWrapper.
        """
        return self.getGraphWrapper().getNodeWrapper(self.getCurrentParamNodeName())

    # def getCurrentSelectedNodeWrapper(self):
    #     """
    #         Returns the current selected nodeWrapper.
    #     """
    #     return self.getGraphWrapper().getNodeWrapper(self.getcurrentSelectedNodeNameList())

    # def getCurrentSelectedNodeWrapperList(self):
    #     # tmp = self._currentSelectedNodeWrapperList
    #     # self._currentSelectedNodeWrapperList = QObjectListModel()
    #     # for value in tmp:
    #     #     self._currentSelectedNodeWrapperList.append(value)
    #     return self._currentSelectedNodeWrapperList

    # @QtCore.Slot(int, result="QVariant")
    # def getCurrentSelectedNodeWrapperIndex(self, index):
    #     return self.getCurrentSelectedNodeWrapperList()[index]

    def getCurrentViewerNodeWrapper(self):
        """
            Returns the current viewer nodeWrapper.
        """
        return self.getGraphWrapper().getNodeWrapper(self.getCurrentViewerNodeName())

    #################### setters ####################

    def setCurrentParamNodeWrapper(self, nodeWrapper):
        """
            Changes the current param node and emits the change.
        """
        if self._currentParamNodeName == nodeWrapper.getName():
            return
        self._currentParamNodeName = nodeWrapper.getName()
        self.currentParamNodeChanged.emit()

    # def setCurrentSelectedNodeWrapper(self, nodeWrapper):
    #     """
    #     Changes the current selected node and emits the change.
    #     """
    #     # if self._currentSelectedNodeName == nodeWrapper.getName():
    #     #     return
    #     # self._currentSelectedNodeName = nodeWrapper.getName()
    #     # self.currentSelectedNodeChanged.emit()

    #     self._currentSelectedNodeWrapper = QObjectListModel()
    #     self._currentSelectedNodeWrapper.append(nodeWrapper)
    #     self._currentSelectedNodeNameList.append(nodeWrapper.getName())
    #     self.currentSelectedNodeChanged.emit()

    # def setCurrentSelectedNodeWrapperList(self, nodeWrapper):
    #     self._currentSelectedNodeWrapper = QObjectListModel()
    #     self._currentSelectedNodeWrapper.append(nodeWrapper)
    #     self.currentSelectedNodeWrapperListChanged.emit()

    def setCurrentSelectedNodeNameList(self, nodeWrapper):
        self._currentSelectedNodeNameList.append(nodeWrapper.getName())
        self.currentSelectedNodeNameListChanged.emit()

    def setCurrentViewerNodeWrapper(self, nodeWrapper):
        """
        Changes the current viewer node and emits the change.
        """
        if self._currentViewerNodeName == nodeWrapper.getName():
            return
        self._currentViewerNodeName = nodeWrapper.getName()
        self.currentViewerNodeChanged.emit()

    ################################################## EVENT FROM QML #####################################################

    ########################## CREATION & DESTRUCTION ############################

    ##### Node #####

    @QtCore.Slot(str, int, int)
    def creationNode(self, nodeType, x, y):
        """
            Function called when we want to create a node from the QML.
        """
        self.getGraph().createNode(nodeType, x, y)

    # @QtCore.Slot()
    # def destructionNode(self):
    #     """
    #         Function called when we want to delete a node from the QML.
    #     """
    #     # if at least one node in the graph
    #     if len(self.getGraphWrapper().getNodeWrappers()) > 0 and len(self.getGraph().getNodes()) > 0:
    #         # if a node is selected
    #         if self._currentSelectedNodeName != None:
    #             for nodeName in self._currentSelectedNodeName:
    #                 self.getGraph.deleteNode(nodeName)

    #             #self.getGraph().deleteNode(self._currentSelectedNodeName)
    #     self._currentSelectedNodeName = []
    #     self.currentSelectedNodeChanged.emit()
    #     self._currentParamNodeName = None
    #     self.currentParamNodeChanged.emit()
    #     self._currentViewerNodeName = None
    #     self.currentViewerNodeChanged.emit()

    @QtCore.Slot()
    def destructionNode(self):
        #if at least one node in the graph
        if len(self.getGraphWrapper().getNodeWrappers()) > 0 and len(self.getGraph().getNodes()) > 0:
            # if a node is selected
            if self._currentSelectedNodeNameList != []:
                for nodeName in self._currentSelectedNodeNameList:
                    self.getGraph().deleteNode(nodeName)
                    #self._currentSelectedNodeNameList.remove(nodeName)
                    print "remove ", nodeName
        self._currentSelectedNodeNameList = []
        self.currentSelectedNodeNameListChanged.emit()

        if self._currentSelectedNodeNameList != []:
            print "Unable to delete all selected nodes !"

                #self.getGraph().deleteNode(self._currentSelectedNodeName)
        self.currentParamNodeChanged.emit()
        self._currentParamNodeName = None
        self._currentViewerNodeName = None
        self.currentViewerNodeChanged.emit()

    ##### Connection #####

    def connect(self, clipOut, clipIn):
        """
            Add a connection between 2 clips.
        """
        self.getGraph().createConnection(clipOut, clipIn)
        self.getGraphWrapper().resetTmpClips()

    def disconnect(self, connection):
        """
            Remove a connection between 2 clips.
        """
        self.getGraph().deleteConnection(connection)
        self.getGraphWrapper().resetTmpClips()

    @QtCore.Slot(str, str, int)
    def clipPressed(self, nodeName, port, clipNumber):
        """
            Function called when a clip is pressed (but not released yet).
            The function replace the tmpClipIn or tmpClipOut.
        """
        position = self.getGraphWrapper().getPositionClip(nodeName, port, clipNumber)
        idClip = IdClip(nodeName, port, clipNumber, position)
        if (port == "input"):
            self.getGraphWrapper().setTmpClipIn(idClip)
        elif (port == "output"):
            self.getGraphWrapper().setTmpClipOut(idClip)

    @QtCore.Slot(str, str, int)
    def clipReleased(self, nodeName, port, clipNumber):
        """
            Function called when a clip is released (after pressed).
        """
        if (port == "input"):
            #if there is a tmpNodeOut
            if (self.getGraphWrapper().getTmpClipOut() != None and self.getGraphWrapper().getTmpClipOut()._nodeName != nodeName):
                position = self.getGraphWrapper().getPositionClip(nodeName, port, clipNumber)
                idClip = IdClip(nodeName, port, clipNumber, position)
                if self.getGraphWrapper().canConnect(self.getGraphWrapper().getTmpClipOut(), idClip):
                    self.connect(self.getGraphWrapper().getTmpClipOut(), idClip)
                elif self.getGraph().contains(self.getGraphWrapper().getTmpClipOut()) and self.getGraph().contains(idClip):
                    self.disconnect(self.getGraphWrapper().getConnectionByClips(self.getGraphWrapper().getTmpClipOut(), idClip))
                else:
                    print "Unable to connect or delete the nodes."

        elif (port == "output"):
            #if there is a tmpNodeIn
            if (self.getGraphWrapper().getTmpClipIn() != None and self.getGraphWrapper().getTmpClipIn()._nodeName != nodeName):
                position = self.getGraphWrapper().getPositionClip(nodeName, port, clipNumber)
                idClip = IdClip(nodeName, port, clipNumber, position)
                if self.getGraphWrapper().canConnect(idClip, self.getGraphWrapper().getTmpClipIn()):
                    self.connect(idClip, self.getGraphWrapper().getTmpClipIn())
                elif self.getGraph().contains(self.getGraphWrapper().getTmpClipIn()) and self.getGraph().contains(idClip):
                    self.disconnect(self.getGraphWrapper().getConnectionByClips(idClip, self.getGraphWrapper().getTmpClipIn()))
                else:
                    print "Unable to connect or delete the nodes."

    ################################################## INTERACTIONS ##################################################

    @QtCore.Slot(str, int, int)
    def nodeMoved(self, nodeName, x, y):
        """
            Manage when a node is moved.
        """
        # only push a cmd if the node truly moved
        if self.getGraph().getNode(nodeName).getOldCoord() != (x, y):
            cmdMoved = CmdSetCoord(self.getGraph(), nodeName, (x, y))
            cmdManager = CommandManager()
            cmdManager.push(cmdMoved)

    @QtCore.Slot(str, int, int)
    def nodeIsMoving(self, nodeName, x, y):
        """
            Manage when a node is moved.
        """
        self.getGraph().getNode(nodeName).setCoord(x, y)
        self.getGraph().connectionsCoordChanged()

    ######################### UNDO & REDO ############################

    @QtCore.Slot()
    def undo(self):
        """
            Call the cmdManager to undo the last command.
        """
        cmdManager = CommandManager()
        cmdManager.undo()

    @QtCore.Slot()
    def redo(self):
        """
            Call the cmdManager to redo the last command.
        """
        cmdManager = CommandManager()
        cmdManager.redo()

    def getQObjectPluginsIdentifiers(self):
        """
            Returns a QObjectListModel of all names of Tuttle's plugins.
        """
        pluginsNames = QObjectListModel(self)
        pluginsNames.setObjectList(tuttleTools.getPluginsNames())
        return pluginsNames

    @QtCore.Slot(str, result="QVariant")
    def getQObjectPluginsIdentifiersByParentPath(self, pathname):
        pluginsIds = QObjectListModel(self)
        pluginsIds.setObjectList(tuttleTools.getPluginsIdentifiersByParentPath(pathname))
        return pluginsIds

    @QtCore.Slot(str, result=bool)
    def nextSonIsAPlugin(self, pathname):
        return pathname not in tuttleTools.getPluginsIdentifiersAsDictionary()

    ################################################# LISTS ############################################
    # @QtCore.Slot("QVariant")
    # def addNodeWrapperToList(self, nodeWrapper):
    #     self._currentSelectedNodeWrapperList.append(nodeWrapper)
    #     self.currentSelectedNodeWrapperListChanged.emit()

    @QtCore.Slot("QVariant")
    def addNodeNameToList(self, nodeWrapper):
        if nodeWrapper.getName() not in self._currentSelectedNodeNameList:
            self._currentSelectedNodeNameList.append(nodeWrapper.getName())
        else:
            self._currentSelectedNodeNameList.remove(nodeWrapper.getName())
        self.currentSelectedNodeNameListChanged.emit()

    @QtCore.Slot("QVariant", result=bool)
    def isNodeWrapperInCurrentNodeWrapperList(self, nodeName):
        print "In function"
        print "NodeNameList", self._currentSelectedNodeNameList
        #print "NodeWrapperList", self._currentSelectedNodeWrapperList
        for nodeNameElement in self._currentSelectedNodeNameList:
            print "isNodeWrapperInCurrentNodeNameList"
            print nodeName
            print nodeNameElement
            if nodeName == nodeNameElement:
                return True

        return False

    ################################################## DATA EXPOSED TO QML ##################################################

    # graphWrapper
    graphWrapper = QtCore.Property(QtCore.QObject, getGraphWrapper, constant=True)

    # current param, view, and selected node
    currentParamNodeChanged = QtCore.Signal()
    currentParamNodeWrapper = QtCore.Property(QtCore.QObject, getCurrentParamNodeWrapper, setCurrentParamNodeWrapper, notify=currentParamNodeChanged)
    currentViewerNodeChanged = QtCore.Signal()
    currentViewerNodeWrapper = QtCore.Property(QtCore.QObject, getCurrentViewerNodeWrapper, setCurrentViewerNodeWrapper, notify=currentViewerNodeChanged)
    #currentSelectedNodeChanged = QtCore.Signal()
    #currentSelectedNodeWrapper = QtCore.Property(QtCore.QObject, getCurrentSelectedNodeWrapper, setCurrentSelectedNodeWrapper, notify=currentSelectedNodeChanged)
    currentSelectedNodeWrapperListChanged = QtCore.Signal()
    # currentSelectedNodeWrapperList = QtCore.Property(QtCore.QObject, getCurrentSelectedNodeWrapperList, constant=True)
    # currentSelectedNodeWrapperIndex = QtCore.Property(QtCore.QObject, getCurrentSelectedNodeWrapperIndex, constant=True)
    currentSelectedNodeNameListChanged = QtCore.Signal()
    currentSelectedNodeNameList = QtCore.Property(QtCore.QObject, getCurrentSelectedNodeNameList, constant=True)
    currentSelectedNodeNameIndex = QtCore.Property(QtCore.QObject, getCurrentSelectedNodeNameIndex, constant=True)

    # tuttle data
    tuttlePlugins = QtCore.Property(QtCore.QObject, getQObjectPluginsIdentifiers, constant=True)
