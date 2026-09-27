import { Component, computed, signal } from '@angular/core';
import {
  categorias,
  comparador,
  correspondeABusca,
  daCategoria,
  formatarPreco,
  ordens,
  produtos,
  textoDaContagem,
  type Ordem,
} from '../../../dominio';

@Component({
  selector: 'app-catalogo',
  template: `
    <main class="catalogo">
      <div class="filtros">
        <label>
          Buscar
          <input
            name="busca"
            type="search"
            placeholder="Nome do produto"
            [value]="busca()"
            (input)="busca.set($event.target.value)"
          />
        </label>
        <label>
          Categoria
          <select
            name="categoria"
            [value]="categoria()"
            (change)="categoria.set($any($event.target).value)"
          >
            <option value="">Todas</option>
            @for (c of categorias; track c) {
              <option [value]="c">{{ c }}</option>
            }
          </select>
        </label>
        <label>
          Ordenar por
          <select name="ordem" [value]="ordem()" (change)="ordem.set($any($event.target).value)">
            @for (o of ordens; track o.valor) {
              <option [value]="o.valor">{{ o.rotulo }}</option>
            }
          </select>
        </label>
      </div>
      <p class="contagem" role="status">{{ textoDaContagem(visiveis().length) }}</p>
      <ul class="produtos">
        @for (produto of visiveis(); track produto.id) {
          <li>
            <span class="nome">{{ produto.nome }}</span>
            <span class="categoria">{{ produto.categoria }}</span>
            <span class="preco">{{ formatarPreco(produto.preco) }}</span>
          </li>
        }
      </ul>
      @if (visiveis().length === 0) {
        <p class="vazio">Nenhum produto encontrado.</p>
      }
    </main>
  `,
})
export class CatalogoDeProdutos {
  // O template só enxerga membros da classe: o que vem do domínio é
  // repassado aqui.
  protected readonly categorias = categorias;
  protected readonly ordens = ordens;
  protected readonly formatarPreco = formatarPreco;
  protected readonly textoDaContagem = textoDaContagem;

  protected readonly busca = signal('');
  protected readonly categoria = signal('');
  protected readonly ordem = signal<Ordem>('nome');

  // A lista visível é um valor derivado: recalcula só quando busca,
  // categoria ou ordem mudam.
  protected readonly visiveis = computed(() =>
    produtos
      .filter(
        (produto) => correspondeABusca(produto, this.busca()) && daCategoria(produto, this.categoria()),
      )
      .sort(comparador(this.ordem())),
  );
}
