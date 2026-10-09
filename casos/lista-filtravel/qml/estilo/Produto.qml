import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts

// .produtos li: nome e categoria à esquerda, preço à direita, nas duas linhas.
Rectangle {
    id: produto

    property alias nome: nome.text
    property alias categoria: categoria.text
    property alias preco: preco.text

    width: ListView.view.width
    implicitHeight: grade.implicitHeight + 16
    color: "#333"

    GridLayout {
        id: grade
        x: 8
        y: 8
        width: produto.width - 16
        columns: 2
        columnSpacing: 16
        rowSpacing: 0

        Label {
            id: nome
            Layout.fillWidth: true
        }
        Label {
            id: preco
            Layout.rowSpan: 2
            color: "#9fd88a"
        }
        Label {
            id: categoria
            color: "#999"
            font.pixelSize: 14
        }
    }
}
