import { AsyncPipe } from '@angular/common';
import { Component } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { map, startWith } from 'rxjs';
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

// RxJS de propósito: a lista visível é um fluxo derivado dos valueChanges
// dos controles, embora o Angular atual recomende signals.
@Component({
  selector: 'app-catalogo',
  imports: [ReactiveFormsModule, AsyncPipe],
  template: `
    <main class="catalogo">
      <div class="filtros" [formGroup]="filtros">
        <label>
          Buscar
          <input formControlName="busca" type="search" placeholder="Nome do produto" />
        </label>
        <label>
          Categoria
          <select formControlName="categoria">
            <option value="">Todas</option>
            @for (categoria of categorias; track categoria) {
              <option [value]="categoria">{{ categoria }}</option>
            }
          </select>
        </label>
        <label>
          Ordenar por
          <select formControlName="ordem">
            @for (ordem of ordens; track ordem.valor) {
              <option [value]="ordem.valor">{{ ordem.rotulo }}</option>
            }
          </select>
        </label>
      </div>
      @if (visiveis$ | async; as visiveis) {
        <p class="contagem" role="status">{{ textoDaContagem(visiveis.length) }}</p>
        <ul class="produtos">
          @for (produto of visiveis; track produto.id) {
            <li>
              <span class="nome">{{ produto.nome }}</span>
              <span class="categoria">{{ produto.categoria }}</span>
              <span class="preco">{{ formatarPreco(produto.preco) }}</span>
            </li>
          }
        </ul>
        @if (visiveis.length === 0) {
          <p class="vazio">Nenhum produto encontrado.</p>
        }
      }
    </main>
  `,
})
export class CatalogoDeProdutos {
  protected readonly categorias = categorias;
  protected readonly ordens = ordens;
  protected readonly formatarPreco = formatarPreco;
  protected readonly textoDaContagem = textoDaContagem;

  protected readonly filtros = new FormGroup({
    busca: new FormControl('', { nonNullable: true }),
    categoria: new FormControl('', { nonNullable: true }),
    ordem: new FormControl<Ordem>('nome', { nonNullable: true }),
  });

  // Fluxo da lista visível: recalcula a cada mudança num dos controles
  protected readonly visiveis$ = this.filtros.valueChanges.pipe(
    startWith(this.filtros.getRawValue()),
    map(() => {
      const { busca, categoria, ordem } = this.filtros.getRawValue();
      return produtos
        .filter((produto) => correspondeABusca(produto, busca) && daCategoria(produto, categoria))
        .sort(comparador(ordem));
    }),
  );
}
