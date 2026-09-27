import { Component, resource, signal } from '@angular/core';
import {
  ESPERA_MS,
  MENSAGENS,
  MINIMO_DE_LETRAS,
  buscarCidades,
  rotulo,
  type Cidade,
} from '../../../dominio';

@Component({
  selector: 'app-busca',
  template: `
    <main class="busca">
      <label>
        Cidade de destino
        <input
          name="destino"
          autocomplete="off"
          placeholder="Digite ao menos 2 letras"
          [value]="texto()"
          (input)="texto.set($event.target.value); agendarBusca($event.target.value)"
          (keydown.escape)="cancelar()"
        />
      </label>
      @if (mensagem(); as m) {
        <p class="situacao" role="status">{{ m }}</p>
      }
      @if (sugestoes().length > 0) {
        <ul class="sugestoes">
          @for (cidade of sugestoes(); track cidade) {
            <li>
              <button type="button" (click)="escolher(cidade)">{{ rotulo(cidade) }}</button>
            </li>
          }
        </ul>
      }
      @if (escolha(); as e) {
        <p class="escolha">Destino: {{ e }}</p>
      }
    </main>
  `,
})
export class BuscaDeDestino {
  protected readonly rotulo = rotulo;

  protected readonly texto = signal('');
  // Termo da última busca. Um signal só notifica quando o valor muda, então
  // um termo repetido não dispara nova requisição.
  private readonly termo = signal('');
  private readonly aberta = signal(false);
  protected readonly escolha = signal<string | null>(null);
  private espera: number | undefined;

  // O recurso refaz a requisição quando o termo muda, expõe isLoading e
  // error, e descarta a resposta de uma requisição que já foi substituída.
  private readonly cidades = resource({
    params: () => (this.termo().length >= MINIMO_DE_LETRAS ? this.termo() : undefined),
    loader: ({ params, abortSignal }) => buscarCidades(params, abortSignal),
  });

  protected agendarBusca(valor: string) {
    clearTimeout(this.espera);
    this.espera = window.setTimeout(() => {
      const novo = valor.trim();
      if (novo === this.termo()) return;
      // Aborta a requisição anterior, como o controlador.abort() do Solid. O
      // resource não tem abort(): é o set() que aborta o loader em andamento,
      // e o valor gravado não importa, por isso undefined, o de "sem
      // resposta". Sem isso, um termo curto deixaria a requisição seguir:
      // com params undefined, o resource só descarta a resposta.
      this.cidades.set(undefined);
      this.aberta.set(true);
      this.termo.set(novo);
    }, ESPERA_MS);
  }

  protected cancelar() {
    clearTimeout(this.espera);
    // Aborta a requisição em andamento pelo set(), como em agendarBusca.
    this.cidades.set(undefined);
    this.aberta.set(false);
  }

  protected escolher(cidade: Cidade) {
    this.cancelar();
    // Muda o texto sem agendar busca: nenhuma busca nova.
    this.texto.set(rotulo(cidade));
    this.escolha.set(rotulo(cidade));
  }

  private visivel() {
    return this.aberta() && this.termo().length >= MINIMO_DE_LETRAS;
  }

  protected mensagem() {
    if (!this.visivel()) return null;
    if (this.cidades.isLoading()) return MENSAGENS.buscando;
    if (this.cidades.error()) return MENSAGENS.falha;
    return this.cidades.value()?.length === 0 ? MENSAGENS.nenhuma : null;
  }

  protected sugestoes() {
    return this.visivel() && !this.cidades.isLoading() && !this.cidades.error()
      ? (this.cidades.value() ?? [])
      : [];
  }
}
