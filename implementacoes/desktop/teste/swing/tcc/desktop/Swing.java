package tcc.desktop;

import static tcc.desktop.Captura.ALTURA;
import static tcc.desktop.Captura.LARGURA;

import java.awt.Component;
import java.awt.Container;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicReference;
import java.util.function.Supplier;
import javax.swing.JComponent;
import javax.swing.SwingUtilities;

// Apoio das Telas de teste do Swing, comum às interfaces.
public final class Swing {

  private Swing() {}

  // Como a thread da interface do navegador: tudo roda na EDT do Swing, e
  // o teste espera o resultado.
  public static <T> T naTela(Supplier<T> bloco) {
    AtomicReference<T> resultado = new AtomicReference<>();
    try {
      SwingUtilities.invokeAndWait(() -> resultado.set(bloco.get()));
    } catch (InterruptedException | InvocationTargetException e) {
      throw new RuntimeException(e);
    }
    return resultado.get();
  }

  public static void naTela(Runnable bloco) {
    naTela(() -> {
      bloco.run();
      return null;
    });
  }

  // Todos os componentes abaixo de pai, de cima para baixo, como o
  // querySelectorAll.
  public static List<Component> componentes(Container pai) {
    List<Component> todos = new ArrayList<>();
    for (Component filho : pai.getComponents()) {
      todos.add(filho);
      if (filho instanceof Container container) {
        todos.addAll(componentes(container));
      }
    }
    return todos;
  }

  // Grava a tela no tamanho da janela do Main. Sem janela, o Swing não
  // dispõe os componentes sozinho: a função os dispõe, de cima para baixo,
  // e pinta a raiz numa imagem. A segunda passada dá ao texto que quebra
  // linhas a altura da largura que a primeira lhe deu.
  public static void capturar(JComponent raiz, String cena) {
    BufferedImage imagem = naTela(() -> {
      raiz.setSize(LARGURA, ALTURA);
      dispor(raiz);
      dispor(raiz);
      BufferedImage copia = new BufferedImage(
        LARGURA,
        ALTURA,
        BufferedImage.TYPE_INT_RGB
      );
      Graphics2D grafico = copia.createGraphics();
      raiz.paint(grafico);
      grafico.dispose();
      return copia;
    });
    Captura.gravar(imagem, cena);
  }

  private static void dispor(Container pai) {
    pai.invalidate();
    pai.doLayout();
    for (Component filho : pai.getComponents()) {
      if (filho instanceof Container container) {
        dispor(container);
      }
    }
  }
}
