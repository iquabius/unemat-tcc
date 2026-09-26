import { AsyncPipe } from '@angular/common';
import { Component, inject } from '@angular/core';
import { formatarPreco, MENSAGENS, produto, textoDoFrete } from '../../../dominio';
import { CarrinhoService } from './carrinho.service';

@Component({
  selector: 'app-painel',
  imports: [AsyncPipe],
  template: `
    <section class="carrinho">
      <h2>Carrinho</h2>
      @if (carrinho.estado$ | async; as estado) {
        @if (estado.itens.length === 0) {
          @if (estado.confirmacao) {
            <p class="confirmacao">{{ estado.confirmacao }}</p>
          } @else {
            <p class="aviso">{{ mensagens.vazio }}</p>
          }
        } @else {
          <ul class="itens">
            @for (item of estado.itens; track item.id) {
              <li>
                <span class="nome">{{ produto(item.id).nome }}</span>
                <span class="quantidade">
                  <button
                    type="button"
                    [attr.aria-label]="'Diminuir ' + produto(item.id).nome"
                    (click)="carrinho.despachar({ tipo: 'alterar', id: item.id, delta: -1 })"
                  >−</button>
                  <span class="valor">{{ item.quantidade }}</span>
                  <button
                    type="button"
                    [attr.aria-label]="'Aumentar ' + produto(item.id).nome"
                    (click)="carrinho.despachar({ tipo: 'alterar', id: item.id, delta: 1 })"
                  >+</button>
                </span>
                <span class="subtotal">{{ formatarPreco(produto(item.id).preco * item.quantidade) }}</span>
                <button
                  type="button"
                  class="remover"
                  [attr.aria-label]="'Remover ' + produto(item.id).nome"
                  (click)="carrinho.despachar({ tipo: 'remover', id: item.id })"
                >Remover</button>
              </li>
            }
          </ul>
          @if (carrinho.resumo$ | async; as resumo) {
            <div class="totais">
              <p><span>Subtotal</span><span>{{ formatarPreco(resumo.subtotal) }}</span></p>
              <p>
                <span>Frete</span>
                <span>{{ resumo.frete === 0 ? 'Grátis' : formatarPreco(resumo.frete) }}</span>
              </p>
              <p class="total"><span>Total</span><span>{{ formatarPreco(resumo.total) }}</span></p>
            </div>
            <button type="button" class="finalizar" (click)="carrinho.despachar({ tipo: 'finalizar' })">
              Finalizar compra
            </button>
            <p class="frete">{{ textoDoFrete(resumo) }}</p>
          }
        }
      }
    </section>
  `,
})
export class PainelDoCarrinho {
  protected readonly carrinho = inject(CarrinhoService);
  protected readonly mensagens = MENSAGENS;
  protected readonly produto = produto;
  protected readonly formatarPreco = formatarPreco;
  protected readonly textoDoFrete = textoDoFrete;
}
