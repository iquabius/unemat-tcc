import {
  Component,
  DestroyRef,
  Injectable,
  effect,
  inject,
  input,
  signal,
} from "@angular/core";
import {
  COLUNAS,
  MENSAGENS,
  anunciarArquivamento,
  anunciarMovimento,
  carregarQuadro,
  ouvirOutrasAbas,
  podeIr,
  salvarQuadro,
  tarefa,
  textoDaColuna,
  textoDoCabecalho,
  tituloDa,
  type Coluna,
  type EstadoDoQuadro,
} from "../../../dominio";

// O quadro e a situação moram num serviço; o componente Quadro o provê, e
// os componentes de dentro recebem a mesma instância por injeção. Cada
// ponto da tela se atualiza quando o signal que ele lê se altera.
@Injectable()
export class LojaDoQuadro {
  private readonly quadro = signal(carregarQuadro());
  private readonly texto = signal("");
  readonly estado = this.quadro.asReadonly();
  readonly situacao = this.texto.asReadonly();

  constructor() {
    effect(() => salvarQuadro(this.estado()));
    // O serviço vive enquanto o componente que o provê; sem isto, o
    // ouvinte das outras abas continua fora da página.
    inject(DestroyRef).onDestroy(
      ouvirOutrasAbas((quadro) => this.trocar(quadro)),
    );
  }

  // O signal só avisa quando recebe outro valor: cada transição troca o
  // quadro por uma cópia, sem alterar as listas do anterior.
  mover(id: number, de: Coluna, para: Coluna) {
    this.quadro.update((quadro) => ({
      ...quadro,
      [de]: quadro[de].filter((t) => t !== id),
      [para]: [...quadro[para], id],
    }));
    this.texto.set(anunciarMovimento(id, para));
  }

  arquivar(id: number, de: Coluna) {
    this.quadro.update((quadro) => ({
      ...quadro,
      [de]: quadro[de].filter((t) => t !== id),
    }));
    this.texto.set(anunciarArquivamento(id));
  }

  private trocar(quadro: EstadoDoQuadro) {
    this.quadro.set(quadro);
    this.texto.set(MENSAGENS.outraAba);
  }
}

@Component({
  selector: "app-cabecalho",
  template: `
    <header class="cabecalho">
      <strong>Meu quadro</strong>
      <span class="resumo">{{ textoDoCabecalho(loja.estado()) }}</span>
      <p class="situacao" role="status">{{ loja.situacao() }}</p>
    </header>
  `,
})
export class Cabecalho {
  protected readonly loja = inject(LojaDoQuadro);
  protected readonly textoDoCabecalho = textoDoCabecalho;
}

// Cada opção diz se é a escolhida: um [value] no select chegaria antes das
// opções do @for, e a lista ficaria na primeira.
@Component({
  selector: "app-coluna",
  template: `
    <section class="coluna">
      <h2>{{ textoDaColuna(loja.estado(), coluna()) }}</h2>
      @if (loja.estado()[coluna()].length > 0) {
        <ul>
          @for (id of loja.estado()[coluna()]; track id) {
            <li>
              <span class="titulo">{{ tarefa(id).titulo }}</span>
              <select
                attr.aria-label="Coluna de {{ tarefa(id).titulo }}"
                (change)="loja.mover(id, coluna(), $any($event.target).value)"
              >
                @for (para of colunas; track para) {
                  <option
                    [value]="para"
                    [selected]="para === coluna()"
                    [disabled]="!podeIr(loja.estado(), coluna(), para)"
                  >
                    {{ tituloDa(para) }}
                  </option>
                }
              </select>
              <button
                type="button"
                class="arquivar"
                attr.aria-label="Arquivar {{ tarefa(id).titulo }}"
                (click)="loja.arquivar(id, coluna())"
              >
                Arquivar
              </button>
            </li>
          }
        </ul>
      } @else {
        <p class="aviso">{{ MENSAGENS.colunaVazia }}</p>
      }
    </section>
  `,
})
export class ColunaDoQuadro {
  readonly coluna = input.required<Coluna>();
  protected readonly loja = inject(LojaDoQuadro);
  // O template só alcança o que a classe expõe: o domínio entra por aqui.
  protected readonly MENSAGENS = MENSAGENS;
  protected readonly colunas = COLUNAS;
  protected readonly podeIr = podeIr;
  protected readonly tarefa = tarefa;
  protected readonly textoDaColuna = textoDaColuna;
  protected readonly tituloDa = tituloDa;
}

// O quadro: provê a loja que os componentes de dentro compartilham, uma
// instância nova cada vez que ele entra na página.
@Component({
  selector: "app-quadro",
  imports: [Cabecalho, ColunaDoQuadro],
  providers: [LojaDoQuadro],
  template: `
    <div class="quadro">
      <app-cabecalho />
      @for (coluna of colunas; track coluna) {
        <app-coluna [coluna]="coluna" />
      }
    </div>
  `,
})
export class Quadro {
  protected readonly colunas = COLUNAS;
}

// A página: o botão que tira o quadro da página e o põe de volta.
@Component({
  selector: "app-quadro-de-tarefas",
  imports: [Quadro],
  template: `
    <main class="pagina">
      <button type="button" class="alternar" (click)="visivel.set(!visivel())">
        {{ visivel() ? "Esconder quadro" : "Mostrar quadro" }}
      </button>
      @if (visivel()) {
        <app-quadro />
      }
    </main>
  `,
})
export class QuadroDeTarefas {
  protected readonly visivel = signal(true);
}
