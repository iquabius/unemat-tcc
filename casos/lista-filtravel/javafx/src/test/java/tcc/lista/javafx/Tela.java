package tcc.lista.javafx;

import static tcc.lista.DominioKt.getCategorias;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.FutureTask;
import java.util.function.Supplier;
import java.util.stream.IntStream;
import javafx.application.Platform;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Label;
import javafx.scene.control.ListCell;
import javafx.scene.control.ListView;
import javafx.scene.control.TextField;
import javafx.stage.Stage;
import tcc.lista.Ordem;
import tcc.lista.Produto;

// Ações e leituras usadas pelo roteiro, como as funções do
// roteiro-de-teste.js. As Telas do Swing e do JavaFX com FXML têm os mesmos
// nomes. Acha os controles pelo rótulo (setLabelFor) e os textos pela classe
// de estilo.
class Tela {
    private final Parent catalogo;

    Tela() {
        iniciarPlataforma();
        catalogo = naTela(() -> {
            CatalogoDeProdutos raiz = new CatalogoDeProdutos();
            Stage janela = new Stage();
            janela.setScene(new Scene(raiz, 480, 720));
            janela.show();
            return raiz;
        });
    }

    private static void iniciarPlataforma() {
        CompletableFuture<Void> pronta = new CompletableFuture<>();
        try {
            Platform.startup(() -> pronta.complete(null));
            pronta.join();
        } catch (IllegalStateException jaIniciada) {
            // Outro teste da mesma JVM já iniciou o JavaFX.
        }
    }

    // Como a thread da interface do navegador: tudo roda na thread do JavaFX.
    private static <T> T naTela(Supplier<T> bloco) {
        FutureTask<T> tarefa = new FutureTask<>(bloco::get);
        Platform.runLater(tarefa);
        try {
            return tarefa.get();
        } catch (InterruptedException | ExecutionException e) {
            throw new RuntimeException(e);
        }
    }

    private static void naTela(Runnable bloco) {
        naTela(() -> {
            bloco.run();
            return null;
        });
    }

    private Node rotulado(String rotulo) {
        return catalogo.lookupAll(".label").stream()
                .filter(n -> n instanceof Label l && rotulo.equals(l.getText()))
                .map(n -> ((Label) n).getLabelFor())
                .findFirst()
                .orElseThrow();
    }

    @SuppressWarnings("unchecked")
    private ComboBox<String> selecao(String rotulo) {
        return (ComboBox<String>) rotulado(rotulo);
    }

    private static Label daClasse(Node pai, String classe) {
        return (Label) pai.lookup("." + classe);
    }

    // Como o setter + evento "input" do roteiro.
    void buscar(String texto) {
        naTela(() -> ((TextField) rotulado("Buscar")).setText(texto));
    }

    void escolherCategoria(String categoria) {
        naTela(() -> selecao("Categoria").getSelectionModel().select(getCategorias().indexOf(categoria) + 1));
    }

    void escolherOrdem(Ordem ordem) {
        naTela(() -> selecao("Ordenar por").getSelectionModel().select(ordem.ordinal()));
    }

    List<String> opcoesDeCategoria() {
        return naTela(() -> List.copyOf(selecao("Categoria").getItems()));
    }

    // Os textos de cada item da lista, na ordem da tela: nome, categoria,
    // preço. Cada item passa por uma célula da fábrica, como a ListView faz ao
    // desenhá-lo; a ListView só cria as células que cabem na janela.
    @SuppressWarnings("unchecked")
    private List<List<String>> itens() {
        return naTela(() -> {
            // A lista de produtos, e não a das opções de um ComboBox.
            ListView<Produto> lista = (ListView<Produto>) catalogo.getChildrenUnmodifiable().stream()
                    .filter(n -> n instanceof ListView)
                    .findFirst()
                    .orElseThrow();
            return IntStream.range(0, lista.getItems().size()).mapToObj(posicao -> {
                ListCell<Produto> celula = lista.getCellFactory().call(lista);
                celula.updateListView(lista);
                celula.updateIndex(posicao);
                return List.of("nome", "categoria", "preco").stream()
                        .map(classe -> daClasse(celula.getGraphic(), classe).getText())
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
