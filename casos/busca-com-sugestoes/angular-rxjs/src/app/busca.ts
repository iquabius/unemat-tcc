import { AsyncPipe } from '@angular/common';
import { Component } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import {
  Observable,
  Subject,
  catchError,
  distinctUntilChanged,
  map,
  merge,
  of,
  startWith,
  switchMap,
  takeUntil,
  timer,
} from 'rxjs';
import {
  ESPERA_MS,
  MENSAGENS,
  MINIMO_DE_LETRAS,
  buscarCidades,
  rotulo,
  type Cidade,
} from '../../../dominio';

type Estado =
  | { tipo: 'vazio' }
  | { tipo: 'buscando' }
  | { tipo: 'sugestoes'; cidades: Cidade[] }
  | { tipo: 'nenhuma' }
  | { tipo: 'falha' };

const VAZIO: Estado = { tipo: 'vazio' };

// A API simulada como Observable: cancelar a assinatura aborta a requisição.
function buscar$(termo: string): Observable<Cidade[]> {
  return new Observable((assinante) => {
    const controlador = new AbortController();
    buscarCidades(termo, controlador.signal).then(
      (cidades) => {
        assinante.next(cidades);
        assinante.complete();
      },
      (erro) => assinante.error(erro),
    );
    return () => controlador.abort();
  });
}

// RxJS de propósito: este é o caso em que ele mais se destaca (switchMap,
// distinctUntilChanged), embora o Angular atual recomende signals.
@Component({
  selector: 'app-busca',
  imports: [ReactiveFormsModule, AsyncPipe],
  template: `
    <main class="busca">
      <label>
        Cidade de destino
        <input
          name="destino"
          [formControl]="texto"
          autocomplete="off"
          placeholder="Digite ao menos 2 letras"
          (keydown.escape)="cancelamentos.next()"
        />
      </label>
      @let atual = (estado$ | async) ?? vazio;
      @if (mensagem(atual); as texto) {
        <p class="situacao" role="status">{{ texto }}</p>
      }
      @if (atual.tipo === 'sugestoes') {
        <ul class="sugestoes">
          @for (cidade of atual.cidades; track rotulo(cidade)) {
            <li>
              <button type="button" (click)="escolher(cidade)">{{ rotulo(cidade) }}</button>
            </li>
          }
        </ul>
      }
      @if (escolha$ | async; as escolha) {
        <p class="escolha">Destino: {{ escolha }}</p>
      }
    </main>
  `,
})
export class BuscaDeDestino {
  protected readonly rotulo = rotulo;
  protected readonly vazio = VAZIO;
  protected readonly texto = new FormControl('', { nonNullable: true });

  // Esc e a escolha de uma sugestão cancelam a espera e a requisição
  protected readonly cancelamentos = new Subject<void>();
  private readonly escolhas = new Subject<Cidade>();

  protected readonly estado$: Observable<Estado> = merge(
    this.texto.valueChanges.pipe(
      // Espera: cada tecla troca o temporizador; um cancelamento o descarta
      switchMap((valor) =>
        timer(ESPERA_MS).pipe(
          map(() => valor.trim()),
          takeUntil(this.cancelamentos),
        ),
      ),
      distinctUntilChanged(),
      // Cada termo novo troca a requisição anterior, que é abortada
      switchMap((termo) =>
        termo.length < MINIMO_DE_LETRAS
          ? of(VAZIO)
          : buscar$(termo).pipe(
              map((cidades): Estado =>
                cidades.length === 0 ? { tipo: 'nenhuma' } : { tipo: 'sugestoes', cidades },
              ),
              catchError(() => of<Estado>({ tipo: 'falha' })),
              startWith<Estado>({ tipo: 'buscando' }),
              takeUntil(this.cancelamentos),
            ),
      ),
    ),
    this.cancelamentos.pipe(map(() => VAZIO)),
  );

  protected readonly escolha$ = this.escolhas.pipe(map(rotulo));

  protected escolher(cidade: Cidade) {
    // emitEvent: false muda o texto sem passar por valueChanges: nenhuma busca nova
    this.texto.setValue(rotulo(cidade), { emitEvent: false });
    this.cancelamentos.next();
    this.escolhas.next(cidade);
  }

  protected mensagem(estado: Estado): string | null {
    switch (estado.tipo) {
      case 'buscando':
        return MENSAGENS.buscando;
      case 'nenhuma':
        return MENSAGENS.nenhuma;
      case 'falha':
        return MENSAGENS.falha;
      default:
        return null;
    }
  }
}
