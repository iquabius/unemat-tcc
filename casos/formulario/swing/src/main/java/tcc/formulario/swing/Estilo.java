package tcc.formulario.swing;

import java.awt.Color;
import java.awt.Component;
import java.awt.Container;
import java.awt.Dimension;
import javax.swing.BorderFactory;
import javax.swing.JComboBox;
import javax.swing.JComponent;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.border.Border;

// Aparência do Formulário, fora da tela, como o estilo.css: o Swing não tem
// seletores, então o Estilo percorre os componentes e escolhe pela classe
// (a propriedade "classe", no papel do class do HTML) ou pelo tipo, e
// repinta o campo quando a tela muda a propriedade "invalido" (o
// aria-invalid). Fica fora da análise.
final class Estilo {
    private static final Color FUNDO = new Color(0x2b2b2b);
    private static final Color TEXTO = new Color(0xeeeeee);
    private static final Color FUNDO_DA_ENTRADA = new Color(0x3a3a3a);
    private static final Color BORDA = new Color(0x555555);
    private static final Color BORDA_INVALIDA = new Color(0xe05555);
    private static final Color FUNDO_INVALIDO = new Color(0x4a2a2a);
    private static final Color ERRO = new Color(0xff8a8a);
    private static final Color CONFIRMACAO = new Color(0x9fd88a);

    private Estilo() {}

    static void aplicar(JComponent raiz) {
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
        Object classe = componente.getClientProperty("classe");
        if ("rotulo".equals(classe)) {
            componente.setBorder(BorderFactory.createEmptyBorder(0, 0, 12, 0));
            limitarAltura(componente);
        } else if ("erro".equals(classe)) {
            componente.setForeground(ERRO);
            componente.setBorder(BorderFactory.createEmptyBorder(0, 0, 12, 0));
        } else if ("confirmacao".equals(classe)) {
            componente.setForeground(CONFIRMACAO);
            componente.setBorder(BorderFactory.createEmptyBorder(12, 0, 0, 0));
        } else if (componente instanceof JLabel) {
            componente.setBorder(BorderFactory.createEmptyBorder(0, 0, 4, 0));
        } else if (componente instanceof JTextField campo) {
            campo.setCaretColor(TEXTO);
            pintarEntrada(campo, false);
            campo.addPropertyChangeListener("invalido", e -> pintarEntrada(campo, Boolean.TRUE.equals(e.getNewValue())));
            limitarAltura(campo);
        } else if (componente instanceof JComboBox) {
            componente.setBackground(FUNDO_DA_ENTRADA);
            limitarAltura(componente);
        }
    }

    // O BoxLayout estica na altura o que não tiver tamanho máximo.
    private static void limitarAltura(JComponent componente) {
        componente.setMaximumSize(new Dimension(384, componente.getPreferredSize().height));
    }

    private static void pintarEntrada(JTextField campo, boolean invalido) {
        Border borda = BorderFactory.createLineBorder(invalido ? BORDA_INVALIDA : BORDA);
        campo.setBorder(BorderFactory.createCompoundBorder(borda, BorderFactory.createEmptyBorder(6, 6, 6, 6)));
        campo.setBackground(invalido ? FUNDO_INVALIDO : FUNDO_DA_ENTRADA);
    }
}
