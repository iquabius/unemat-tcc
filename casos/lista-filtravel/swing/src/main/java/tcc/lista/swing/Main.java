package tcc.lista.swing;

import javax.swing.JFrame;
import javax.swing.SwingUtilities;

// Abre a janela com o catálogo, como o index.html que carrega o script.
public class Main {
    public static void main(String[] argumentos) {
        // Como no navegador, a tela é montada na thread da interface (a EDT).
        SwingUtilities.invokeLater(() -> {
            CatalogoDeProdutos catalogo = new CatalogoDeProdutos();
            Estilo.aplicar(catalogo);
            JFrame janela = new JFrame("Lista filtrável");
            janela.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            janela.setContentPane(catalogo);
            janela.setSize(480, 720);
            janela.setVisible(true);
        });
    }
}
