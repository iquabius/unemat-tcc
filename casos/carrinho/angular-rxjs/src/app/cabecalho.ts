import { AsyncPipe } from '@angular/common';
import { Component, inject } from '@angular/core';
import { map } from 'rxjs';
import { textoDoCabecalho } from '../../../dominio';
import { CarrinhoService } from './carrinho.service';

@Component({
  selector: 'app-cabecalho',
  imports: [AsyncPipe],
  template: `
    <header class="cabecalho">
      <strong>Minha loja</strong>
      <span class="resumo">{{ texto$ | async }}</span>
    </header>
  `,
})
export class Cabecalho {
  protected readonly texto$ = inject(CarrinhoService).resumo$.pipe(map(textoDoCabecalho));
}
