package tcc.lista.javafx;

import static org.junit.Assert.assertTrue;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import org.junit.Test;
import tcc.lista.Ordem;

// As 11 verificações de casos/lista-filtravel/roteiro-de-teste.js, na mesma
// ordem e com os mesmos nomes. Falha listando todas as que não passaram.
public class RoteiroTest {
    private final List<String> falhas = new ArrayList<>();

    private void conferir(String nome, Object obtido, Object esperado) {
        if (!Objects.equals(obtido, esperado)) {
            falhas.add(nome + ": obtido " + obtido + ", esperado " + esperado);
        }
    }

    @Test
    public void roteiro() {
        Tela tela = new Tela();

        conferir("1 contagem inicial", tela.contagem(), "30 de 30 produtos");
        conferir("1 ordem por nome", tela.nomes().subList(0, 3), List.of("Açúcar mascavo 1 kg", "Agenda 2027", "Azeite extravirgem 500 ml"));
        conferir("1 categorias", tela.opcoesDeCategoria(), List.of("Todas", "Casa", "Cozinha", "Eletrônicos", "Mercearia", "Papelaria"));
        conferir("1 sem aviso de vazio", tela.vazio(), false);
        conferir("1 preço formatado", tela.primeiroPreco(), "R$ 12,50");

        tela.buscar("CAFE");
        conferir("2 busca sem acento e em maiúsculas", List.of(tela.contagem(), tela.nomes()), List.of("2 de 30 produtos", List.of("Café em grãos 500 g", "Cafeteira italiana")));
        tela.buscar("  cerâmica ");
        conferir("3 busca com acento e espaços", tela.nomes(), List.of("Caneca de cerâmica", "Vaso de cerâmica"));

        tela.buscar("");
        tela.escolherCategoria("Cozinha");
        tela.escolherOrdem(Ordem.MAIOR_PRECO);
        conferir("4 cozinha por maior preço", tela.nomes(), List.of("Chaleira elétrica", "Cafeteira italiana", "Frigideira antiaderente", "Faca do chef", "Tábua de corte", "Caneca de cerâmica"));

        tela.escolherCategoria("");
        tela.escolherOrdem(Ordem.MENOR_PRECO);
        conferir("5 todas por menor preço", List.of(tela.contagem(), tela.nomes().subList(0, 2)), List.of("30 de 30 produtos", List.of("Chá de camomila", "Bloco de notas adesivas")));

        tela.buscar("xyz");
        conferir("6 nenhum resultado", List.of(tela.contagem(), tela.nomes().size(), tela.vazio()), List.of("0 de 30 produtos", 0, true));
        tela.buscar("");
        conferir("7 volta ao catálogo inteiro", List.of(tela.contagem(), tela.vazio()), List.of("30 de 30 produtos", false));

        assertTrue(String.join("\n", falhas), falhas.isEmpty());
    }
}
