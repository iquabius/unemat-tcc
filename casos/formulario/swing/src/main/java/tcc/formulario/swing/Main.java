package tcc.formulario.swing;

import javax.swing.JFrame;
import javax.swing.SwingUtilities;

// Abre a janela com o formulário, como o index.html que carrega o script.
public class Main {
    public static void main(String[] argumentos) {
        // Como no navegador, a tela é montada na thread da interface (a EDT).
        SwingUtilities.invokeLater(() -> {
            FormularioDeReserva formulario = new FormularioDeReserva();
            Estilo.aplicar(formulario);
            JFrame janela = new JFrame("Formulário com validação");
            janela.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            janela.setContentPane(formulario);
            // O tamanho da tela das capturas do Android: a coluna de 384 da web
            // mais as margens de 16.
            janela.setSize(416, 560);
            janela.setVisible(true);
        });
    }
}
