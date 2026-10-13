package tcc.lista.javafx;

import static tcc.lista.DominioKt.comparador;
import static tcc.lista.DominioKt.correspondeABusca;
import static tcc.lista.DominioKt.daCategoria;
import static tcc.lista.DominioKt.formatarPreco;
import static tcc.lista.DominioKt.getCategorias;
import static tcc.lista.DominioKt.getProdutos;
import static tcc.lista.DominioKt.textoDaContagem;

import java.util.Arrays;
import java.util.Comparator;
import java.util.function.Predicate;
import javafx.beans.binding.Bindings;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.collections.transformation.FilteredList;
import javafx.collections.transformation.SortedList;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Control;
import javafx.scene.control.Label;
import javafx.scene.control.ListCell;
import javafx.scene.control.ListView;
import javafx.scene.control.TextField;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.Priority;
import javafx.scene.layout.VBox;
import tcc.lista.Ordem;
import tcc.lista.Produto;

// O catálogo em JavaFX, montado em código como o do Swing. A lista visível é
// derivada do catálogo por duas listas que se atualizam sozinhas: a
// FilteredList, cujo filtro é um binding da busca e da categoria, e a
// SortedList, cuja ordem é um binding da ordem escolhida. (O getProdutos() e
// o getCategorias() são as propriedades produtos e categorias do domínio em
// Kotlin, vistas do Java.)
public class CatalogoDeProdutos extends VBox {
    private final TextField busca = new TextField();
    private final ComboBox<String> categoria = new ComboBox<>(opcoesDeCategoria());
    private final ComboBox<String> ordem = new ComboBox<>(FXCollections.observableArrayList(
            Arrays.stream(Ordem.values()).map(Ordem::getRotulo).toList()));
    private final Label contagem = new Label();
    private final FilteredList<Produto> filtrados = new FilteredList<>(FXCollections.observableList(getProdutos()));
    private final SortedList<Produto> visiveis = new SortedList<>(filtrados);
    private final ListView<Produto> lista = new ListView<>(visiveis);
    private final Label vazio = new Label("Nenhum produto encontrado.");

    public CatalogoDeProdutos() {
        VBox filtros = new VBox(
                rotulo("Buscar", busca),
                rotulo("Categoria", categoria),
                rotulo("Ordenar por", ordem));
        getChildren().addAll(filtros, contagem, lista, vazio);
        VBox.setVgrow(lista, Priority.ALWAYS);
        getStyleClass().add("catalogo");
        filtros.getStyleClass().add("filtros");
        contagem.getStyleClass().add("contagem");
        vazio.getStyleClass().add("vazio");
        lista.setCellFactory(l -> new ItemDeProduto());
        categoria.getSelectionModel().select(0);
        ordem.getSelectionModel().select(0);

        // O filtro e a ordem são valores derivados dos controles, com as
        // dependências listadas depois do cálculo.
        filtrados.predicateProperty().bind(Bindings.<Predicate<Produto>>createObjectBinding(() -> {
            String texto = busca.getText();
            String categoriaEscolhida = categoria();
            return produto -> correspondeABusca(produto, texto) && daCategoria(produto, categoriaEscolhida);
        }, busca.textProperty(), categoria.getSelectionModel().selectedIndexProperty()));
        visiveis.comparatorProperty().bind(Bindings.<Comparator<Produto>>createObjectBinding(
                () -> comparador(Ordem.values()[ordem.getSelectionModel().getSelectedIndex()]),
                ordem.getSelectionModel().selectedIndexProperty()));

        contagem.textProperty().bind(Bindings.createStringBinding(
                () -> textoDaContagem(visiveis.size()), visiveis));
        // Como o hidden: invisível e fora do layout.
        vazio.visibleProperty().bind(Bindings.isEmpty(visiveis));
        vazio.managedProperty().bind(vazio.visibleProperty());
    }

    private static ObservableList<String> opcoesDeCategoria() {
        ObservableList<String> opcoes = FXCollections.observableArrayList("Todas");
        opcoes.addAll(getCategorias());
        return opcoes;
    }

    // Como o <label>: o texto e o controle que ele nomeia.
    private static VBox rotulo(String texto, Control controle) {
        Label rotulo = new Label(texto);
        rotulo.setLabelFor(controle);
        VBox caixa = new VBox(rotulo, controle);
        caixa.getStyleClass().add("rotulo");
        return caixa;
    }

    private String categoria() {
        int posicao = categoria.getSelectionModel().getSelectedIndex();
        return posicao == 0 ? "" : getCategorias().get(posicao - 1);
    }

    // A ListView não monta os itens: a fábrica de células cria poucas células
    // e as reaproveita, e o updateItem preenche cada uma com um produto, no
    // papel do map que monta os <li>.
    static class ItemDeProduto extends ListCell<Produto> {
        private final Label nome = new Label();
        private final Label categoria = new Label();
        private final Label preco = new Label();
        private final BorderPane item = new BorderPane(new VBox(nome, categoria), null, preco, null, null);

        ItemDeProduto() {
            nome.getStyleClass().add("nome");
            categoria.getStyleClass().add("categoria");
            preco.getStyleClass().add("preco");
        }

        @Override
        protected void updateItem(Produto produto, boolean semProduto) {
            super.updateItem(produto, semProduto);
            if (semProduto || produto == null) {
                setGraphic(null);
            } else {
                nome.setText(produto.getNome());
                categoria.setText(produto.getCategoria());
                preco.setText(formatarPreco(produto.getPreco()));
                setGraphic(item);
            }
        }
    }
}
