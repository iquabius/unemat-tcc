import QtQuick
import QtQuick.Controls.Basic

// O body do estilo.css: fundo, cor e tamanho do texto. Os filhos ficam em
// coluna: o formulário e a confirmação.
ApplicationWindow {
    default property alias conteudo: coluna.data

    visible: true
    width: 416
    height: 560
    color: "#2b2b2b"
    font.pixelSize: 16
    palette.windowText: "#eee"
    palette.text: "#eee"

    Column {
        id: coluna
    }
}
