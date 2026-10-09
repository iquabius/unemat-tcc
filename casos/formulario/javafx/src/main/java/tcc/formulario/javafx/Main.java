package tcc.formulario.javafx;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.stage.Stage;

// Abre a janela com o formulário, como o index.html que carrega o script e
// o estilo.css.
public class Main extends Application {
    @Override
    public void start(Stage janela) {
        Scene cena = new Scene(new FormularioDeReserva(), 416, 560);
        cena.getStylesheets().add(Main.class.getResource("/estilo.css").toExternalForm());
        janela.setTitle("Formulário com validação");
        janela.setScene(cena);
        janela.show();
    }

    public static void main(String[] argumentos) {
        launch(argumentos);
    }
}
