import Qt 4.7

Rectangle {
    id: node
    height: 40 + 9*(model.element.nodeNbInput-1)
    width: 110
    x: model.element.nodeXCoord
    y: model.element.nodeYCoord
    z: index
    color: "transparent"
    Rectangle {
        id: nodeBorder
        height: node.height
        width: node.width
        anchors.centerIn: parent
        color: model.element.nodeColor
        opacity: 0.5
        radius: 10
    }
    Rectangle {
        id: nodeRectangle
        anchors.centerIn: parent
        height: node.height - 8
        width: node.width - 8
        color: "#bbbbbb"
        radius: 8
        Text {
            anchors.centerIn: parent
            text: model.element.nodeName
            font.pointSize: 10
            color: "black"
        }
    }
    Column {
        id: nodeInputs
        anchors.horizontalCenter: parent.left
        anchors.top: parent.verticalCenter
        spacing: 2
        property int nbInputs: model.element.nodeNbInput
        Repeater {
            model: nodeInputs.nbInputs
            Rectangle {
                height: 5
                width: 5
                color: "#bbbbbb"
                radius: 2
            }
        }
    }
    Column {
        id: nodeOutputs
        anchors.horizontalCenter: parent.right
        anchors.top: parent.verticalCenter
        spacing: 2
        Repeater {
            model: 1
            Rectangle {
                height: 5
                width: 5
                color: "#bbbbbb"
                radius: 2
                MouseArea {
                    anchors.fill: parent
                }
            }
        }
    }
    states: State {
        name: "selected";
        when: node.focus
        PropertyChanges {
            target: nodeRectangle
            color: "#d9d9d9"
        }
    }
    MouseArea {
        anchors.fill: parent
        drag.target: parent
        drag.axis: Drag.XandYAxis
        onPressed: {
            node.focus = true
            parent.opacity = 0.5
        }
        onReleased: {
            parent.opacity = 1
            model.element.nodeXCoord = parent.x
            model.element.nodeYCoord = parent.y
        }
        onClicked: {
            console.log(model.element.nodeName)
            console.log("Node index : "+index)
            node.focus = true
        }
    }
    Keys.onPressed: {
        if (event.key==Qt.Key_Delete) {
            if (node.focus = true){
                nodeListModel.removeElement(index)
            }
        }
    }
}
