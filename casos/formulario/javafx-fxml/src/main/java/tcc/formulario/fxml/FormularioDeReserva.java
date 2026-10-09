package tcc.formulario.fxml;

import static tcc.formulario.DominioKt.erroDaData;
import static tcc.formulario.DominioKt.erroDaOrdem;
import static tcc.formulario.DominioKt.erroDoEmail;
import static tcc.formulario.DominioKt.erroDoNome;
import static tcc.formulario.DominioKt.hoje;
import static tcc.formulario.DominioKt.mensagemDeConfirmacao;

import java.util.List;
import java.util.Map;
import javafx.beans.binding.Bindings;
import javafx.beans.binding.BooleanBinding;
import javafx.beans.binding.StringBinding;
import javafx.collections.FXCollections;
import javafx.collections.ObservableSet;
import javafx.css.PseudoClass;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import tcc.formulario.Reserva;
import tcc.formulario.TipoDeVoo;

// Controlador do FormularioDeReserva.fxml. O FXMLLoader monta a tela, preenche
// os campos marcados com @FXML pelo fx:id e chama o initialize; dali em diante
// é o mesmo código do JavaFX montado em Java: o estado são as propriedades dos
// controles, e cada erro é um binding que lista as propriedades de que depende.
public class FormularioDeReserva {
    // Como o aria-invalid: o estilo pinta de vermelho o campo com :invalido.
    private static final PseudoClass INVALIDO = PseudoClass.getPseudoClass("invalido");

    @FXML private TextField nome;
    @FXML private TextField email;
    @FXML private ComboBox<String> tipo;
    @FXML private TextField ida;
    @FXML private TextField volta;
    @FXML private Button reservar;
    @FXML private Label confirmacao;
    @FXML private Label mensagemNome;
    @FXML private Label mensagemEmail;
    @FXML private Label mensagemIda;
    @FXML private Label mensagemVolta;

    // O parágrafo de erro de cada campo, como o <p class="erro">.
    private Map<TextField, Label> erros;

    // Campos já tocados (que perderam o foco uma vez): um conjunto observável,
    // do qual os bindings podem depender, como o signal de tocados do Solid.
    private final ObservableSet<TextField> tocados = FXCollections.observableSet();

    @FXML
    private void initialize() {
        erros = Map.of(nome, mensagemNome, email, mensagemEmail, ida, mensagemIda, volta, mensagemVolta);
        ida.setText(hoje());
        volta.setText(hoje());
        tipo.getSelectionModel().select(0);

        // Valores derivados: cada createStringBinding recebe o cálculo e, depois
        // dele, as propriedades que o cálculo lê.
        BooleanBinding idaEVolta = tipo.getSelectionModel().selectedIndexProperty()
                .isEqualTo(TipoDeVoo.IDA_E_VOLTA.ordinal());
        StringBinding erroNome = Bindings.createStringBinding(
                () -> erroDoNome(nome.getText()), nome.textProperty());
        StringBinding erroEmail = Bindings.createStringBinding(
                () -> erroDoEmail(email.getText()), email.textProperty());
        StringBinding erroIda = Bindings.createStringBinding(
                () -> erroDaData(ida.getText()), ida.textProperty());
        StringBinding erroVolta = Bindings.createStringBinding(
                () -> idaEVolta.get() ? erroDaData(volta.getText()) : null, idaEVolta, volta.textProperty());
        StringBinding erroOrdem = Bindings.createStringBinding(
                () -> idaEVolta.get() ? erroDaOrdem(ida.getText(), volta.getText()) : null,
                idaEVolta, ida.textProperty(), volta.textProperty());
        BooleanBinding temErro = erroNome.isNotNull()
                .or(erroEmail.isNotNull())
                .or(erroIda.isNotNull())
                .or(erroVolta.isNotNull())
                .or(erroOrdem.isNotNull());

        // O erro visível de cada campo só aparece depois de tocado.
        mostrarErro(nome, Bindings.createStringBinding(
                () -> tocados.contains(nome) ? erroNome.get() : null, tocados, erroNome));
        mostrarErro(email, Bindings.createStringBinding(
                () -> tocados.contains(email) ? erroEmail.get() : null, tocados, erroEmail));
        mostrarErro(ida, Bindings.createStringBinding(
                () -> tocados.contains(ida) ? erroIda.get() : null, tocados, erroIda));
        // Como o ?? da web: o erro de formato da volta vem antes do de ordem.
        mostrarErro(volta, Bindings.createStringBinding(() -> {
            String erro = tocados.contains(volta) ? erroVolta.get() : null;
            if (erro == null && (tocados.contains(ida) || tocados.contains(volta))) {
                erro = erroOrdem.get();
            }
            return erro;
        }, tocados, erroVolta, erroOrdem));

        volta.disableProperty().bind(idaEVolta.not());
        reservar.disableProperty().bind(temErro);

        // Como o onBlur: o foco é uma propriedade, e o listener marca o campo.
        for (TextField campo : List.of(nome, email, ida, volta)) {
            campo.focusedProperty().addListener((propriedade, antes, agora) -> {
                if (!agora) {
                    tocados.add(campo);
                }
            });
        }
    }

    // Como o onSubmit: a confirmação muda só no clique, não acompanha os campos.
    @FXML
    private void reservar() {
        confirmacao.setText(mensagemDeConfirmacao(new Reserva(
                nome.getText(), email.getText(), tipo(), ida.getText(), volta.getText())));
    }

    private TipoDeVoo tipo() {
        return TipoDeVoo.values()[tipo.getSelectionModel().getSelectedIndex()];
    }

    private void mostrarErro(TextField campo, StringBinding erro) {
        Label paragrafo = erros.get(campo);
        paragrafo.textProperty().bind(erro);
        // Como o hidden: invisível e fora do layout.
        paragrafo.visibleProperty().bind(erro.isNotNull());
        paragrafo.managedProperty().bind(paragrafo.visibleProperty());
        // A pseudoclasse não tem propriedade para ligar: uma assinatura a
        // acompanha, chamada já com o valor atual e depois a cada mudança.
        erro.subscribe(valor -> campo.pseudoClassStateChanged(INVALIDO, valor != null));
    }
}
