package tcc.formulario.swing;

import org.junit.Rule;
import org.junit.Test;
import tcc.formulario.DataFixa;
import tcc.formulario.TipoDeViagem;

// Mesmas cenas de implementacoes/formulario/cenas.mts. Cada cena cria a sua
// Tela dentro do teste, depois que a DataFixa fixa "hoje".
public class CenasTest {

  @Rule
  public final DataFixa dataFixa = new DataFixa();

  @Test
  public void inicial() {
    new Tela().capturar("inicial");
  }

  // Erros visíveis: nome tocado e vazio, e-mail mal formatado, volta antes da
  // ida.
  @Test
  public void erros() {
    Tela tela = new Tela();
    tela.focar(Campo.NOME);
    tela.preencher(Campo.EMAIL, "maria@");
    tela.escolherTipo(TipoDeViagem.IDA_E_VOLTA);
    tela.preencher(Campo.VOLTA, "01/09/2026");
    tela.focar(Campo.NOME);
    tela.capturar("erros");
  }

  @Test
  public void comprado() {
    Tela tela = new Tela();
    tela.preencher(Campo.NOME, "Maria");
    tela.preencher(Campo.EMAIL, "maria@exemplo.com");
    tela.escolherTipo(TipoDeViagem.IDA_E_VOLTA);
    tela.preencher(Campo.IDA, "10/10/2026");
    tela.preencher(Campo.VOLTA, "15/10/2026");
    tela.comprar();
    tela.capturar("comprado");
  }
}
