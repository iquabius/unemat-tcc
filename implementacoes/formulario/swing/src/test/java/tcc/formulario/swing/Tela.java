package tcc.formulario.swing;

import static tcc.desktop.Swing.componentes;
import static tcc.desktop.Swing.naTela;

import java.awt.Component;
import java.awt.event.FocusEvent;
import java.awt.event.FocusListener;
import java.util.List;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JComponent;
import javax.swing.JLabel;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import tcc.desktop.Swing;
import tcc.formulario.TipoDeVoo;

// Ações e leituras usadas pelas cenas e pelo teste, como as funções do
// teste-de-conformidade.js. A Tela do JavaFX tem os mesmos nomes. Acha os
// campos pelo rótulo (setLabelFor), os erros e a confirmação pela classe.
class Tela {

  private final FormularioDeReserva formulario;
  // Sem janela, o Swing não tem foco: o campo focado fica anotado aqui.
  private Campo focado;

  // Como o Main: a tela com o Estilo, que as cenas capturam.
  Tela() {
    formulario = naTela(() -> {
      FormularioDeReserva tela = new FormularioDeReserva();
      Estilo.aplicar(tela);
      return tela;
    });
  }

  private Component rotulado(String rotulo) {
    return componentes(formulario)
      .stream()
      .filter(c -> c instanceof JLabel l && rotulo.equals(l.getText()))
      .map(c -> ((JLabel) c).getLabelFor())
      .findFirst()
      .orElseThrow();
  }

  private JTextField campo(Campo campo) {
    return (JTextField) rotulado(campo.rotulo);
  }

  // Os componentes do tipo dado com a propriedade "classe" dada, como o
  // querySelectorAll(".classe").
  private <T extends JComponent> List<T> daClasse(
    String classe,
    Class<T> tipo
  ) {
    return componentes(formulario)
      .stream()
      .filter(tipo::isInstance)
      .map(tipo::cast)
      .filter(c -> classe.equals(c.getClientProperty("classe")))
      .toList();
  }

  private JButton botao() {
    return componentes(formulario)
      .stream()
      .filter(c -> c instanceof JButton b && "Reservar".equals(b.getText()))
      .map(c -> (JButton) c)
      .findFirst()
      .orElseThrow();
  }

  // Como o setter + evento "input" da web: altera o texto sem mover o foco.
  void digitar(Campo campo, String texto) {
    naTela(() -> campo(campo).setText(texto));
  }

  // Como o blur da web, que dispara o evento em vez de mover o foco: sem
  // janela, o Swing não tem foco para mover. Todos os listeners de foco do
  // campo recebem o evento, os da tela e os do próprio Swing (o do cursor),
  // como no dispatchEvent da web.
  void sair(Campo campo) {
    naTela(() -> {
      JTextField alvo = campo(campo);
      FocusEvent evento = new FocusEvent(alvo, FocusEvent.FOCUS_LOST);
      for (FocusListener ouvinte : alvo.getFocusListeners()) {
        ouvinte.focusLost(evento);
      }
    });
  }

  // Como o focus() da web: o campo que tinha o foco o perde.
  void focar(Campo campo) {
    if (focado != null && focado != campo) {
      sair(focado);
    }
    focado = campo;
  }

  // Como o fill() do Playwright: foca o campo e escreve.
  void preencher(Campo campo, String texto) {
    focar(campo);
    digitar(campo, texto);
  }

  void capturar(String cena) {
    Swing.capturar(formulario, cena);
  }

  @SuppressWarnings("unchecked")
  void escolherTipo(TipoDeVoo tipo) {
    naTela(() ->
      ((JComboBox<String>) rotulado("Tipo de voo")).setSelectedIndex(
        tipo.ordinal()
      )
    );
  }

  void reservar() {
    naTela(() -> botao().doClick());
  }

  boolean botaoHabilitado() {
    return naTela(() -> botao().isEnabled());
  }

  boolean habilitado(Campo campo) {
    return naTela(() -> campo(campo).isEnabled());
  }

  String valor(Campo campo) {
    return naTela(() -> campo(campo).getText());
  }

  boolean invalido(Campo campo) {
    return naTela(() ->
      Boolean.TRUE.equals(campo(campo).getClientProperty("invalido"))
    );
  }

  // Mensagens de erro visíveis, de cima para baixo.
  List<String> erros() {
    return naTela(() ->
      daClasse("erro", JLabel.class)
        .stream()
        .filter(JComponent::isVisible)
        .map(JLabel::getText)
        .toList()
    );
  }

  String confirmacao() {
    return naTela(() ->
      daClasse("confirmacao", JTextArea.class).get(0).getText()
    );
  }
}
