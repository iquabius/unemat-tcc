import { Injectable } from '@angular/core';
import { BehaviorSubject, distinctUntilChanged, map } from 'rxjs';
import {
  carregarCarrinho,
  reduzir,
  resumir,
  salvarCarrinho,
  type Acao,
  type EstadoDoCarrinho,
} from '../../../dominio';

// O serviço guarda o estado num BehaviorSubject: quem assina recebe o valor
// atual na hora e cada mudança depois. Todos os componentes injetam a mesma
// instância.
@Injectable({ providedIn: 'root' })
export class CarrinhoService {
  private readonly estado = new BehaviorSubject<EstadoDoCarrinho>(carregarCarrinho());

  readonly estado$ = this.estado.asObservable();
  readonly itens$ = this.estado$.pipe(
    map((estado) => estado.itens),
    distinctUntilChanged(),
  );
  readonly resumo$ = this.itens$.pipe(map(resumir));

  constructor() {
    this.itens$.subscribe(salvarCarrinho);
  }

  despachar(acao: Acao) {
    this.estado.next(reduzir(this.estado.value, acao));
  }
}
