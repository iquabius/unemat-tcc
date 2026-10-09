package tcc.lista.swing;

import static tcc.desktop.Swing.componentes;
import static tcc.desktop.Swing.naTela;
import static tcc.lista.DominioKt.getCategorias;

import java.awt.Component;
import java.awt.Container;
import java.util.List;
import java.util.stream.IntStream;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JTextField;
import javax.swing.ListModel;
import tcc.lista.Ordem;
import tcc.lista.Produto;

// Ações e leituras usadas pelo roteiro, como as funções do
// roteiro-de-teste.js. As Telas do JavaFX têm os mesmos nomes. Acha os
// controles pelo rótulo (setLabelFor) e os textos pela classe.
class Tela {
    private final CatalogoDeProdutos catalogo;

    Tela() {
        catalogo = naTela(CatalogoDeProdutos::new);
    }

    private Component rotulado(String rotulo) {
        return componentes(catalogo).stream()
                .filter(c -> c instanceof JLabel l && rotulo.equals(l.getText()))
                .map(c -> ((JLabel) c).getLabelFor())
                .findFirst()
                .orElseThrow();
    }

    @SuppressWarnings("unchecked")
    private JComboBox<String> selecao(String rotulo) {
        return (JComboBox<String>) rotulado(rotulo);
    }

    private JLabel daClasse(Container pai, String classe) {
        return componentes(pai).stream()
                .filter(c -> c instanceof JLabel l && classe.equals(l.getClientProperty("classe")))
                .map(c -> (JLabel) c)
                .findFirst()
                .orElseThrow();
    }

    // Como o setter + evento "input" do roteiro.
    void buscar(String texto) {
        naTela(() -> ((JTextField) rotulado("Buscar")).setText(texto));
    }

    void escolherCategoria(String categoria) {
        naTela(() -> selecao("Categoria").setSelectedIndex(getCategorias().indexOf(categoria) + 1));
    }

    void escolherOrdem(Ordem ordem) {
        naTela(() -> selecao("Ordenar por").setSelectedIndex(ordem.ordinal()));
    }

    List<String> opcoesDeCategoria() {
        return naTela(() -> {
            JComboBox<String> selecao = selecao("Categoria");
            return IntStream.range(0, selecao.getItemCount()).mapToObj(selecao::getItemAt).toList();
        });
    }

    // Os textos de cada item da lista, na ordem da tela: nome, categoria,
    // preço. Cada item passa pelo renderer, como a JList faz ao desenhá-lo.
    @SuppressWarnings("unchecked")
    private List<List<String>> itens() {
        return naTela(() -> {
            JList<Produto> lista = (JList<Produto>) componentes(catalogo).stream()
                    .filter(c -> c instanceof JList)
                    .findFirst()
                    .orElseThrow();
            ListModel<Produto> modelo = lista.getModel();
            return IntStream.range(0, modelo.getSize()).mapToObj(posicao -> {
                Container item = (Container) lista.getCellRenderer().getListCellRendererComponent(
                        lista, modelo.getElementAt(posicao), posicao, false, false);
                return List.of("nome", "categoria", "preco").stream()
                        .map(classe -> daClasse(item, classe).getText())
                        .toList();
            }).toList();
        });
    }

    List<String> nomes() {
        return itens().stream().map(item -> item.get(0)).toList();
    }

    // Como o texto() do roteiro, que troca o espaço não separável do preço.
    String primeiroPreco() {
        return itens().get(0).get(2).replace(' ', ' ');
    }

    String contagem() {
        return naTela(() -> daClasse(catalogo, "contagem").getText());
    }

    boolean vazio() {
        return naTela(() -> daClasse(catalogo, "vazio").isVisible());
    }
}
