#include "Dominio.h"

#include <QCollator>
#include <QLocale>
#include <algorithm>

namespace lista {

const QList<Produto> produtos = {
    {1, "Café em grãos 500 g", "Mercearia", 39.9},
    {2, "Açúcar mascavo 1 kg", "Mercearia", 12.5},
    {3, "Chá de camomila", "Mercearia", 8.99},
    {4, "Azeite extravirgem 500 ml", "Mercearia", 45},
    {5, "Pão de fermentação natural", "Mercearia", 22},
    {6, "Mel silvestre 300 g", "Mercearia", 27.9},
    {7, "Caneca de cerâmica", "Cozinha", 34.9},
    {8, "Cafeteira italiana", "Cozinha", 129.9},
    {9, "Chaleira elétrica", "Cozinha", 159},
    {10, "Frigideira antiaderente", "Cozinha", 119.9},
    {11, "Faca do chef", "Cozinha", 89.9},
    {12, "Tábua de corte", "Cozinha", 49.9},
    {13, "Fone de ouvido sem fio", "Eletrônicos", 249.9},
    {14, "Mouse sem fio", "Eletrônicos", 79.9},
    {15, "Teclado mecânico", "Eletrônicos", 399},
    {16, "Cabo USB-C 2 m", "Eletrônicos", 29.9},
    {17, "Carregador portátil", "Eletrônicos", 149.9},
    {18, "Caixa de som Bluetooth", "Eletrônicos", 199.9},
    {19, "Caderno pautado", "Papelaria", 24.9},
    {20, "Canetas esferográficas (10 un.)", "Papelaria", 15.9},
    {21, "Agenda 2027", "Papelaria", 54.9},
    {22, "Marca-texto (4 cores)", "Papelaria", 19.9},
    {23, "Bloco de notas adesivas", "Papelaria", 9.9},
    {24, "Estojo escolar", "Papelaria", 32.9},
    {25, "Garrafa térmica 1 L", "Casa", 99.9},
    {26, "Luminária de mesa", "Casa", 139.9},
    {27, "Vela aromática", "Casa", 44.9},
    {28, "Toalha de banho", "Casa", 59.9},
    {29, "Travesseiro de espuma", "Casa", 119},
    {30, "Vaso de cerâmica", "Casa", 69.9},
};

// Como o Intl.Collator e o Intl.NumberFormat da web.
static const QLocale PT_BR(QLocale::Portuguese, QLocale::Brazil);

static int compararTextos(const QString &a, const QString &b)
{
    static const QCollator collator(PT_BR);
    return collator.compare(a, b);
}

const QStringList categorias = [] {
    QStringList nomes;
    for (const auto &produto : produtos)
        if (!nomes.contains(produto.categoria)) nomes << produto.categoria;
    std::ranges::sort(nomes, [](const QString &a, const QString &b) { return compararTextos(a, b) < 0; });
    return nomes;
}();

const QList<Ordem> ordens = {Ordem::Nome, Ordem::MenorPreco, Ordem::MaiorPreco};

QString rotulo(Ordem ordem)
{
    switch (ordem) {
    case Ordem::Nome: return "Nome (A–Z)";
    case Ordem::MenorPreco: return "Menor preço";
    case Ordem::MaiorPreco: return "Maior preço";
    }
    return {};
}

/** Minúsculas e sem acentos, para comparar textos como o usuário espera. */
static QString normalizar(const QString &texto)
{
    QString semAcentos;
    for (const QChar c : texto.normalized(QString::NormalizationForm_D))
        if (c.category() != QChar::Mark_NonSpacing) semAcentos += c;
    return semAcentos.toLower().trimmed();
}

bool correspondeABusca(const Produto &produto, const QString &busca)
{
    return normalizar(produto.nome).contains(normalizar(busca));
}

bool daCategoria(const Produto &produto, const QString &categoria)
{
    return categoria.isEmpty() || produto.categoria == categoria;
}

std::function<int(const Produto &, const Produto &)> comparador(Ordem ordem)
{
    if (ordem == Ordem::Nome)
        return [](const Produto &a, const Produto &b) { return compararTextos(a.nome, b.nome); };
    const int sentido = ordem == Ordem::MenorPreco ? 1 : -1;
    return [sentido](const Produto &a, const Produto &b) {
        if (a.preco != b.preco) return a.preco < b.preco ? -sentido : sentido;
        return compararTextos(a.nome, b.nome);
    };
}

QString formatarPreco(double preco)
{
    return PT_BR.toCurrencyString(preco, "R$", 2);
}

QString textoDaContagem(qsizetype visiveis)
{
    return QStringLiteral("%1 de %2 produtos").arg(visiveis).arg(produtos.size());
}

} // namespace lista
