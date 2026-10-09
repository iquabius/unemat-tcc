#pragma once

// O domínio da Lista visto da QML: o catálogo e as mesmas funções de
// Dominio.h, como propriedades e métodos de um objeto único que a QML chama
// pelo nome Dominio (como o import do dominio.ts). Fica fora da análise, como
// o domínio: só traduz os tipos.

#include "Dominio.h"

#include <QObject>
#include <QVariant>
#include <QtQml/qqmlregistration.h>

// Os produtos chegam à QML como valores com os campos do Produto.
struct ProdutoQml {
    Q_GADGET
    QML_FOREIGN(lista::Produto)
    QML_VALUE_TYPE(produto)
};

class DominioQml : public QObject {
    Q_OBJECT
    QML_NAMED_ELEMENT(Dominio)
    QML_SINGLETON
    // Dominio.Nome, Dominio.MenorPreco e Dominio.MaiorPreco, os valores do
    // enum Ordem.
    QML_EXTENDED_NAMESPACE(lista)
    Q_PROPERTY(QList<lista::Produto> produtos READ produtos CONSTANT)
    Q_PROPERTY(QStringList categorias READ categorias CONSTANT)
    Q_PROPERTY(QVariantList ordens READ ordens CONSTANT)

public:
    QList<lista::Produto> produtos() const { return lista::produtos; }
    QStringList categorias() const { return lista::categorias; }

    // Como o ordens da web: [{ valor, rotulo }].
    QVariantList ordens() const
    {
        QVariantList opcoes;
        for (const auto ordem : lista::ordens)
            opcoes << QVariantMap{{"valor", QVariant::fromValue(ordem)}, {"rotulo", lista::rotulo(ordem)}};
        return opcoes;
    }

    Q_INVOKABLE bool correspondeABusca(const lista::Produto &produto, const QString &busca) const
    {
        return lista::correspondeABusca(produto, busca);
    }
    Q_INVOKABLE bool daCategoria(const lista::Produto &produto, const QString &categoria) const
    {
        return lista::daCategoria(produto, categoria);
    }
    // O comparador(ordem) da web devolve uma função; daqui, a QML recebe o
    // resultado dela para um par de produtos.
    Q_INVOKABLE int comparar(lista::Ordem ordem, const lista::Produto &a, const lista::Produto &b) const
    {
        return lista::comparador(ordem)(a, b);
    }
    Q_INVOKABLE QString formatarPreco(double preco) const { return lista::formatarPreco(preco); }
    Q_INVOKABLE QString textoDaContagem(int visiveis) const { return lista::textoDaContagem(visiveis); }
};
