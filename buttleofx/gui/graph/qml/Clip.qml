import QtQuick 1.1

Rectangle {
    id: clip
    property string port : parent.port

    height: clipSize
    width: clipSize
    color: "#bbbbbb"
    radius: 4

    MouseArea {
        id: clipMouseArea
        anchors.fill: parent
        hoverEnabled: true
        onPressed: {
            color = "red"
            _buttleData.getGraphWrapper().clipPressed(m.nodeModel.name, port, index) // we send all information needed to identify the clip : nodename, port and clip number
        }
        onReleased: {
            color = "#bbbbbb"

            var coordReleased = clipMouseArea.mapToItem(nodeRepeater, mouseX, mouseY)
            console.log("Mouse X  : ", coordReleased.x)
            console.log("Mouse Y  : ", coordReleased.y)
            console.log("Item at : ", nodeRepeater.childAt(coordReleased.x, coordReleased.y))

             //_buttleData.getGraphWrapper().clipReleased(m.nodeModel.name, port, index)
        }
        onEntered: {
            color = "blue"
        }
        onExited: {
            color = "#bbbbbb"
        }

    }
}
