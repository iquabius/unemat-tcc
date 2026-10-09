import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts

// .formulario button e button:disabled.
Button {
    id: botao

    Layout.fillWidth: true
    padding: 8
    background: Rectangle {
        color: botao.enabled ? "#2e4d24" : "#3a3a3a"
        border.color: "#555"
    }
    contentItem: Text {
        text: botao.text
        font: botao.font
        color: botao.enabled ? "#eee" : "#888"
        horizontalAlignment: Text.AlignHCenter
    }
}
