package tcc.formulario.swing;

import static org.junit.Assert.assertTrue;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import org.junit.Rule;
import org.junit.Test;
import tcc.formulario.DataFixa;
import tcc.formulario.TipoDeVoo;

// As 19 verificações de casos/formulario/roteiro-de-teste.js, na mesma ordem
// e com os mesmos nomes. Falha listando todas as que não passaram.
public class RoteiroTest {
    @Rule
    public final DataFixa dataFixa = new DataFixa();

    private final List<String> falhas = new ArrayList<>();

    private void conferir(String nome, Object obtido, Object esperado) {
        if (!Objects.equals(obtido, esperado)) {
            falhas.add(nome + ": obtido " + obtido + ", esperado " + esperado);
        }
    }

    @Test
    public void roteiro() {
        Tela tela = new Tela();
        String nome = "Informe o nome do passageiro.";
        String email = "Informe um e-mail válido.";
        String data = "Use uma data válida no formato DD/MM/AAAA.";
        String ordem = "A volta não pode ser antes da ida.";

        conferir("1 botão começa desabilitado", tela.botaoHabilitado(), false);
        conferir("1 nenhum erro visível", tela.erros(), List.of());
        conferir("1 datas começam hoje", List.of(tela.valor(Campo.IDA), tela.valor(Campo.VOLTA)), List.of("26/09/2026", "26/09/2026"));
        conferir("1 volta começa desabilitada", tela.habilitado(Campo.VOLTA), false);

        tela.sair(Campo.NOME);
        conferir("2 nome tocado e vazio", List.of(tela.erros(), tela.invalido(Campo.NOME)), List.of(List.of(nome), true));
        tela.digitar(Campo.NOME, "Maria");
        conferir("3 nome preenchido", tela.erros(), List.of());

        tela.digitar(Campo.EMAIL, "maria@");
        conferir("4 e-mail inválido antes de tocar", tela.erros(), List.of());
        tela.sair(Campo.EMAIL);
        conferir("4 e-mail inválido depois de tocar", tela.erros(), List.of(email));
        tela.digitar(Campo.EMAIL, "maria@exemplo.com");
        conferir("4 e-mail corrigido", tela.erros(), List.of());
        conferir("5 botão habilitado (só ida)", tela.botaoHabilitado(), true);

        tela.digitar(Campo.IDA, "31/02/2026");
        tela.sair(Campo.IDA);
        conferir("6 data inexistente", List.of(tela.erros(), tela.botaoHabilitado()), List.of(List.of(data), false));
        tela.digitar(Campo.IDA, "10/10/2099");
        conferir("6 data corrigida", List.of(tela.erros(), tela.botaoHabilitado()), List.of(List.of(), true));

        tela.escolherTipo(TipoDeVoo.IDA_E_VOLTA);
        conferir("7 volta habilitada", tela.habilitado(Campo.VOLTA), true);
        conferir("7 volta antes da ida", List.of(tela.erros(), tela.botaoHabilitado()), List.of(List.of(ordem), false));
        tela.digitar(Campo.VOLTA, "1/1/2100");
        tela.sair(Campo.VOLTA);
        conferir("8 volta mal formatada", List.of(tela.erros(), tela.botaoHabilitado()), List.of(List.of(data), false));
        tela.digitar(Campo.VOLTA, "15/10/2099");
        conferir("8 volta corrigida", List.of(tela.erros(), tela.botaoHabilitado()), List.of(List.of(), true));

        tela.reservar();
        conferir(
                "9 confirmação de ida e volta",
                tela.confirmacao(),
                "Voo de ida e volta reservado para Maria: ida em 10/10/2099 e volta em 15/10/2099. "
                        + "A confirmação vai para maria@exemplo.com.");

        tela.digitar(Campo.VOLTA, "xx");
        tela.escolherTipo(TipoDeVoo.IDA);
        conferir(
                "10 volta desabilitada não conta",
                List.of(tela.habilitado(Campo.VOLTA), tela.erros(), tela.botaoHabilitado()),
                List.of(false, List.of(), true));
        tela.reservar();
        conferir(
                "10 confirmação só de ida",
                tela.confirmacao(),
                "Voo só de ida reservado para Maria em 10/10/2099. A confirmação vai para maria@exemplo.com.");

        assertTrue(String.join("\n", falhas), falhas.isEmpty());
    }
}
