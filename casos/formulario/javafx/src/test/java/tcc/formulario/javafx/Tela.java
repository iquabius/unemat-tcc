package tcc.formulario.javafx;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.FutureTask;
import java.util.function.Supplier;
import javafx.application.Platform;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.stage.Stage;
import tcc.formulario.TipoDeVoo;

// Ações e leituras usadas pelo roteiro, como as funções do
// roteiro-de-teste.js. As Telas do Swing e do JavaFX com FXML têm os mesmos
// nomes. Acha os campos pelo rótulo (setLabelFor), os erros e a confirmação
// pela classe de estilo.
class Tela {
    private final Parent formulario;

    Tela() {
        iniciarPlataforma();
        formulario = naTela(() -> {
            FormularioDeReserva raiz = new FormularioDeReserva();
            // Numa janela, para que o foco possa ir de um campo a outro.
            Stage janela = new Stage();
            janela.setScene(new Scene(raiz, 416, 560));
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
        return formulario.lookupAll(".label").stream()
                .filter(n -> n instanceof Label l && rotulo.equals(l.getText()))
                .map(n -> ((Label) n).getLabelFor())
                .findFirst()
                .orElseThrow();
    }

    private TextField campo(Campo campo) {
        return (TextField) rotulado(campo.rotulo);
    }

    private List<Label> daClasse(String classe) {
        return formulario.lookupAll("." + classe).stream().map(n -> (Label) n).toList();
    }

    private Button botao() {
        return formulario.lookupAll(".button").stream()
                .filter(n -> n instanceof Button b && "Reservar".equals(b.getText()))
                .map(n -> (Button) n)
                .findFirst()
                .orElseThrow();
    }

    // Como o setter + evento "input" do roteiro: muda o texto sem mudar o foco.
    void digitar(Campo campo, String texto) {
        naTela(() -> campo(campo).setText(texto));
    }

    // Como o blur do roteiro: o foco entra no campo e passa para outro.
    void sair(Campo campo) {
        naTela(() -> {
            campo(campo).requestFocus();
            campo(campo == Campo.NOME ? Campo.EMAIL : Campo.NOME).requestFocus();
        });
    }

    @SuppressWarnings("unchecked")
    void escolherTipo(TipoDeVoo tipo) {
        naTela(() -> ((ComboBox<String>) rotulado("Tipo de voo")).getSelectionModel().select(tipo.ordinal()));
    }

    void reservar() {
        naTela(() -> botao().fire());
    }

    boolean botaoHabilitado() {
        return naTela(() -> !botao().isDisabled());
    }

    boolean habilitado(Campo campo) {
        return naTela(() -> !campo(campo).isDisabled());
    }

    String valor(Campo campo) {
        return naTela(() -> campo(campo).getText());
    }

    boolean invalido(Campo campo) {
        return naTela(() -> campo(campo).getPseudoClassStates().stream()
                .anyMatch(p -> p.getPseudoClassName().equals("invalido")));
    }

    // Mensagens de erro visíveis, de cima para baixo.
    List<String> erros() {
        return naTela(() -> daClasse("erro").stream().filter(Node::isVisible).map(Label::getText).toList());
    }

    String confirmacao() {
        return naTela(() -> daClasse("confirmacao").get(0).getText());
    }
}
