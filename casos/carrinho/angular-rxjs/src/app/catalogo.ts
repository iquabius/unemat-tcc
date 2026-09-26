import { AsyncPipe } from '@angular/common';
import { Component, inject } from '@angular/core';
import { formatarPreco, produtos, quantidadeNoCarrinho } from '../../../dominio';
import { CarrinhoService } from './carrinho.service';

@Component({
  selector: 'app-catalogo',
  imports: [AsyncPipe],
  template: `
    <section class="catalogo">
      <h2>Produtos</h2>
      <ul>
        @let itens = (carrinho.itens$ | async) ?? [];
        @for (p of produtos; track p.id) {
          <li>
            <span class="nome">{{ p.nome }}</span>
            <span class="preco">{{ formatarPreco(p.preco) }}</span>
            <button
              type="button"
              [attr.aria-label]="'Adicionar ' + p.nome"
              (click)="carrinho.despachar({ tipo: 'adicionar', id: p.id })"
            >
              Adicionar
            </button>
            @if (quantidadeNoCarrinho(itens, p.id); as quantidade) {
              <span class="no-carrinho">{{ quantidade }} no carrinho</span>
            }
          </li>
        }
      </ul>
    </section>
  `,
})
export class Catalogo {
  protected readonly carrinho = inject(CarrinhoService);
  protected readonly produtos = produtos;
  protected readonly formatarPreco = formatarPreco;
  protected readonly quantidadeNoCarrinho = quantidadeNoCarrinho;
}
