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
            graphArea.connectionIsBeingCreated = true
            color = "red"
            _buttleData.getGraphWrapper().clipPressed(m.nodeModel.name, port, index) // we send all information needed to identify the clip : nodename, port and clip number
        }
        onReleased: {
            graphArea.connectionIsBeingCreated = false
            color = "#bbbbbb"
             //_buttleData.getGraphWrapper().clipReleased(m.nodeModel.name, port, index)
        }
        onEntered: {
            color = "blue"
        }
        onExited: {
            color = "#bbbbbb"
        }

        Connections {
            target: graphArea
            onConnectionIsBeingCreatedChanged: {
                if(!connectionIsBeingCreated)
                {
                    console.log("End of creating connection")
                    console.log("MouseArea containsMouse ? ", clipMouseArea.containsMouse)
                }

                if ((connectionIsBeingCreated==false) && (parent.containsMouse)) {
                    console.log("clip contains mouse");
                    _buttleData.getGraphWrapper().clipReleased(m.nodeModel.name, port, index);
                }
            }
        }
    }
}
