import { Component } from '@angular/core';
import { Cabecalho } from './cabecalho';
import { Catalogo } from './catalogo';
import { PainelDoCarrinho } from './painel';

// RxJS de propósito: o estado compartilhado é um BehaviorSubject num serviço,
// embora o Angular atual recomende signals.
@Component({
  selector: 'app-loja',
  imports: [Cabecalho, Catalogo, PainelDoCarrinho],
  template: `
    <div class="loja">
      <app-cabecalho />
      <app-catalogo />
      <app-painel />
    </div>
  `,
})
export class Loja {}
