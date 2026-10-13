package tcc.formulario.swing;

import static tcc.formulario.DominioKt.erroDaData;
import static tcc.formulario.DominioKt.erroDaOrdem;
import static tcc.formulario.DominioKt.erroDoEmail;
import static tcc.formulario.DominioKt.erroDoNome;
import static tcc.formulario.DominioKt.hoje;
import static tcc.formulario.DominioKt.mensagemDeConfirmacao;

import java.awt.event.FocusAdapter;
import java.awt.event.FocusEvent;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.stream.Stream;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JComponent;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import tcc.formulario.Reserva;
import tcc.formulario.TipoDeVoo;

// O formulário de reserva em Swing, como o MainActivity do Views: os
// componentes e o estado ficam nesta classe, e cada listener revalida tudo.
public class FormularioDeReserva extends JPanel {
    private final JTextField nome = new JTextField();
    private final JTextField email = new JTextField();
    // Como o <select>: a posição da opção é a do TipoDeVoo.
    private final JComboBox<String> tipo = new JComboBox<>(new String[] {"Só ida", "Ida e volta"});
    private final JTextField ida = new JTextField(hoje());
    private final JTextField volta = new JTextField(hoje());
    private final JButton reservar = new JButton("Reservar");
    private final JLabel confirmacao = new JLabel();

    // O parágrafo de erro de cada campo, como o <p class="erro"> do jQuery.
    private final Map<JTextField, JLabel> erros = Map.of(
            nome, erro(), email, erro(), ida, erro(), volta, erro());

    // Campos já tocados (que perderam o foco uma vez), como o Set do jQuery.
    private final Set<JTextField> tocados = new HashSet<>();

    public FormularioDeReserva() {
        setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
        add(rotulo("Nome do passageiro", nome));
        add(erros.get(nome));
        add(rotulo("E-mail", email));
        add(erros.get(email));
        add(rotulo("Tipo de voo", tipo));
        add(rotulo("Data de ida", ida));
        add(erros.get(ida));
        add(rotulo("Data de volta", volta));
        add(erros.get(volta));
        add(reservar);
        add(confirmacao);
        confirmacao.putClientProperty("classe", "confirmacao");
        volta.setEnabled(false);

        // Como .on("input", validar): o DocumentListener avisa as três formas
        // de mudança do texto, e as três revalidam.
        DocumentListener validarAoMudar = new DocumentListener() {
            @Override
            public void insertUpdate(DocumentEvent e) {
                validar();
            }

            @Override
            public void removeUpdate(DocumentEvent e) {
                validar();
            }

            @Override
            public void changedUpdate(DocumentEvent e) {
                validar();
            }
        };
        for (JTextField campo : List.of(nome, email, ida, volta)) {
            campo.getDocument().addDocumentListener(validarAoMudar);
            // Como .on("blur"): marca o campo como tocado.
            campo.addFocusListener(new FocusAdapter() {
                @Override
                public void focusLost(FocusEvent e) {
                    tocados.add(campo);
                    validar();
                }
            });
        }

        // Como .on("change") do <select>.
        tipo.addActionListener(e -> {
            volta.setEnabled(tipo() == TipoDeVoo.IDA_E_VOLTA);
            validar();
        });

        // Como .on("submit"): o botão só fica habilitado sem erros.
        reservar.addActionListener(e -> confirmacao.setText(mensagemDeConfirmacao(
                new Reserva(nome.getText(), email.getText(), tipo(), ida.getText(), volta.getText()))));

        validar();
    }

    // Como o <label>: o texto e o campo que ele nomeia.
    private static JPanel rotulo(String texto, JComponent campo) {
        JLabel rotulo = new JLabel(texto);
        rotulo.setLabelFor(campo);
        JPanel painel = new JPanel();
        painel.setLayout(new BoxLayout(painel, BoxLayout.Y_AXIS));
        painel.add(rotulo);
        painel.add(campo);
        painel.putClientProperty("classe", "rotulo");
        return painel;
    }

    private static JLabel erro() {
        JLabel erro = new JLabel();
        erro.putClientProperty("classe", "erro");
        erro.setVisible(false);
        return erro;
    }

    private TipoDeVoo tipo() {
        return TipoDeVoo.values()[tipo.getSelectedIndex()];
    }

    private void mostrarErro(JTextField campo, String erro) {
        // Como o aria-invalid: o Estilo pinta de vermelho o campo inválido.
        campo.putClientProperty("invalido", erro != null);
        erros.get(campo).setText(erro);
        erros.get(campo).setVisible(erro != null);
    }

    // Revalida o formulário inteiro a cada evento: mostra os erros dos campos
    // já tocados e habilita o botão só se não houver erro nenhum.
    private void validar() {
        boolean idaEVolta = tipo() == TipoDeVoo.IDA_E_VOLTA;
        String erroNome = erroDoNome(nome.getText());
        String erroEmail = erroDoEmail(email.getText());
        String erroIda = erroDaData(ida.getText());
        String erroVolta = idaEVolta ? erroDaData(volta.getText()) : null;
        String erroOrdem = idaEVolta ? erroDaOrdem(ida.getText(), volta.getText()) : null;

        mostrarErro(nome, tocados.contains(nome) ? erroNome : null);
        mostrarErro(email, tocados.contains(email) ? erroEmail : null);
        mostrarErro(ida, tocados.contains(ida) ? erroIda : null);
        // Como o ?? da web: o erro de formato da volta vem antes do de ordem.
        String erroVisivelDaVolta = tocados.contains(volta) ? erroVolta : null;
        if (erroVisivelDaVolta == null && (tocados.contains(ida) || tocados.contains(volta))) {
            erroVisivelDaVolta = erroOrdem;
        }
        mostrarErro(volta, erroVisivelDaVolta);

        boolean temErro = Stream.of(erroNome, erroEmail, erroIda, erroVolta, erroOrdem).anyMatch(Objects::nonNull);
        reservar.setEnabled(!temErro);
    }
}
