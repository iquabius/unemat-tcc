import QtQuick
import QtQuick.Layouts

// .formulario: uma coluna de até 384 px, com 12 px entre os itens e 16 px de
// borda.
Item {
    default property alias itens: coluna.data

    implicitWidth: coluna.width + 32
    implicitHeight: coluna.implicitHeight + 32

    ColumnLayout {
        id: coluna
        x: 16
        y: 16
        width: 384
        spacing: 12
    }
}
