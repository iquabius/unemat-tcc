import { AsyncPipe } from '@angular/common';
import { Component } from '@angular/core';
import { Subject, scan, startWith } from 'rxjs';

// RxJS de propósito: o Angular atual recomenda signals, mas este exemplo
// existe para comparar com RxJS.
@Component({
  selector: 'app-contador',
  imports: [AsyncPipe],
  template: `
    <main class="contador">
      <output>{{ contador$ | async }}</output>
      <button aria-label="Incrementar" (click)="cliques.next()">+</button>
    </main>
  `,
})
export class Contador {
  private readonly valorInicial = 0;

  // Fluxo que emite um evento a cada clique no botão
  protected readonly cliques = new Subject<void>();

  // Fluxo que acumula "valor + 1" a cada clique, a partir do valor inicial
  protected readonly contador$ = this.cliques.pipe(
    scan((valor) => valor + 1, this.valorInicial),
    startWith(this.valorInicial),
  );
}
