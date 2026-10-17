package tcc.desktop;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.io.UncheckedIOException;
import javax.imageio.ImageIO;

// Grava as capturas das cenas em <destino>/<tecnologia>-<cena>.png, com o
// mesmo esquema de nomes das capturas web e Android, como o
// implementacoes/android/captura/Captura.kt. Destino e tecnologia vêm do
// Gradle (build.gradle.kts do desktop); quem compara com as versionadas é o
// implementacoes/capturar.mts.
public final class Captura {

  // O tamanho da janela do Main de cada tecnologia: a coluna de 384 da web
  // mais as margens de 16. As imagens saem nesse tamanho, na escala da
  // janela, e não na 2 das capturas web e Android: sem janela, o Swing mede
  // o texto na escala 1 e, pintado na 2, corta o fim de cada texto. O JavaFX
  // acompanha, para o par sair na mesma medida.
  public static final int LARGURA = 416;
  public static final int ALTURA = 560;

  private Captura() {}

  public static void gravar(BufferedImage imagem, String cena) {
    String destino = System.getProperty("capturas.destino");
    String tecnologia = System.getProperty("capturas.tecnologia");
    File arquivo = new File(destino, tecnologia + "-" + cena + ".png");
    arquivo.getParentFile().mkdirs();
    try {
      ImageIO.write(imagem, "png", arquivo);
    } catch (IOException e) {
      throw new UncheckedIOException(e);
    }
  }
}
