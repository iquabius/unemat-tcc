package tcc.formulario.fxml;

import java.io.IOException;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.stage.Stage;

// Abre a janela com o formulário, como o index.html que carrega o script e
// o estilo.css.
public class Main extends Application {
    @Override
    public void start(Stage janela) throws IOException {
        Scene cena = new Scene(FXMLLoader.load(Main.class.getResource("FormularioDeReserva.fxml")), 416, 560);
        cena.getStylesheets().add(Main.class.getResource("/estilo.css").toExternalForm());
        janela.setTitle("Formulário com validação");
        janela.setScene(cena);
        janela.show();
    }

    public static void main(String[] argumentos) {
        launch(argumentos);
    }
}
