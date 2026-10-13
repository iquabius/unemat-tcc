import QtQuick

// A tela da Lista. A lista visível é um property binding: o motor da QML
// anota o que a expressão lê (o texto da busca, a categoria e a ordem
// escolhidas) e a recalcula quando um deles muda, como o createMemo do Solid.
// A aparência fica nos componentes de estilo/ (Janela, Entrada, Produto...),
// como o estilo.css.
Janela {
    id: tela
    title: "Lista filtrável"

    readonly property var visiveis: Dominio.produtos
        .filter(produto => Dominio.correspondeABusca(produto, busca.text)
            && Dominio.daCategoria(produto, categoria.currentValue))
        .sort((a, b) => Dominio.comparar(ordem.currentValue, a, b))

    Filtros {
        Rotulo {
            texto: "Buscar"
            Entrada {
                id: busca
                placeholderText: "Nome do produto"
            }
        }
        Rotulo {
            texto: "Categoria"
            Selecao {
                id: categoria
                textRole: "texto"
                valueRole: "valor"
                // Categoria vazia é "Todas".
                model: [{ valor: "", texto: "Todas" }]
                    .concat(Dominio.categorias.map(c => ({ valor: c, texto: c })))
            }
        }
        Rotulo {
            texto: "Ordenar por"
            Selecao {
                id: ordem
                textRole: "rotulo"
                valueRole: "valor"
                model: Dominio.ordens
            }
        }
    }

    Contagem { text: Dominio.textoDaContagem(tela.visiveis.length) }

    // Como o <ul> com o map: o ListView monta um Produto por item do modelo
    // e o refaz quando o modelo muda.
    Produtos {
        model: tela.visiveis
        delegate: Produto {
            required property var modelData
            nome: modelData.nome
            categoria: modelData.categoria
            preco: Dominio.formatarPreco(modelData.preco)
        }
    }

    Contagem {
        text: "Nenhum produto encontrado."
        visible: tela.visiveis.length === 0
    }
}
