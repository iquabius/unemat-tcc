package tcc.formulario.swing;

import java.awt.Color;
import java.awt.Component;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Insets;
import java.awt.RenderingHints;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JComponent;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.UIManager;
import javax.swing.border.Border;
import javax.swing.plaf.ColorUIResource;
import javax.swing.plaf.InsetsUIResource;
import javax.swing.plaf.basic.BasicComboBoxUI;

// Aparência do Formulário, fora da tela, como o estilo.css: o Swing não tem
// seletores, então o Estilo percorre os componentes e escolhe pela classe
// (a propriedade "classe", no papel do class do HTML) ou pelo tipo, e
// repinta o campo quando a tela altera a propriedade "invalido" (o
// aria-invalid) ou o habilita e desabilita (o :disabled). Fica fora da
// análise.
final class Estilo {

  // O max-width da coluna na web (24rem).
  private static final int LARGURA = 384;
  private static final Color FUNDO = new Color(0x2b2b2b);
  private static final Color TEXTO = new Color(0xeeeeee);
  private static final Color FUNDO_DA_ENTRADA = new Color(0x3a3a3a);
  private static final Color BORDA = new Color(0x555555);
  private static final Color BORDA_INVALIDA = new Color(0xe05555);
  private static final Color FUNDO_INVALIDO = new Color(0x4a2a2a);
  private static final Color ERRO = new Color(0xff8a8a);
  private static final Color CONFIRMACAO = new Color(0x9fd88a);
  private static final Color FUNDO_DO_BOTAO = new Color(0x2e4d24);
  private static final Color TEXTO_DO_BOTAO_DESABILITADO = new Color(0x888888);
  // O opacity: 0.5 do campo desabilitado, já misturado ao fundo.
  private static final Color BORDA_DESABILITADA = new Color(0x404040);
  private static final Color FUNDO_DESABILITADO = new Color(0x333333);
  private static final Color TEXTO_DESABILITADO = new Color(0x8c8c8c);
  // A cor da dica no Android; a web fica com a do navegador. No campo
  // desabilitado, a mesma cor com o opacity: 0.5, já misturada ao fundo.
  private static final Color DICA = new Color(0x999999);
  private static final Color DICA_DESABILITADA = new Color(0x626262);
  // O font-size de 1rem e o de 0.875rem do erro, sem o negrito do Metal.
  private static final Font FONTE = new Font(Font.SANS_SERIF, Font.PLAIN, 16);
  private static final Font FONTE_DO_ERRO = FONTE.deriveFont(14f);

  private Estilo() {}

  static void aplicar(JComponent raiz) {
    // O que o Metal e o Basic pintam com as cores e medidas do tema: o texto
    // do botão desabilitado e o recuo e a seta do ComboBox.
    UIManager.put(
      "Button.disabledText",
      new ColorUIResource(TEXTO_DO_BOTAO_DESABILITADO)
    );
    UIManager.put("ComboBox.padding", new InsetsUIResource(6, 6, 6, 6));
    for (String cor : new String[] {
      "ComboBox.buttonBackground",
      "ComboBox.buttonShadow",
      "ComboBox.buttonHighlight",
      "ComboBox.background",
    }) {
      UIManager.put(cor, new ColorUIResource(FUNDO_DA_ENTRADA));
    }
    UIManager.put("ComboBox.buttonDarkShadow", new ColorUIResource(TEXTO));
    raiz.setBorder(BorderFactory.createEmptyBorder(16, 16, 16, 16));
    percorrer(raiz);
  }

  // Os filhos antes do pai, para que a altura do rótulo já conte a borda
  // do campo.
  private static void percorrer(Container pai) {
    if (pai instanceof JPanel) {
      pai.setBackground(FUNDO);
    }
    for (Component filho : pai.getComponents()) {
      if (filho instanceof JPanel painel) {
        percorrer(painel);
      }
      if (filho instanceof JComponent componente) {
        estilizar(componente);
      }
    }
  }

  private static void estilizar(JComponent componente) {
    // Coluna alinhada à esquerda, com a largura do max-width da web.
    componente.setAlignmentX(Component.LEFT_ALIGNMENT);
    componente.setForeground(TEXTO);
    componente.setFont(FONTE);
    Object classe = componente.getClientProperty("classe");
    if ("rotulo".equals(classe)) {
      componente.setBorder(BorderFactory.createEmptyBorder(0, 0, 12, 0));
      limitarAltura(componente);
    } else if ("erro".equals(classe)) {
      componente.setForeground(ERRO);
      componente.setFont(FONTE_DO_ERRO);
      componente.setBorder(BorderFactory.createEmptyBorder(0, 0, 12, 0));
    } else if ("confirmacao".equals(classe)) {
      // Quebra entre palavras, na largura da coluna, sobre o fundo.
      JTextArea texto = (JTextArea) componente;
      texto.setForeground(CONFIRMACAO);
      texto.setBorder(BorderFactory.createEmptyBorder(12, 0, 0, 0));
      texto.setLineWrap(true);
      texto.setWrapStyleWord(true);
      texto.setOpaque(false);
      texto.setMaximumSize(new Dimension(LARGURA, Integer.MAX_VALUE));
    } else if (componente instanceof JLabel) {
      componente.setBorder(BorderFactory.createEmptyBorder(0, 0, 4, 0));
    } else if (componente instanceof JTextField campo) {
      campo.setCaretColor(TEXTO);
      campo.setDisabledTextColor(TEXTO_DESABILITADO);
      pintarEntrada(campo);
      campo.addPropertyChangeListener("invalido", e -> pintarEntrada(campo));
      campo.addPropertyChangeListener("enabled", e -> pintarEntrada(campo));
      limitarAltura(campo);
    } else if (componente instanceof JComboBox<?> tipo) {
      // O ComboBox do Metal é um botão com gradiente; o do Basic desenha a
      // opção escolhida sobre o fundo dele.
      tipo.setUI(new BasicComboBoxUI());
      tipo.setFont(FONTE);
      tipo.setForeground(TEXTO);
      tipo.setBackground(FUNDO_DA_ENTRADA);
      tipo.setBorder(BorderFactory.createLineBorder(BORDA));
      limitarAltura(tipo);
    } else if (componente instanceof JButton botao) {
      // Reinstala o Metal no botão, que lê de novo a cor do texto
      // desabilitado.
      botao.updateUI();
      botao.setContentAreaFilled(false);
      botao.setOpaque(true);
      botao.setFocusPainted(false);
      botao.setBorder(
        BorderFactory.createCompoundBorder(
          BorderFactory.createLineBorder(BORDA),
          BorderFactory.createEmptyBorder(8, 8, 8, 8)
        )
      );
      pintarBotao(botao);
      botao.addPropertyChangeListener("enabled", e -> pintarBotao(botao));
      limitarAltura(botao);
    }
  }

  private static void pintarBotao(JButton botao) {
    botao.setBackground(botao.isEnabled() ? FUNDO_DO_BOTAO : FUNDO_DA_ENTRADA);
  }

  // O BoxLayout estica na altura o que não tiver tamanho máximo.
  private static void limitarAltura(JComponent componente) {
    componente.setMaximumSize(
      new Dimension(LARGURA, componente.getPreferredSize().height)
    );
  }

  private static void pintarEntrada(JTextField campo) {
    boolean invalido = Boolean.TRUE.equals(campo.getClientProperty("invalido"));
    boolean habilitado = campo.isEnabled();
    Border borda = BorderFactory.createLineBorder(
      !habilitado ? BORDA_DESABILITADA : invalido ? BORDA_INVALIDA : BORDA
    );
    Border moldura = BorderFactory.createCompoundBorder(
      borda,
      BorderFactory.createEmptyBorder(6, 6, 6, 6)
    );
    Object dica = campo.getClientProperty("dica");
    campo.setBorder(
      dica == null ? moldura : new BordaComDica(moldura, (String) dica)
    );
    campo.setBackground(
      !habilitado
        ? FUNDO_DESABILITADO
        : invalido
          ? FUNDO_INVALIDO
          : FUNDO_DA_ENTRADA
    );
  }

  // Como o ::placeholder: o JTextField não tem dica, e a borda a pinta por
  // cima do campo vazio, onde o texto começaria.
  private static final class BordaComDica implements Border {

    private final Border moldura;
    private final String dica;

    BordaComDica(Border moldura, String dica) {
      this.moldura = moldura;
      this.dica = dica;
    }

    @Override
    public void paintBorder(
      Component componente,
      Graphics grafico,
      int x,
      int y,
      int largura,
      int altura
    ) {
      moldura.paintBorder(componente, grafico, x, y, largura, altura);
      if (!((JTextField) componente).getText().isEmpty()) {
        return;
      }
      Graphics2D texto = (Graphics2D) grafico.create();
      texto.setRenderingHint(
        RenderingHints.KEY_TEXT_ANTIALIASING,
        RenderingHints.VALUE_TEXT_ANTIALIAS_ON
      );
      texto.setColor(componente.isEnabled() ? DICA : DICA_DESABILITADA);
      texto.setFont(componente.getFont());
      FontMetrics medidas = texto.getFontMetrics();
      Insets margens = getBorderInsets(componente);
      int linha = altura - margens.top - margens.bottom;
      texto.drawString(
        dica,
        x + margens.left,
        y +
          margens.top +
          (linha - medidas.getHeight()) / 2 +
          medidas.getAscent()
      );
      texto.dispose();
    }

    @Override
    public Insets getBorderInsets(Component componente) {
      return moldura.getBorderInsets(componente);
    }

    @Override
    public boolean isBorderOpaque() {
      return moldura.isBorderOpaque();
    }
  }
}
