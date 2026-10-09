import QtQuick
import QtQuick.Layouts

// .produtos: os itens separados por uma linha de 1 px, sobre o fundo #444.
ListView {
    Layout.fillWidth: true
    Layout.fillHeight: true
    clip: true
    spacing: 1

    Rectangle {
        z: -1
        anchors.fill: parent
        color: "#444"
    }
}
