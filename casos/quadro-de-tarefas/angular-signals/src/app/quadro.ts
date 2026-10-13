import {
  Component,
  DestroyRef,
  Injectable,
  computed,
  effect,
  inject,
  input,
  signal,
} from "@angular/core";
import {
  COLUNAS,
  MENSAGENS,
  anunciar,
  cabeEm,
  carregarQuadro,
  ouvirOutrasAbas,
  reduzir,
  salvarQuadro,
  tarefa,
  textoDaColuna,
  textoDoCabecalho,
  tituloDa,
  vizinhas,
  type Acao,
  type Coluna,
} from "../../../dominio";

// O quadro e a situação moram num serviço; o componente Quadro o provê, e
// os componentes de dentro recebem a mesma instância por injeção. Cada
// ponto da tela se atualiza quando o signal que ele lê muda.
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
      ouvirOutrasAbas((acao) => this.despachar(acao)),
    );
  }

  despachar(acao: Acao) {
    this.quadro.update((quadro) => reduzir(quadro, acao));
    this.texto.set(anunciar(acao));
  }
}

@Component({
  selector: "app-cabecalho",
  template: `
    <header class="cabecalho">
      <strong>Meu quadro</strong>
      <span class="resumo">{{ resumo() }}</span>
      <p class="situacao" role="status">{{ loja.situacao() }}</p>
    </header>
  `,
})
export class Cabecalho {
  protected readonly loja = inject(LojaDoQuadro);
  protected readonly resumo = computed(() =>
    textoDoCabecalho(this.loja.estado()),
  );
}

@Component({
  selector: "app-coluna",
  template: `
    <section class="coluna">
      <h2>{{ titulo() }}</h2>
      @if (ids().length > 0) {
        <ul>
          @for (id of ids(); track id) {
            <li>
              <span class="titulo">{{ tarefa(id).titulo }}</span>
              @if (vizinhas().anterior; as para) {
                <button
                  type="button"
                  attr.aria-label="Mover {{ tarefa(id).titulo }} para {{
                    tituloDa(para)
                  }}"
                  [disabled]="!cabe(para)"
                  (click)="mover(id, para)"
                >
                  ←
                </button>
              } @else {
                <span></span>
              }
              @if (vizinhas().proxima; as para) {
                <button
                  type="button"
                  attr.aria-label="Mover {{ tarefa(id).titulo }} para {{
                    tituloDa(para)
                  }}"
                  [disabled]="!cabe(para)"
                  (click)="mover(id, para)"
                >
                  →
                </button>
              } @else {
                <span></span>
              }
              <button
                type="button"
                class="arquivar"
                attr.aria-label="Arquivar {{ tarefa(id).titulo }}"
                (click)="arquivar(id)"
              >
                Arquivar
              </button>
            </li>
          }
        </ul>
      } @else {
        <p class="aviso">{{ colunaVazia }}</p>
      }
    </section>
  `,
})
export class ColunaDoQuadro {
  protected readonly tarefa = tarefa;
  protected readonly tituloDa = tituloDa;
  protected readonly colunaVazia = MENSAGENS.colunaVazia;

  readonly coluna = input.required<Coluna>();
  private readonly loja = inject(LojaDoQuadro);
  protected readonly ids = computed(() => this.loja.estado()[this.coluna()]);
  protected readonly titulo = computed(() =>
    textoDaColuna(this.loja.estado(), this.coluna()),
  );
  protected readonly vizinhas = computed(() => vizinhas(this.coluna()));

  protected cabe(para: Coluna) {
    return cabeEm(this.loja.estado(), para);
  }

  protected mover(id: number, para: Coluna) {
    this.loja.despachar({ tipo: "mover", id, para });
  }

  protected arquivar(id: number) {
    this.loja.despachar({ tipo: "arquivar", id });
  }
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
