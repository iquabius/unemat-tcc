import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts

// .formulario input, com o [aria-invalid="true"] na propriedade invalida.
TextField {
    id: entrada

    property bool invalida: false

    Layout.fillWidth: true
    padding: 6
    color: "#eee"
    placeholderTextColor: "#999"
    opacity: enabled ? 1 : 0.5
    background: Rectangle {
        color: entrada.invalida ? "#4a2a2a" : "#3a3a3a"
        border.color: entrada.invalida ? "#e05555" : "#555"
    }
}
