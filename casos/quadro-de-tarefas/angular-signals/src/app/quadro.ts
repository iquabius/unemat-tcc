import { NgTemplateOutlet } from "@angular/common";
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
      ouvirOutrasAbas((quadro) =>
        this.despachar({ tipo: "outra-aba", quadro }),
      ),
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
      <span class="resumo">{{ textoDoCabecalho(loja.estado()) }}</span>
      <p class="situacao" role="status">{{ loja.situacao() }}</p>
    </header>
  `,
})
export class Cabecalho {
  protected readonly loja = inject(LojaDoQuadro);
  protected readonly textoDoCabecalho = textoDoCabecalho;
}

@Component({
  selector: "app-coluna",
  imports: [NgTemplateOutlet],
  template: `
    <ng-template #mover let-para="para" let-sinal="sinal" let-id="id">
      @if (para) {
        <button
          type="button"
          attr.aria-label="Mover {{ tarefa(id).titulo }} para {{
            tituloDa(para)
          }}"
          [disabled]="!cabeEm(loja.estado(), para)"
          (click)="loja.despachar({ tipo: 'mover', id: id, para: para })"
        >
          {{ sinal }}
        </button>
      } @else {
        <span></span>
      }
    </ng-template>
    <section class="coluna">
      <h2>{{ textoDaColuna(loja.estado(), coluna()) }}</h2>
      @if (loja.estado()[coluna()].length > 0) {
        <ul>
          @for (id of loja.estado()[coluna()]; track id) {
            <li>
              <span class="titulo">{{ tarefa(id).titulo }}</span>
              <ng-container
                *ngTemplateOutlet="
                  mover;
                  context: {
                    para: vizinhas(coluna()).anterior,
                    sinal: '←',
                    id: id,
                  }
                "
              />
              <ng-container
                *ngTemplateOutlet="
                  mover;
                  context: {
                    para: vizinhas(coluna()).proxima,
                    sinal: '→',
                    id: id,
                  }
                "
              />
              <button
                type="button"
                class="arquivar"
                attr.aria-label="Arquivar {{ tarefa(id).titulo }}"
                (click)="loja.despachar({ tipo: 'arquivar', id: id })"
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
  protected readonly cabeEm = cabeEm;
  protected readonly tarefa = tarefa;
  protected readonly textoDaColuna = textoDaColuna;
  protected readonly tituloDa = tituloDa;
  protected readonly vizinhas = vizinhas;
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
