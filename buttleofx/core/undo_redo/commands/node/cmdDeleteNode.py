# undo_redo
from buttleofx.core.undo_redo.manageTools import UndoableCommand
# core
from buttleofx.core.graph.node import Node


class CmdDeleteNode(UndoableCommand):
    """
        Command that deletes a node.
        Attributes :
        - graphTarget : the graph in which the node will be deleted.
        - node : we save the node's data because we will need it for the redo
        - connections : list of the connections of the node, based on all the connections. We just keep the connections concerning our node.
    """

    def __init__(self, graphTarget, node):
        self._graphTarget = graphTarget
        self._node = node
        self._connections = [connection for connection in self._graphTarget.getConnections() if (connection.getClipOut().getNodeName() == node.getName() or connection.getClipIn().getNodeName() == node.getName())]

    def undoCmd(self):
        """
            Undo the suppression of the node <=> recreate the node.
        """
        # we recreate the node
        self._graphTarget.getNodes().append(self._node)
        # we recreate all the connections
        for connection in self._connections:
            tuttleNodeSource = self._graphTarget.getNode(connection.getClipOut().getNodeName()).getTuttleNode()
            tuttleNodeOutput = self._graphTarget.getNode(connection.getClipIn().getNodeName()).getTuttleNode()
            tuttleConnection = self._graphTarget.getGraphTuttle().connect(tuttleNodeSource, tuttleNodeOutput)
            connection.setTuttleConnection(tuttleConnection)
            self._graphTarget.getConnections().append(connection)

        self._graphTarget.nodesChanged()
        self._graphTarget.connectionsChanged()

    def redoCmd(self):
        """
            Redo the suppression of the node.
        """
        self.doCmd()

    def doCmd(self):
        """
            Delete a node.
        """
        # Delete the tuttle connections
        self._graphTarget.getGraphTuttle().unconnect(self._node.getTuttleNode())

        # Delete the buttle conenctions
        self._graphTarget.deleteNodeConnections(self._node.getName())

        # Delete the node
        self._graphTarget.getNodes().remove(self._node)

        # Emit signals
        self._graphTarget.nodesChanged()
        self._graphTarget.connectionsChanged()