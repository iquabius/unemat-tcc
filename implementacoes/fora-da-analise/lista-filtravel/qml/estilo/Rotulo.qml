import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts

// .filtros label: o texto e, embaixo, o controle que ele nomeia.
ColumnLayout {
    property alias texto: rotulo.text

    Layout.fillWidth: true
    spacing: 4

    Label {
        id: rotulo
    }
}
