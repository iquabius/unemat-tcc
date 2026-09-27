import { Component, computed, effect, inject, Injectable, signal } from '@angular/core';
import {
  carregarCarrinho,
  formatarPreco,
  MENSAGENS,
  produto,
  produtos,
  quantidadeNoCarrinho,
  reduzir,
  resumir,
  salvarCarrinho,
  textoDoCabecalho,
  textoDoFrete,
  type Acao,
  type EstadoDoCarrinho,
} from '../../../dominio';

// O estado mora num serviço que a Loja fornece; os componentes o recebem
// por injeção, e cada ponto da tela se atualiza só quando o dado que ele lê
// muda.
@Injectable()
export class Carrinho {
  readonly estado = signal<EstadoDoCarrinho>(carregarCarrinho());

  constructor() {
    effect(() => salvarCarrinho(this.estado().itens));
  }

  despachar(acao: Acao) {
    this.estado.update((estado) => reduzir(estado, acao));
  }
}

@Component({
  selector: 'app-cabecalho',
  template: `
    <header class="cabecalho">
      <strong>Minha loja</strong>
      <span class="resumo">{{ textoDoCabecalho(resumir(carrinho.estado().itens)) }}</span>
    </header>
  `,
})
export class Cabecalho {
  protected readonly carrinho = inject(Carrinho);
  protected readonly textoDoCabecalho = textoDoCabecalho;
  protected readonly resumir = resumir;
}

@Component({
  selector: 'app-catalogo',
  template: `
    <section class="catalogo">
      <h2>Produtos</h2>
      <ul>
        @for (p of produtos; track p.id) {
          @let quantidade = quantidadeNoCarrinho(carrinho.estado().itens, p.id);
          <li>
            <span class="nome">{{ p.nome }}</span>
            <span class="preco">{{ formatarPreco(p.preco) }}</span>
            <button
              type="button"
              aria-label="Adicionar {{ p.nome }}"
              (click)="carrinho.despachar({ tipo: 'adicionar', id: p.id })"
            >
              Adicionar
            </button>
            @if (quantidade > 0) {
              <span class="no-carrinho">{{ quantidade }} no carrinho</span>
            }
          </li>
        }
      </ul>
    </section>
  `,
})
export class Catalogo {
  protected readonly carrinho = inject(Carrinho);
  protected readonly produtos = produtos;
  protected readonly formatarPreco = formatarPreco;
  protected readonly quantidadeNoCarrinho = quantidadeNoCarrinho;
}

@Component({
  selector: 'app-painel',
  template: `
    <section class="carrinho">
      <h2>Carrinho</h2>
      @if (carrinho.estado().itens.length > 0) {
        <ul class="itens">
          @for (item of carrinho.estado().itens; track item.id) {
            @let p = produto(item.id);
            <li>
              <span class="nome">{{ p.nome }}</span>
              <span class="quantidade">
                <button
                  type="button"
                  aria-label="Diminuir {{ p.nome }}"
                  (click)="carrinho.despachar({ tipo: 'alterar', id: item.id, delta: -1 })"
                >
                  −
                </button>
                <span class="valor">{{ item.quantidade }}</span>
                <button
                  type="button"
                  aria-label="Aumentar {{ p.nome }}"
                  (click)="carrinho.despachar({ tipo: 'alterar', id: item.id, delta: 1 })"
                >
                  +
                </button>
              </span>
              <span class="subtotal">{{ formatarPreco(p.preco * item.quantidade) }}</span>
              <button
                type="button"
                class="remover"
                aria-label="Remover {{ p.nome }}"
                (click)="carrinho.despachar({ tipo: 'remover', id: item.id })"
              >
                Remover
              </button>
            </li>
          }
        </ul>
        <div class="totais">
          <p>
            <span>Subtotal</span>
            <span>{{ formatarPreco(resumo().subtotal) }}</span>
          </p>
          <p>
            <span>Frete</span>
            <span>{{ resumo().frete === 0 ? 'Grátis' : formatarPreco(resumo().frete) }}</span>
          </p>
          <p class="total">
            <span>Total</span>
            <span>{{ formatarPreco(resumo().total) }}</span>
          </p>
        </div>
        <button type="button" class="finalizar" (click)="carrinho.despachar({ tipo: 'finalizar' })">
          Finalizar compra
        </button>
        <p class="frete">{{ textoDoFrete(resumo()) }}</p>
      } @else if (carrinho.estado().confirmacao; as confirmacao) {
        <p class="confirmacao">{{ confirmacao }}</p>
      } @else {
        <p class="aviso">{{ mensagens.vazio }}</p>
      }
    </section>
  `,
})
export class PainelDoCarrinho {
  protected readonly carrinho = inject(Carrinho);
  protected readonly resumo = computed(() => resumir(this.carrinho.estado().itens));
  protected readonly mensagens = MENSAGENS;
  protected readonly produto = produto;
  protected readonly formatarPreco = formatarPreco;
  protected readonly textoDoFrete = textoDoFrete;
}

@Component({
  selector: 'app-loja',
  imports: [Cabecalho, Catalogo, PainelDoCarrinho],
  providers: [Carrinho],
  template: `
    <div class="loja">
      <app-cabecalho />
      <app-catalogo />
      <app-painel />
    </div>
  `,
})
export class Loja {}
