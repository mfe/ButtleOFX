import Qt 4.7

Rectangle {
    id: graph
    width: 850
    height: 350
    gradient: Gradient {
        GradientStop { position: 0.0; color: "black" }
        GradientStop { position: 0.1; color: "#212121" }
    }

    Item {
        id: nodes
        focus: true
        Repeater {
            model : nodeListModel
            Node {}
        }
    }

    Tools {}

}
