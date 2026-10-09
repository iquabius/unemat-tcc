package tcc.formulario.swing;

import java.awt.Component;
import java.awt.Container;
import java.awt.event.FocusEvent;
import java.awt.event.FocusListener;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicReference;
import java.util.function.Supplier;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JComponent;
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import tcc.formulario.TipoDeVoo;

// Ações e leituras usadas pelo roteiro, como as funções do
// roteiro-de-teste.js. As Telas do JavaFX têm os mesmos nomes. Acha os campos
// pelo rótulo (setLabelFor), os erros e a confirmação pela classe.
class Tela {
    private final FormularioDeReserva formulario;

    Tela() {
        formulario = naTela(FormularioDeReserva::new);
    }

    // Como a thread da interface do navegador: tudo roda na EDT do Swing.
    private static <T> T naTela(Supplier<T> bloco) {
        AtomicReference<T> resultado = new AtomicReference<>();
        try {
            SwingUtilities.invokeAndWait(() -> resultado.set(bloco.get()));
        } catch (InterruptedException | InvocationTargetException e) {
            throw new RuntimeException(e);
        }
        return resultado.get();
    }

    private static void naTela(Runnable bloco) {
        naTela(() -> {
            bloco.run();
            return null;
        });
    }

    private static List<Component> componentes(Container pai) {
        List<Component> todos = new ArrayList<>();
        for (Component filho : pai.getComponents()) {
            todos.add(filho);
            if (filho instanceof Container container) {
                todos.addAll(componentes(container));
            }
        }
        return todos;
    }

    private Component rotulado(String rotulo) {
        return componentes(formulario).stream()
                .filter(c -> c instanceof JLabel l && rotulo.equals(l.getText()))
                .map(c -> ((JLabel) c).getLabelFor())
                .findFirst()
                .orElseThrow();
    }

    private JTextField campo(Campo campo) {
        return (JTextField) rotulado(campo.rotulo);
    }

    private List<JLabel> daClasse(String classe) {
        return componentes(formulario).stream()
                .filter(c -> c instanceof JLabel l && classe.equals(l.getClientProperty("classe")))
                .map(c -> (JLabel) c)
                .toList();
    }

    private JButton botao() {
        return componentes(formulario).stream()
                .filter(c -> c instanceof JButton b && "Reservar".equals(b.getText()))
                .map(c -> (JButton) c)
                .findFirst()
                .orElseThrow();
    }

    // Como o setter + evento "input" do roteiro: muda o texto sem mudar o foco.
    void digitar(Campo campo, String texto) {
        naTela(() -> campo(campo).setText(texto));
    }

    // Como o blur do roteiro, que dispara o evento em vez de mover o foco: sem
    // janela, o Swing não tem foco para mover.
    void sair(Campo campo) {
        naTela(() -> {
            JTextField alvo = campo(campo);
            FocusEvent evento = new FocusEvent(alvo, FocusEvent.FOCUS_LOST);
            for (FocusListener ouvinte : alvo.getFocusListeners()) {
                ouvinte.focusLost(evento);
            }
        });
    }

    @SuppressWarnings("unchecked")
    void escolherTipo(TipoDeVoo tipo) {
        naTela(() -> ((JComboBox<String>) rotulado("Tipo de voo")).setSelectedIndex(tipo.ordinal()));
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
        return naTela(() -> Boolean.TRUE.equals(campo(campo).getClientProperty("invalido")));
    }

    // Mensagens de erro visíveis, de cima para baixo.
    List<String> erros() {
        return naTela(() -> daClasse("erro").stream().filter(JComponent::isVisible).map(JLabel::getText).toList());
    }

    String confirmacao() {
        return naTela(() -> daClasse("confirmacao").get(0).getText());
    }
}
