package tcc.lista.swing;

import java.awt.Color;
import java.awt.Component;
import java.awt.Container;
import java.awt.Dimension;
import javax.swing.BorderFactory;
import javax.swing.JComboBox;
import javax.swing.JComponent;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextField;
import javax.swing.JViewport;

// Aparência da Lista, fora da tela, como o estilo.css: o Swing não tem
// seletores, então o Estilo percorre os componentes e escolhe pela classe
// (a propriedade "classe", no papel do class do HTML) ou pelo tipo. Também
// estiliza o painel que desenha os itens, que não está na árvore. Fica fora
// da análise.
final class Estilo {
    private static final Color FUNDO = new Color(0x2b2b2b);
    private static final Color TEXTO = new Color(0xeeeeee);
    private static final Color FUNDO_DA_ENTRADA = new Color(0x3a3a3a);
    private static final Color BORDA = new Color(0x555555);
    private static final Color APAGADO = new Color(0xaaaaaa);
    private static final Color FUNDO_DO_ITEM = new Color(0x333333);
    private static final Color SEPARADOR = new Color(0x444444);
    private static final Color CATEGORIA = new Color(0x999999);
    private static final Color PRECO = new Color(0x9fd88a);

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
            if (filho instanceof JPanel || filho instanceof JScrollPane || filho instanceof JViewport) {
                percorrer((Container) filho);
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
            componente.setBorder(BorderFactory.createEmptyBorder(0, 0, 8, 0));
            limitarAltura(componente);
        } else if ("contagem".equals(classe) || "vazio".equals(classe)) {
            componente.setForeground(APAGADO);
            componente.setBorder(BorderFactory.createEmptyBorder(4, 0, 12, 0));
        } else if (componente instanceof JLabel) {
            componente.setBorder(BorderFactory.createEmptyBorder(0, 0, 4, 0));
        } else if (componente instanceof JTextField campo) {
            campo.setCaretColor(TEXTO);
            campo.setBackground(FUNDO_DA_ENTRADA);
            campo.setBorder(BorderFactory.createCompoundBorder(
                    BorderFactory.createLineBorder(BORDA), BorderFactory.createEmptyBorder(6, 6, 6, 6)));
            limitarAltura(campo);
        } else if (componente instanceof JComboBox) {
            componente.setBackground(FUNDO_DA_ENTRADA);
            limitarAltura(componente);
        } else if (componente instanceof JList<?> lista) {
            lista.setBackground(SEPARADOR);
            if (lista.getCellRenderer() instanceof JPanel item) {
                estilizarItem(item);
            }
        }
    }

    private static void estilizarItem(JPanel item) {
        item.setBackground(FUNDO_DO_ITEM);
        item.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createMatteBorder(0, 0, 1, 0, SEPARADOR), BorderFactory.createEmptyBorder(8, 8, 8, 8)));
        for (Component filho : item.getComponents()) {
            if (filho instanceof JPanel textos) {
                textos.setOpaque(false);
                for (Component texto : textos.getComponents()) {
                    estilizarTexto((JComponent) texto);
                }
            } else {
                estilizarTexto((JComponent) filho);
            }
        }
    }

    private static void estilizarTexto(JComponent texto) {
        Object classe = texto.getClientProperty("classe");
        texto.setForeground("categoria".equals(classe) ? CATEGORIA : "preco".equals(classe) ? PRECO : TEXTO);
    }

    // O BoxLayout estica na altura o que não tiver tamanho máximo.
    private static void limitarAltura(JComponent componente) {
        componente.setMaximumSize(new Dimension(448, componente.getPreferredSize().height));
    }
}
