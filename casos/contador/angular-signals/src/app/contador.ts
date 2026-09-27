import { Component, signal } from '@angular/core';

@Component({
  selector: 'app-contador',
  template: `
    <main class="contador">
      <output>{{ contador() }}</output>
      <button aria-label="Incrementar" (click)="contador.set(contador() + 1)">+</button>
    </main>
  `,
})
export class Contador {
  // O componente raiz não recebe inputs, por isso o valor inicial é um campo
  // e não uma propriedade, como no Solid.
  private readonly valorInicial = 0;

  protected readonly contador = signal(this.valorInicial);
}
