package tcc.desktop;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.FutureTask;
import java.util.function.Supplier;
import javafx.application.Platform;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

// Apoio das Telas de teste do JavaFX, comum aos casos e às duas montagens.
public final class JavaFX {
    private static boolean iniciada;

    private JavaFX() {}

    private static synchronized void iniciar() {
        if (iniciada) {
            return;
        }
        CompletableFuture<Void> pronta = new CompletableFuture<>();
        Platform.startup(() -> pronta.complete(null));
        pronta.join();
        iniciada = true;
    }

    // Como a thread da interface do navegador: tudo roda na thread do
    // JavaFX, e o teste espera o resultado.
    public static <T> T naTela(Supplier<T> bloco) {
        iniciar();
        FutureTask<T> tarefa = new FutureTask<>(bloco::get);
        Platform.runLater(tarefa);
        try {
            return tarefa.get();
        } catch (InterruptedException | ExecutionException e) {
            throw new RuntimeException(e);
        }
    }

    public static void naTela(Runnable bloco) {
        naTela(() -> {
            bloco.run();
            return null;
        });
    }

    // Mostra a tela numa janela, para que o foco possa ir do campo ao tipo
    // de voo; na plataforma Headless, a janela não aparece. O JavaFX foca o
    // primeiro campo ao abrir a janela, e o navegador não foca nenhum: o foco
    // vai para a raiz, para que nenhum campo saia tocado sem a rotina pedir.
    public static <T extends Parent> T mostrar(Supplier<T> montar) {
        return naTela(() -> {
            T raiz = montar.get();
            Stage janela = new Stage();
            janela.setScene(new Scene(raiz));
            janela.show();
            raiz.requestFocus();
            return raiz;
        });
    }
}
