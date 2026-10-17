package tcc.desktop;

import static tcc.desktop.Captura.ALTURA;
import static tcc.desktop.Captura.LARGURA;

import java.awt.image.BufferedImage;
import java.net.URL;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.FutureTask;
import java.util.function.Supplier;
import javafx.application.Platform;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.image.PixelReader;
import javafx.scene.image.WritableImage;
import javafx.stage.Stage;

// Apoio das Telas de teste do JavaFX, comum às interfaces.
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

  // Mostra a tela numa janela, como o Main: no mesmo tamanho e com o
  // estilo.css da interface, quando ela tem um. A janela deixa o foco ir de
  // um campo a outro; na plataforma Headless, ela não aparece. O JavaFX foca
  // o primeiro campo ao abrir a janela, e o navegador não foca nenhum: o foco
  // vai para a raiz, para que nenhum campo saia tocado sem o teste pedir.
  public static <T extends Parent> T mostrar(Supplier<T> montar) {
    return naTela(() -> {
      T raiz = montar.get();
      Scene cena = new Scene(raiz, LARGURA, ALTURA);
      URL estilo = JavaFX.class.getResource("/estilo.css");
      if (estilo != null) {
        cena.getStylesheets().add(estilo.toExternalForm());
      }
      // Sem o cursor de texto, que pisca e mudaria a captura a cada
      // execução, como o Playwright, que o esconde nas capturas web.
      cena
        .getStylesheets()
        .add("data:text/css,.text-input{-fx-display-caret:false;}");
      Stage janela = new Stage();
      janela.setScene(cena);
      janela.show();
      raiz.requestFocus();
      return raiz;
    });
  }

  // Grava a tela da janela de raiz pela foto (snapshot) que o JavaFX tira
  // da cena, com o CSS e o layout em dia.
  public static void capturar(Parent raiz, String cena) {
    BufferedImage imagem = naTela(() -> {
      WritableImage foto = raiz.getScene().snapshot(null);
      int largura = (int) foto.getWidth();
      int altura = (int) foto.getHeight();
      PixelReader pixels = foto.getPixelReader();
      BufferedImage copia = new BufferedImage(
        largura,
        altura,
        BufferedImage.TYPE_INT_RGB
      );
      for (int y = 0; y < altura; y++) {
        for (int x = 0; x < largura; x++) {
          copia.setRGB(x, y, pixels.getArgb(x, y));
        }
      }
      return copia;
    });
    Captura.gravar(imagem, cena);
  }
}
