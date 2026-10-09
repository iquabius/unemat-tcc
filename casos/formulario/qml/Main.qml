import QtQuick
import Formulario

// A tela do Formulário. Cada valor derivado é um property binding: o motor da
// QML anota as propriedades que a expressão lê e a reavalia quando uma delas
// muda, como o createMemo do Solid. A aparência fica nos componentes de
// estilo/ (Janela, Entrada, Erro...), como o estilo.css.
Janela {
    id: tela
    title: "Formulário com validação"

    // Os textos dos campos são o estado: os erros os leem direto.
    readonly property bool idaEVolta: tipo.currentValue === Dominio.IdaEVolta
    readonly property var erroNome: Dominio.erroDoNome(nome.text)
    readonly property var erroEmail: Dominio.erroDoEmail(email.text)
    readonly property var erroIda: Dominio.erroDaData(ida.text)
    readonly property var erroVolta: idaEVolta ? Dominio.erroDaData(volta.text) : null
    readonly property var erroOrdem: idaEVolta ? Dominio.erroDaOrdem(ida.text, volta.text) : null
    readonly property bool temErro: [erroNome, erroEmail, erroIda, erroVolta, erroOrdem].some(Boolean)
    property string confirmacao: ""

    Formulario {
        Rotulo {
            texto: "Nome do passageiro"
            Entrada {
                id: nome
                // Tocado: perdeu o foco uma vez. Cada campo guarda o seu.
                property bool tocado: false
                readonly property var erro: tocado ? tela.erroNome : null
                onActiveFocusChanged: if (!activeFocus) tocado = true
                invalida: erro !== null
            }
        }
        Erro { text: nome.erro ?? ""; visible: nome.erro !== null }

        Rotulo {
            texto: "E-mail"
            Entrada {
                id: email
                property bool tocado: false
                readonly property var erro: tocado ? tela.erroEmail : null
                onActiveFocusChanged: if (!activeFocus) tocado = true
                invalida: erro !== null
                inputMethodHints: Qt.ImhEmailCharactersOnly
            }
        }
        Erro { text: email.erro ?? ""; visible: email.erro !== null }

        Rotulo {
            texto: "Tipo de voo"
            Selecao {
                id: tipo
                textRole: "texto"
                valueRole: "valor"
                model: [
                    { valor: Dominio.Ida, texto: "Só ida" },
                    { valor: Dominio.IdaEVolta, texto: "Ida e volta" },
                ]
            }
        }

        Rotulo {
            texto: "Data de ida"
            Entrada {
                id: ida
                property bool tocado: false
                readonly property var erro: tocado ? tela.erroIda : null
                onActiveFocusChanged: if (!activeFocus) tocado = true
                invalida: erro !== null
                text: Dominio.hoje()
                placeholderText: "DD/MM/AAAA"
            }
        }
        Erro { text: ida.erro ?? ""; visible: ida.erro !== null }

        Rotulo {
            texto: "Data de volta"
            Entrada {
                id: volta
                property bool tocado: false
                // Como o ?? da web: o erro da própria data, senão o da ordem.
                readonly property var erro: (tocado ? tela.erroVolta : null)
                    ?? (ida.tocado || tocado ? tela.erroOrdem : null)
                onActiveFocusChanged: if (!activeFocus) tocado = true
                invalida: erro !== null
                enabled: tela.idaEVolta
                text: Dominio.hoje()
                placeholderText: "DD/MM/AAAA"
            }
        }
        Erro { text: volta.erro ?? ""; visible: volta.erro !== null }

        Botao {
            text: "Reservar"
            enabled: !tela.temErro
            onClicked: tela.confirmacao = Dominio.mensagemDeConfirmacao({
                nome: nome.text,
                email: email.text,
                tipo: tipo.currentValue,
                ida: ida.text,
                volta: volta.text,
            })
        }
    }
    Confirmacao { text: tela.confirmacao }
}
