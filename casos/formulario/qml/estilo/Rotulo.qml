import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts

// .formulario label: o texto e, embaixo, o campo que ele nomeia.
ColumnLayout {
    property alias texto: rotulo.text

    Layout.fillWidth: true
    spacing: 4

    Label {
        id: rotulo
    }
}
