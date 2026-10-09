package tcc.formulario.javafx;

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
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Control;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.VBox;
import tcc.formulario.Reserva;
import tcc.formulario.TipoDeVoo;

// O formulário de reserva em JavaFX, montado em código como o do Swing. O
// estado são as propriedades dos próprios controles (textProperty), e cada
// erro é um binding que lista as propriedades de que depende: muda sozinho
// quando uma delas muda, como o createMemo do Solid, mas com as dependências
// escritas à mão.
public class FormularioDeReserva extends VBox {
    // Como o aria-invalid: o estilo pinta de vermelho o campo com :invalido.
    private static final PseudoClass INVALIDO = PseudoClass.getPseudoClass("invalido");

    private final TextField nome = new TextField();
    private final TextField email = new TextField();
    // Como o <select>: a posição da opção é a do TipoDeVoo.
    private final ComboBox<String> tipo = new ComboBox<>(FXCollections.observableArrayList("Só ida", "Ida e volta"));
    private final TextField ida = new TextField(hoje());
    private final TextField volta = new TextField(hoje());
    private final Button reservar = new Button("Reservar");
    private final Label confirmacao = new Label();

    // O parágrafo de erro de cada campo, como o <p class="erro">.
    private final Map<TextField, Label> erros = Map.of(
            nome, erro(), email, erro(), ida, erro(), volta, erro());

    // Campos já tocados (que perderam o foco uma vez): um conjunto observável,
    // do qual os bindings podem depender, como o signal de tocados do Solid.
    private final ObservableSet<TextField> tocados = FXCollections.observableSet();

    public FormularioDeReserva() {
        getChildren().addAll(
                rotulo("Nome do passageiro", nome),
                erros.get(nome),
                rotulo("E-mail", email),
                erros.get(email),
                rotulo("Tipo de voo", tipo),
                rotulo("Data de ida", ida),
                erros.get(ida),
                rotulo("Data de volta", volta),
                erros.get(volta),
                reservar,
                confirmacao);
        getStyleClass().add("formulario");
        confirmacao.getStyleClass().add("confirmacao");
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

        // Como o onSubmit: a confirmação muda só no clique, não acompanha os campos.
        reservar.setOnAction(e -> confirmacao.setText(mensagemDeConfirmacao(new Reserva(
                nome.getText(), email.getText(), tipo(), ida.getText(), volta.getText()))));
    }

    // Como o <label>: o texto e o campo que ele nomeia.
    private static VBox rotulo(String texto, Control campo) {
        Label rotulo = new Label(texto);
        rotulo.setLabelFor(campo);
        VBox caixa = new VBox(rotulo, campo);
        caixa.getStyleClass().add("rotulo");
        return caixa;
    }

    private static Label erro() {
        Label erro = new Label();
        erro.getStyleClass().add("erro");
        return erro;
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
