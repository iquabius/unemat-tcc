import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts

// O body e o .catalogo do estilo.css: fundo, cor do texto e uma coluna de
// até 448 px, com 12 px entre os itens e 16 px de borda.
ApplicationWindow {
    default property alias conteudo: coluna.data

    visible: true
    width: 480
    height: 640
    color: "#2b2b2b"
    font.pixelSize: 16
    palette.windowText: "#eee"
    palette.text: "#eee"

    ColumnLayout {
        id: coluna
        x: 16
        y: 16
        width: 448
        height: parent.height - 32
        spacing: 12
    }
}
