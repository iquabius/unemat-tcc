package tcc.lista.fxml;

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
import javafx.collections.transformation.FilteredList;
import javafx.collections.transformation.SortedList;
import javafx.fxml.FXML;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Label;
import javafx.scene.control.ListCell;
import javafx.scene.control.ListView;
import javafx.scene.control.TextField;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.VBox;
import tcc.lista.Ordem;
import tcc.lista.Produto;

// Controlador do CatalogoDeProdutos.fxml. O FXMLLoader monta a tela, preenche
// os campos marcados com @FXML pelo fx:id e chama o initialize; dali em diante
// é o mesmo código do JavaFX montado em Java: a lista visível é derivada do
// catálogo pela FilteredList e pela SortedList, com o filtro e a ordem ligados
// aos controles. (O getProdutos() e o getCategorias() são as propriedades
// produtos e categorias do domínio em Kotlin, vistas do Java.)
public class CatalogoDeProdutos {
    @FXML private TextField busca;
    @FXML private ComboBox<String> categoria;
    @FXML private ComboBox<String> ordem;
    @FXML private Label contagem;
    @FXML private ListView<Produto> lista;
    @FXML private Label vazio;

    private final FilteredList<Produto> filtrados = new FilteredList<>(FXCollections.observableList(getProdutos()));
    private final SortedList<Produto> visiveis = new SortedList<>(filtrados);

    @FXML
    private void initialize() {
        categoria.getItems().add("Todas");
        categoria.getItems().addAll(getCategorias());
        ordem.getItems().setAll(Arrays.stream(Ordem.values()).map(Ordem::getRotulo).toList());
        lista.setItems(visiveis);
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

    private String categoria() {
        int posicao = categoria.getSelectionModel().getSelectedIndex();
        return posicao == 0 ? "" : getCategorias().get(posicao - 1);
    }

    // A ListView não monta os itens: a fábrica de células cria poucas células
    // e as reaproveita, e o updateItem preenche cada uma com um produto, no
    // papel do map que monta os <li>. O FXML não tem como repetir um trecho
    // por item, então a célula é montada em código, como no JavaFX sem FXML.
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
